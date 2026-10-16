---
name: monologo
description: >
  Corrige um monólogo gravado em inglês: transcreve com o Whisper em modo que preserva erro, faz a
  passada completa frase a frase, devolve a versão corrigida pra ler em voz alta, soma as categorias
  em ingles-erros.md e separa até 3 palavras pro vocabulário. Também diz o tema do próximo monólogo.
  Triggers: "/ingles:monologo", "corrige o de hoje", "corrige o monólogo", "qual o tema de hoje", "/ingles:monologo tema".
---

# /ingles:monologo

Peça central da produção. Ler antes `${CLAUDE_PLUGIN_ROOT}/referencia/regras.md`: ali está como achar `<pasta>`, a pasta do inglês.

| Invocação | O que faz |
|---|---|
| `/ingles:monologo tema` (ou "qual o tema de hoje") | Fase 0 só |
| `/ingles:monologo` (ou "corrige o de hoje") | Fases 1 a 6 |

---

## Fase 0: Antes de gravar

1. Tema de hoje pelo ciclo em `ingles-plano.md` §Ciclo de temas (dia da semana + semana do ciclo). Dia que não
   é de monólogo: dizer qual é o próximo.
2. Os **até 3 itens de vocabulário do monólogo anterior** (estão no fim do arquivo dele em
   `monologos/`): mostrar e pedir pra tentar usar no novo. São 30 segundos.
3. Lembrar a duração do plano e: **sem roteiro** (no nível A1-A2, tópicos escritos são permitidos no
   começo), **sem parar pra corrigir**, se faltar a palavra diz em português e segue. Palavra dita em
   PT não é falha: é exatamente o dado que vira card.

---

## Fase 1: Achar o material

- Áudio em `<pasta>/audio/`: o de hoje (`AAAA-MM-DD.*`); sem data no nome, o mais recente, e confirmar
  com o aluno. Pode ser também um caminho que ele mandar.
- Ou o texto colado (transcrição do celular): pular pra Fase 3 e marcar no arquivo que a transcrição
  não veio do Whisper em modo de erro (vê menos erro).

O git não guarda pasta vazia: num clone novo, `<pasta>/audio/`, `monologos/` e `escrita/` podem não
existir. Criar com `mkdir -p` antes de usar, sem tratar a ausência como erro.

---

## Fase 2: Transcrever sem "limpar" a fala

**O problema:** transcritor automático é um modelo de linguagem, e modelo de linguagem prevê o texto
**fluente** mais provável. Ele limpa a fala: some hesitação, aparece artigo que o aluno não disse,
aparece `-s` de terceira pessoa, o passado errado vira certo. Caso real: "I buyed" saiu transcrito
como "I buy". Resultado: a análise **subestima** os erros, e justamente os de gramática, que são os
que interessam.

**Dois mecanismos que reduzem a limpeza** (usar sempre):

1. `--condition_on_previous_text False`: o Whisper transcreve em janelas de ~30 s e, por padrão, cada
   janela recebe o texto da anterior como contexto. Se a primeira saiu limpa, as seguintes copiam o
   estilo limpo. Desligar isso faz cada trecho ser transcrito pelo que foi dito.
2. `--initial_prompt` **cheio de hesitação e de erro**: o prompt inicial funciona como exemplo de
   estilo, e o modelo imita. Um prompt com "um", "uh", reinício de frase e erro gramatical faz ele
   transcrever do jeito que a pessoa fala, em vez de normalizar.

```bash
whisper <pasta>/audio/AAAA-MM-DD.m4a --model small --language en --condition_on_previous_text False --output_format txt --output_dir <pasta>/audio --initial_prompt "Um, so, uh, I think that, I mean, he go to the... the school yesterday, and, like, it was, uh, more better."
```

No caso real, a passada em modo de erro achou 4 erros a mais que a passada padrão no mesmo áudio
(dois de classe de palavra, um artigo e um falso cognato que a primeira tinha "consertado"). **Reduz a limpeza, não elimina.**
Pronúncia não dá pra avaliar por transcrição.

Rodar no terminal (o modelo `small` em CPU leva alguns minutos pra um áudio de 5 min; rodar em
background se a ferramenta permitir). Ler o `.txt` gerado.

