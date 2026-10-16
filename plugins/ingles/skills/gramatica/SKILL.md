---
name: gramatica
description: >
  Sessão de gramática: escolhe o tópico pelos erros recorrentes (ou pela ordem do livro, na trilha
  inicial), lê a unit do livro e ensina passo a passo, com checagem a cada passo e lote final de quiz.
  Registra cada item no quiz-log.
  Triggers: "/ingles:gramatica", "aula de gramática", "próxima unit", "quiz de gramática", "corrige meu study guide".
---

# /ingles:gramatica

O aluno **não lê o livro**: o agente lê a unit antes e ensina. Ler antes `${CLAUDE_PLUGIN_ROOT}/referencia/regras.md`: ali está como achar `<pasta>`, a pasta do inglês.

---

## Fase 0: Escolher o tópico

Ler `ingles-plano.md` (§Configuração e §Agora), `ingles-erros.md` e as últimas linhas de `ingles-quiz-log.md`.

- **Unit em andamento** em §Agora → continuar dela.
- **Trilha sequencial (A1-A2):** a próxima unit na ordem do livro. Se uma categoria de `ingles-erros.md` já
  aparece em muitos dias e a unit dela está longe, dá pra adiantar; propor e deixar o aluno decidir.
- **Trilha guiada por erro (B1+):** a categoria com **mais dias** em `ingles-erros.md` (dias, não ocorrências:
  10 erros num monólogo só pesam menos que o mesmo erro em 4 dias diferentes). Achar as units do livro
  que cobrem essa categoria pelo sumário (ex.: preposição de tempo, de lugar, preposição dependente).
  Tópico grande vira sequência de units, anotada em §Agora.
- **Sem erro recorrente ainda** (começo): sondagem pelo **Study guide** do livro (teste diagnóstico que
  aponta a unit). O aluno faz no PDF ou no papel e manda as respostas; o agente corrige pelo gabarito
  do livro e as erradas viram a lista de units.

Dizer o tópico e o porquê em uma linha ("preposição: 4 dias em `ingles-erros.md`, 13 ocorrências") e
começar.

---

## Fase 1: Ler a unit

PDF em `<pasta>/livros/`. Ler a unit inteira antes de ensinar, e o apêndice ou a página do Swan se o
tópico tiver caso de borda. Plano interno: **cada seção da unit (A, B, C...) é um passo**, na ordem e
no raciocínio do livro, usando os termos do livro.

**Sem PDF** (ou PDF escaneado ilegível): ensinar pelo próprio conhecimento, seguindo a mesma estrutura
em passos, e avisar uma vez que a referência é o agente, não o livro.

---

## Fase 2: Ensino passo a passo

Pra cada passo:

1. **Regra em poucas linhas** + 2-3 exemplos. Partir de um **erro real do aluno** quando houver
   (buscar em `monologos/` e `escrita/`): "você disse *in October 7th*; data leva *on*".
2. **1-2 itens de checagem.**
3. Acertou → próximo passo. Errou → **outra explicação** (outro ângulo, outro exemplo) e item novo,
   sem avançar. Errou de novo → mostrar o contraste lado a lado (`at night` × `in the night`).

Nível A1-A2: explicação em PT, exemplos em inglês. B1+: em inglês, com PT só onde o contraste com o
português for o ponto.

---

## Fase 3: Lote final

Fim da unit: **lote de 5 itens** misturando os passos.

- Resposta numa mensagem só (numerada).
- Uns **2/3 só em inglês** (lacuna, achar o erro, completar); tradução PT→EN só nos pontos onde o
  português induz o erro.
- Todo item aceita **"don't know"**. Pedir um **porquê curto em inglês** junto da resposta: mostra
  chute, e erro de inglês no porquê vai pro registro de escrita (`/ingles:fecha`).
- Acertou, o lote seguinte sobe a dificuldade; errou, estreita no ponto do erro. Errou 2 ou mais,
  outro lote só daquele passo.
- Se o app do aluno sugere texto no campo de resposta (o Claude desktop faz isso), pedir que ele
  desligue durante o quiz: a sugestão entrega a resposta.

---

## Fase 4: Registrar

1. **`ingles-quiz-log.md`**, um item por linha:
   `| Data | Unit | Passo | Item | Resposta | Certo | Tipo de erro |`
   O item é a lacuna resumida (`born ___ 2007`), não a frase inteira. Revisões longas podem virar uma
   linha só com o placar (`22 lacunas mistas A-E | | 21/23`) mais uma linha por erro.
2. **`ingles-plano.md` §Agora:** unit concluída, próxima unit da sequência, e o que observar no próximo
   monólogo ("preposição de tempo: conferir se `on` + data apareceu certo").
3. O **próximo monólogo** mostra se transferiu. Se a categoria seguir aparecendo em `ingles-erros.md` depois
   da unit, a regra não é o problema: é tirar a forma em tempo real. Sugerir mais leitura em voz alta e
   shadowing, não repetir a unit.

Não commitar aqui: o commit é do `/ingles:fecha`.

---

## Regras

- **Exercício no formato do livro, frases do agente.** Mesmo tipo e estrutura dos exercícios da unit;
  nunca copiar nem parafrasear item do livro.
- **Contextos variados:** a vida do aluno às vezes, mas sem repetir sempre os mesmos temas; trabalho,
  viagem, ciência, o dia a dia de outras pessoas.
- **Gramática não vira card de Anki.** Card é só vocabulário.
- **Material do livro vence a memória do agente** em caso de divergência; o Swan desempata caso de
  borda.
