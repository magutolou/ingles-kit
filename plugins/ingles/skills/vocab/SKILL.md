---
name: vocab
description: >
  Dicionário de inglês no chat, no estilo do Cambridge: verbete com pronúncia, significados, estrutura,
  comparação e erros típicos de falante de português. Registra toda palavra pesquisada, monta os cards
  com frases escritas pelo aluno (Anki opcional) e revisa o registro sem Anki.
  Triggers: "/ingles:vocab", "/ingles:vocab <palavra>", "/ingles:vocab cards", "/ingles:vocab revisa", "modo vocab", "o que significa <palavra>".
---

# /ingles:vocab

Ler antes `${CLAUDE_PLUGIN_ROOT}/referencia/regras.md`: ali está como achar `<pasta>`, a pasta do inglês.

| Invocação | O que faz |
|---|---|
| `/ingles:vocab` | Liga o **modo vocab** na conversa: toda palavra, expressão ou frase que ele mandar recebe verbete. Desliga quando ele pedir ("sai do vocab"). |
| `/ingles:vocab <palavra ou frase>` | Um verbete avulso, no meio de qualquer sessão, e volta ao assunto. |
| `/ingles:vocab cards` | Transforma as pendentes em cards, com frases escritas por ele. |
| `/ingles:vocab revisa` | Revisão ativa do registro (feita pra quem não usa Anki, mas serve pra todos). |

---

## Fase 1: Verbete

Língua do verbete pelo nível (`ingles-plano.md`): A1-A2, explicação em PT e exemplos em inglês; B1 ou acima,
em inglês com equivalentes em PT no fim. Ordem fixa das seções; **seção que não agrega pra aquela
palavra sai**. O tamanho acompanha a pergunta: palavra simples pede verbete curto, idioma traiçoeiro
pede tudo.

1. **Título** `## <expressão>`, na forma de dicionário (`see (something) through`).
2. **Pronunciation:** IPA UK e US, mais uma dica quando há armadilha pra falante de PT (`th`, letra
   muda, vogal curta, sílaba tônica).
3. **Part of speech** (+ registro: informal, formal, vulgar, arcaico).
4. **Meaning(s):** numerados, sentido principal primeiro, cada um com 2-3 exemplos com a palavra em
   negrito.
5. **Structure:** padrão gramatical (`can't help but` + verbo base).
6. **Collocations / related forms:** colocações, família da palavra, sentidos que confundem.
7. **Comparação:** tabela `palavra | nuance` com quase-sinônimos.
8. **Common mistakes for Portuguese speakers:** ✗ → ✓. **Sempre presente.**
9. **Portuguese equivalents.** **Sempre presente.**

No modo vocab, fechar com `Next word?`.

- **Frase de contexto manda.** Se ele mandou a frase onde achou a palavra, o verbete explica **a frase**
  antes da palavra solta: o sentido dela, a quebra em partes, a paráfrase. Muitas vezes ele conhece
  todas as palavras e o que travou foi o idioma (`can't help but`).
- **Palavra que surge dentro do verbete** ("também não sei o que é *stingy*") ganha verbete próprio.
- **Correção dele sobre o contexto:** resposta curta ajustando, sem refazer o verbete.
- **Fonte:** conhecimento do agente; se ele pedir "confere no Cambridge" ou algo soar estranho, buscar
  e corrigir.

---

## Fase 2: Registro imediato

Toda expressão que recebeu verbete entra **na hora** em `<pasta>/ingles-vocab-pendentes.md`, uma linha:

`| expressão (forma de dicionário) | frase de contexto dele, literal (se mandou) | data | origem |`

Origem: `vocab`, `monólogo`, `chat`. Escrever na hora, e não só no fim, porque a conversa pode ser
limpa antes do `/ingles:fecha`, e o registro é o que sobrevive. Antes de escrever, conferir se a expressão
já está em `ingles-vocab-pendentes.md` ou no `ingles-vocabulario.csv` (aí avisar que ele já tem card daquela palavra).