**Checagem do aluno (obrigatória):** mostrar a transcrição e pedir que ele marque:
- onde o Whisper ouviu errado (nome próprio, palavra trocada);
- **onde ele disse uma palavra em português**. O Whisper "traduz" ou deforma a palavra em PT (caso
  real: "propostas" saiu "proposters", "partido" saiu "Partidu"), e sem a marcação dele esses
  fallbacks passam como erro de pronúncia ou somem.

Anotar as correções dele na transcrição como `[= ...]`. Erro do Whisper não conta como erro do aluno.

---

## Fase 3: Passada completa

Frase por frase, **todos** os erros, na ordem do áudio. Tabela numerada:

| # | Disse | Mais natural | Tipo |
|---|---|---|---|

- **Mais natural** = a frase dele dita por um nativo, sem trocar o sentido nem a ideia.
- **Tipo**: usar primeiro as categorias que já existem em `ingles-erros.md`, pra a contagem somar. Categorias
  de partida:
  preposição · artigo · vocabulário / falso cognato · **português no meio da frase** (categoria própria) ·
  forma verbal / tempo · concordância · classe de palavra (`difficult` por `difficulty`) ·
  posição de advérbio · estrutura de frase / calque do PT · sujeito ou objeto ausente ·
  frase quebrada no meio · colocação.
  Criar categoria nova só quando nenhuma serve.
- Erro pequeno também entra. Se o agente decidir não listar algo (estilo, preferência), diz.

Depois da tabela:

- **Padrões:** categoria | ocorrências | itens.
- **Leitura:** 1-2 hipóteses sobre o que domina, ditas como hipótese ("parece que os tempos verbais
  quebram quando a frase fica longa, não por falta de conhecimento: o *present perfect* saiu certo em
  X"). O aluno costuma achar que o problema é um (tempo verbal) e a tabela mostrar outro (preposição).
- Opcional: ritmo em palavras por minuto (contagem aproximada; nativo conversando fica em 130-150).

---

## Fase 4: Versão corrigida pra ler em voz alta

O monólogo inteiro reescrito com as correções, em parágrafos, **mantendo as frases e as ideias dele**.
Não é redação melhorada: é o que ele disse, do jeito que um nativo diria.

Pedir pra ele **ler em voz alta agora**. É o passo principal do método; não precisa escrever nada.

---

## Fase 5: Registrar

1. **Arquivo** `<pasta>/monologos/AAAA-MM-DD-assunto.md` (assunto em kebab-case):
   ```markdown
   ---
   type: monologo
   date: AAAA-MM-DD
   audio: <pasta>/audio/AAAA-MM-DD.m4a (fora do git)
   duracao: M:SS
   transcricao: whisper small, modo de erro   # ou "celular", "texto colado"
   tema: ...
   ---
   ## Transcrição
   ## Erros (passada completa): N no total
   ## Padrões
   ## Versão corrigida
   ## Vocabulário do dia
   ```
2. **`ingles-erros.md`:** pra cada categoria que apareceu, +1 em "Dias" e a ocorrência do dia na coluna de
   ocorrências (`16/10: 5 fala`). Categoria nova entra com 1 dia. Atualizar o exemplo se o novo for
   mais claro.
3. **Vocabulário do dia (até 3):** palavra dita em português, palavra que faltou, falso cognato. Vão
   pra `<pasta>/ingles-vocab-pendentes.md` (expressão | frase de contexto | data | origem `monólogo`) e pro fim
   do arquivo do monólogo. **Erro de gramática não vira card:** fica em `ingles-erros.md` e vira tópico de
   gramática quando se repetir.
4. **`ingles-plano.md` §Agora:** data do último monólogo e o próximo tema.

---

## Fase 6: Fechar

Mensagem curta:

- total de erros e as 2 categorias que mais apareceram;
- os 3 itens de vocabulário (e que `/ingles:vocab cards` transforma em card);
- se alguma categoria já aparece em vários dias de `ingles-erros.md` e é candidata ao próximo `/ingles:gramatica`,
  dizer qual;
- o tema do próximo monólogo.

Não commitar aqui: o commit é do `/ingles:fecha`.

---

## Regras

- **Correção no mesmo dia da gravação.** Monólogo antigo também se corrige quando ele mandar, mas
  monólogo pulado não vira dívida: não pedir pra ele "repor".
- **Passada completa.** Nunca apresentar amostra como total.
- **Sugerir, não concluir, o motivo do erro.**
- Erro do Whisper sai da contagem; palavra em PT conta, na categoria própria.
- A conversa da Fase 2 é em PT ou EN, como o aluno preferir; o registro é em PT.
