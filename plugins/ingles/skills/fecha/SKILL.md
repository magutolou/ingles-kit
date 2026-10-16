---
name: fecha
description: >
  Fecha a sessão de inglês: passada completa nas mensagens que o aluno escreveu em inglês, registro em
  escrita/ e em ingles-erros.md, conferência do vocabulário pendente, atualização de ingles-plano.md §Agora e commit.
  Triggers: "/ingles:fecha", "fecha a sessão", "salva a sessão", "terminei por hoje".
---

# /ingles:fecha

Rodar no fim de **toda** sessão, antes de limpar a conversa: os erros das mensagens escritas só
existem na conversa até aqui. Ler antes `${CLAUDE_PLUGIN_ROOT}/referencia/regras.md`: ali está como
achar `<pasta>`, a pasta do inglês.

**Chamada de dentro de outra skill de fechamento** (o `/flush` de um segundo cérebro, encaixado pelo
setup): rodar só os Passos 2 a 5 e devolver um resumo de uma linha pra ela; o commit e a mensagem
final são da skill que chamou.

---

## Passo 1: Data

`date '+%Y-%m-%d %H:%M'` numa chamada própria. Sessão que virou a meia-noite, ou fechamento atrasado:
o registro leva a data **de quando a conversa aconteceu**; se não der pra saber, perguntar em uma linha.

## Passo 2: Erros das mensagens escritas

Juntar **todas** as mensagens que o aluno escreveu em inglês nesta conversa: conversa livre, porquês
do quiz, frases dos cards e as mensagens em inglês do setup. Ficam de fora a transcrição do monólogo
(já tem arquivo próprio) e as respostas de lacuna do quiz (já estão no `ingles-quiz-log.md`).

Passada completa, mensagem por mensagem, em `<pasta>/escrita/escrita-AAAA-MM-DD.md`:

```markdown
---
type: escrita
date: AAAA-MM-DD
---
| # | Escreveu | Mais natural | Tipo |
|---|---|---|---|
```

Mesmas regras do monólogo: forma nativa sem trocar o sentido, categorias de `ingles-erros.md`, nunca amostra
apresentada como total. Arquivo do dia já existe (segunda sessão no mesmo dia): **acrescentar**,
continuando a numeração. Nunca sobrescrever.

Erro que repete um erro antigo: anotar no Tipo ("repete o 5 de 11/10"). É o sinal mais útil pro aluno.

Sem mensagem em inglês na sessão: pular o passo.

## Passo 3: `ingles-erros.md`

Pra cada categoria que apareceu na escrita de hoje: +1 em "Dias" **se o dia ainda não foi contado**
(o `/ingles:monologo` de hoje pode já ter contado), e a ocorrência na coluna (`16/10: 3 fala + 2 escrita`).

## Passo 4: Vocabulário

Conferir que todo verbete desta conversa está em `ingles-vocab-pendentes.md` (o `/ingles:vocab` escreve na hora;
aqui é a rede de segurança). Palavra em português no meio de uma mensagem em inglês também entra, com
origem `chat`.

## Passo 5: `ingles-plano.md` §Agora

Atualizar o que mudou: unit atual e próxima, último monólogo, próximo tema, quantas palavras pendentes
de card. Mudança de configuração pedida na conversa (frequência, Anki) vai pra §Configuração.

## Passo 6: Commit

Só a pasta do inglês, nunca `git add -A`: o repo pode ter outras mudanças que não são desta sessão.

```bash
git add "<pasta>"
git commit -m "ingles AAAA-MM-DD: <resumo curto>"
```

Resumo do que aconteceu, ex.: `monólogo (31 erros), unit 121, 4 cards`. Áudio e livros ficam fora pelo
`.gitignore`; conferir no `git status` que nenhum `.m4a` ou PDF entrou. Pasta sem git: pular.

## Passo 7: Mostrar

Curto:

- os erros da escrita de hoje (a tabela, se for pequena; senão o total e as categorias);
- as categorias que mais cresceram em `ingles-erros.md`;
- o próximo passo concreto (tema do próximo monólogo, próxima unit, pendentes de card).