---

## Fase 3: Cards (`/ingles:vocab cards`)

Origem da lista: `ingles-vocab-pendentes.md`. Conversa nova não tem o verbete; se ele precisar relembrar o sentido,
refazer um verbete curto.

1. **Duplicata:** conferir no `ingles-vocabulario.csv` pela Frente e pelo sentido. Já tem card: dizer quais
   sentidos o card cobre e perguntar se completa ou pula.
2. **Uma palavra por vez** (ele pode responder várias de uma vez). Mostrar a palavra e a tradução
   proposta pro Verso. **Ele escreve as frases primeiro**, até 3, de usos diferentes. Nunca propor
   frase antes dele: escrever é a parte que fixa.
3. **Revisar o que ele mandou:**
   - corrigir pra forma nativa **sem trocar o sentido nem a frase**;
   - avisar se duas frases usam o mesmo sentido;
   - avisar se falta um uso importante (o principal, ou o que mais confunde falante de PT);
   - a frase de contexto dele pode ser uma das três.
   Avisou, ele refaz. Não reescrever por ele. Erro de inglês nas frases dele também conta pro `/ingles:fecha`.
4. **Gravar no `ingles-vocabulario.csv`** com Edit (nunca por shell), no formato:
   - Frente = expressão, na forma de dicionário;
   - Verso = `tradução<br><br>"frase 1"<br>"frase 2"<br>"frase 3"`, sem explicação;
   - Tags = `uid::voc-NNNN vocab`, com o próximo número livre;
   - aspas internas dobradas (`""`), campo com vírgula entre aspas. Conferir que toda linha tem 3 colunas.
   Exemplo:
   ```
   script,"roteiro<br><br>""I can't follow the script.""<br>""I wrote a script to rename the files.""",uid::voc-0001 vocab
   ```
5. **Tirar a palavra de `ingles-vocab-pendentes.md`.**
6. **Anki** (só se `ingles-plano.md` diz `Anki: sim`):
   `python "${CLAUDE_SKILL_DIR}/push-anki.py" --csv "<pasta>/ingles-vocabulario.csv" --dry-run` primeiro,
   depois sem `--dry-run` (`--deck` muda o nome do deck, padrão `English`). O script precisa do
   Anki aberto com o AnkiConnect. Se o dry-run mostrar `~` (card que vai ser sobrescrito), o aluno
   editou aquele card no app: mostrar a diferença e perguntar antes do push de verdade. Anki fechado e
   o agente com acesso ao PC: oferecer abrir.
   Sem AnkiConnect: lembrar que *File → Import* do `ingles-vocabulario.csv` funciona.

---

## Fase 4: Revisão (`/ingles:vocab revisa`)

Revisão de **produção**, não de reconhecimento:

1. Sortear 5 cards do `ingles-vocabulario.csv`, misturando os recentes (últimos ~10) com os antigos.
2. Pra cada um, mostrar **só a tradução em PT** (ou um contexto em PT) e pedir uma frase nova em
   inglês usando a expressão. Uma mensagem com as 5 respostas.
3. Corrigir as frases (forma nativa, sem trocar o sentido) e dizer quais expressões ele não lembrou.
4. Expressão esquecida: perguntar se ele quer reforçar o card (mais uma frase, outro sentido).

Não é repetição espaçada de verdade: quem quer isso usa o Anki. É um jeito de manter o registro vivo e
de puxar as palavras pra fala.

---

## Regras

- Verbete tem ordem fixa e tamanho variável; "Common mistakes" e "Portuguese equivalents" nunca saem.
- Frase de contexto vem antes da palavra solta.
- Nos cards, ele escreve primeiro e o agente revisa.
- Card é só vocabulário: gramática não vira card.
- O `ingles-vocabulario.csv` é o registro, com ou sem Anki; o Anki é só um espelho dele.
