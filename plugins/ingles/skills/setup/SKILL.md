---
name: setup
description: >
  Instala o plugin de inglês na pasta atual (escolhe onde guardar os dados, acrescenta um bloco ao
  CLAUDE.md, encaixa no fechamento de sessão que já existir) e monta o plano: perfil, diagnóstico de
  nível (EF SET + amostra de produção), trilha de gramática, frequência do monólogo, ciclo de temas,
  vocabulário com ou sem Anki, exposição e checkpoint. Também reconfigura um plano existente.
  Use quando o aluno pedir pra configurar o inglês, montar o plano de inglês ou mudar a frequência do monólogo.
---

# /ingles:setup

Ler antes `${CLAUDE_PLUGIN_ROOT}/referencia/regras.md`.

Tom de conversa, **uma pergunta por vez**, em PT (o aluno pode trocar pra inglês quando quiser).

---

## Fase 0: Detecção

Procurar o bloco `<!-- ingles-kit:inicio -->` no `CLAUDE.md` da pasta atual.

- **Sem bloco** → **instalação** (Fase I) e depois setup completo (Fases 1 a 6).
- **Com bloco**, e `<pasta>/ingles-plano.md` ainda com os marcadores `<!-- ... -->` → setup completo, sem
  reinstalar.
- **Com bloco e plano preenchido** → **reconfiguração**: perguntar o que mudar (frequência do
  monólogo, dias, nível, Anki, modo de correção das mensagens, temas) e editar só aquilo. Mudou o nível
  ou a frequência: refazer o ciclo de temas a partir da próxima semana, sem apagar o que já foi feito.

---

## Fase I: Instalação na pasta do aluno

O plugin traz o comportamento (as skills); os dados do aluno moram no repo dele. Esta fase decide onde
e encaixa o inglês no que já existe, **sem sobrescrever nada**. Cada escrita fora da pasta do inglês
(`CLAUDE.md`, `.gitignore`, skill de fechamento) é mostrada e só acontece com o "sim" dele.

### I.1 Olhar a pasta (sem output)

- É repo git? (`git rev-parse --show-toplevel`). Se a pasta atual não for a raiz do repo, avisar e
  perguntar se ele quer abrir o Claude Code na raiz.
- Tem `CLAUDE.md`? Tem cara de segundo cérebro (`memory/projects/`, `wiki/`, `*_index.md`)?
- Já existe coisa de inglês? Buscar por nome de arquivo e conteúdo, tolerando acento:
  `git ls-files | grep -iE "ingl|english"` e `grep -rilE "ingl[eê]s|english" --include=*.md . | head`.
- Tem skill de fim de sessão? Listar as skills do repo (`ls skills .claude/skills .claude/commands`)
  e ler o `name` e a `description` do frontmatter das candidatas pelo nome (`flush`, `fecha`, `salva`,
  `wrap`, `close`, `end`). Conta a skill **cujo papel** é fechar ou salvar a sessão; uma skill que só
  menciona o `/flush` no texto não conta (num segundo cérebro, quase todas mencionam).
- O repo tem **convenção própria pra pasta nova**? Ler o `CLAUDE.md` dele procurando índice ou hub por
  pasta, script que gera índice, checador de links, nomes de arquivo únicos. Anotar pra I.3.

### I.2 Propor onde guardar os dados

| O que a pasta é | Proposta |
|---|---|
| Segundo cérebro com `memory/projects/` | `memory/projects/ingles/` (ou o nome que ele preferir, se já houver arquivo `ingles.md` ali) |
| Repo qualquer | `ingles/` na raiz |
| Pasta vazia ou sem git | `ingles/` e oferecer `git init` (o histórico do git é o que guarda a evolução) |

**Já existe material de inglês** (um plano antigo, uma lista de erros): mostrar o que achou e
perguntar. O kit **não migra nem apaga** nada sozinho: ou a pasta nova fica ao lado e o material
antigo segue onde está, ou ele pede a migração como tarefa à parte.

### I.3 Criar a pasta

Copiar os modelos sem sobrescrever arquivo existente e criar as subpastas:

```bash
mkdir -p "<pasta>/monologos" "<pasta>/escrita" "<pasta>/audio" "<pasta>/livros"
cp -n "${CLAUDE_PLUGIN_ROOT}"/templates/* "<pasta>/"
```

Conferir com `ls -R "<pasta>"`. Os arquivos levam o prefixo `ingles-` de propósito: num vault com
links por nome de arquivo (Obsidian, `[[wikilink]]`), `plano.md` ou `erros.md` colidiriam com os do
aluno.

Se a I.1 achou convenção de pasta no repo (hub `<pasta>_index.md`, script que gera índice), seguir a
convenção depois de criar: rodar o gerador dele ou criar o hub no formato dele, e rodar o checador de
links se houver. A convenção do repo vence a do kit; só os nomes dos 5 arquivos de dados não mudam,
porque as skills procuram por eles.

### I.4 `.gitignore`

Acrescentar (criando o arquivo se não existir; nunca reescrevendo o que já tem) as linhas que deixam
áudio e livros fora do git:

```
# ingles-kit: áudio e livros ficam só no computador
<pasta>/audio/
<pasta>/livros/
```

### I.5 Bloco no `CLAUDE.md`

Acrescentar **no fim** do `CLAUDE.md` (criar um mínimo, só com o bloco, se não existir). Mostrar o
bloco antes de escrever:

```markdown
<!-- ingles-kit:inicio -->
## Inglês (plugin `ingles`)

- Pasta do inglês: `<pasta>`. Plano em `ingles-plano.md`, erros recorrentes em `ingles-erros.md`.
- Skills: `/ingles:monologo`, `/ingles:gramatica`, `/ingles:vocab`, `/ingles:fecha`, `/ingles:setup`.
  Regras completas no plugin (`referencia/regras.md`), lidas pelas skills.
- Mensagens que eu escrever em inglês são amostra de produção: anote os erros e registre no
  fechamento da sessão. Modo de correção em `ingles-plano.md` §Configuração (no fim ou na hora).
- Corrija pra forma nativa sem trocar o sentido nem a minha frase.
<!-- ingles-kit:fim -->
```

O bloco entre marcadores é do plugin: reinstalar substitui só o que está entre eles.

### I.6 Fechamento de sessão

Os erros das mensagens escritas só existem na conversa até alguém registrar. Duas saídas:

- **Ele já tem uma skill de fim de sessão** (ex.: `/flush` de um segundo cérebro): propor acrescentar
  a ela um passo, mostrado antes:
  > **Inglês (plugin `ingles`):** se o bloco `ingles-kit` existe no `CLAUDE.md` e houve mensagem em
  > inglês, `/ingles:vocab` ou `/ingles:monologo` nesta sessão, executar os Passos 2 a 5 de
  > `/ingles:fecha` (o commit fica com esta skill).

  Assim existe uma rotina de fechamento só. Se ele recusar, o `/ingles:fecha` faz tudo, inclusive
  o commit.
- **Não tem:** o `/ingles:fecha` é a rotina dele. Dizer: "rode `/ingles:fecha` no fim de toda sessão,
  antes de limpar a conversa".

### I.7 Conferir

Mostrar em 4 linhas: pasta criada, `.gitignore`, bloco no `CLAUDE.md`, fechamento escolhido. Não
commitar ainda: o commit é o da Fase 6.

---

## Fase 1: Perfil (conversa)

Perguntar, uma por vez, e adaptar a ordem ao que ele já contou:

1. Como quer ser chamado.
2. **Pra que quer inglês:** conversar, trabalho, entrevista, intercâmbio, prova, conteúdo. Muda o tipo
   de tema e de vocabulário.
3. **Autoavaliação:** entende bem e trava pra falar? Entende pouco? Escreve melhor do que fala?
4. **Como já consome inglês hoje** (séries, jogos, YouTube, nada).
5. **Tem com quem falar** em inglês (amigo, parente, trabalho, comunidade online)? Se tiver, entra na
   rotina como conversa semanal.
6. **Tempo por dia** que dá pra pôr de verdade (não o ideal).
7. **Interesses** (3 a 6): é daqui que saem os temas do monólogo e as sugestões de conteúdo.

---

## Fase 2: Nível

### 2a. EF SET (lado receptivo)

Pedir o **EF SET** (efset.org, grátis, dá o nível CEFR de A1 a C2):

- **50 min** (leitura + listening): o recomendado, dá a linha de base mais confiável.
- **15 min**: pra quem está começando e acharia 50 min pesado, ou pra quem tem pressa.

Explicar em uma linha: o EF SET mede **entender**, não falar. Quem consome muito conteúdo costuma
tirar nota bem acima da própria fala, e a distância entre as duas é justamente o tamanho do problema.

Se ele disser que quase não entende inglês, não insistir no teste de 50 min: o de 15 min ou a
autoavaliação bastam pra começar na trilha inicial.

### 2b. Amostra de produção (o diagnóstico que importa)

Pelo que ele contou e pelo EF SET:

- **Consegue falar alguma coisa** → **monólogo diagnóstico**, sem roteiro, sobre um tema que ele
  conhece e que tenha opinião (3-5 min se B1 ou acima; 1-2 min se A2). Ele grava e o `/ingles:monologo` faz a
  passada completa. Este é o **"antes"** do checkpoint; guardar o tema.
- **Também (todos que conseguem escrever):** 5 a 10 linhas em inglês sobre ele mesmo, no chat.
  Passada completa, igual à do `/ingles:fecha`.
- **Não consegue nem escrever frases simples** → pular a amostra; começar a trilha inicial e fazer
  a primeira amostra depois de algumas units.

O diagnóstico pode levar mais de uma sessão (o aluno vai gravar e volta). Nesse caso, salvar no
`ingles-plano.md` o que já tem, marcar o que falta em §Agora e continuar no próximo `/ingles:setup`.

### 2c. Nível de trabalho

**Quem manda na gramática e no monólogo é a produção, não o EF SET.** EF SET C1 com fala B1 é
trilha B1 na gramática e no monólogo, e C1 só nas sugestões de conteúdo. Registrar os dois números.

---

## Fase 3: Configuração

Propor pela tabela e pelo tempo disponível; **ele decide**. Tudo vai pra `ingles-plano.md` §Configuração.

| | A1-A2 | B1-B2 | C1+ receptivo, fala travada |
|---|---|---|---|
| **Trilha de gramática** | sequencial: uma unit por sessão, na ordem do livro | guiada por erro, com o *Study guide* do livro tapando lacunas | guiada por erro |
| **Livro** | *Essential Grammar in Use* | *English Grammar in Use* | *English Grammar in Use* + Swan pra caso de borda |
| **Monólogo** | 1-2 min; no começo pode escrever tópicos antes, depois sem roteiro | 3-5 min, sem roteiro | 5 min, sem roteiro |
| **Temas** | rotina, descrever pessoa ou lugar, o que fez ontem, planos | opinião, explicar algo que sabe, história do passado, planos | conceito técnico, opinião difícil, resumo de algo consumido, hipótese; **nunca o dia a dia** |
| **Verbete do `/ingles:vocab`** | explicação em PT, exemplos em inglês | em inglês, equivalentes em PT no fim | em inglês |

Itens da configuração:

1. **Frequência do monólogo:** diária, N vezes por semana (com os dias fixos) ou sob demanda. Dia fixo
   funciona melhor que "N vezes quando der" (sugestão, não regra). Duração pela tabela.
2. **Modo de correção das mensagens escritas:** no fim (padrão: o `/ingles:fecha` registra e mostra) ou na
   hora (uma linha curta no fim de cada resposta).
3. **Anki:** sim ou não. Sem Anki, o registro fica em `ingles-vocabulario.csv` e a revisão é o `/ingles:vocab revisa`.
   Com Anki, guiar a instalação pelo `${CLAUDE_PLUGIN_ROOT}/referencia/ferramentas.md` §3 agora ou depois.
4. **Whisper:** tem, quer instalar (guiar pelo `${CLAUDE_PLUGIN_ROOT}/referencia/ferramentas.md` §2) ou vai usar a transcrição do celular
   (avisar que vê menos erro).
5. **Livro:** qual edição ele tem, e se o PDF já está em `<pasta>/livros/`. Sugestões por nível em
   `${CLAUDE_PLUGIN_ROOT}/referencia/ferramentas.md` §1.
6. **Conversa semanal** (se tem com quem falar): frequência. Sugerir pedir correção à pessoa, ou
   gravar a conversa **com consentimento dela** e passar pelo `/ingles:monologo`.
7. **Apresentação mensal** (opcional, B1 ou acima): 10-15 min gravados sobre tema técnico ou de
   opinião, mesmo pipeline do monólogo. É onde o vocabulário acaba e o buraco aparece.

---

## Fase 4: Ciclo de temas

Gerar um ciclo de **4 semanas** só pros dias de monólogo que ele escolheu, pra ele nunca ter que
inventar tema na hora.

- **Uma categoria fixa por dia de monólogo**, escolhida pelo **tipo de frase que puxa**:
  | Categoria | Puxa |
  |---|---|
  | Uma história minha | passado simples, *present perfect*, conectores de sequência |
  | Futuro e hipótese | *will*, *going to*, condicionais |
  | Explicar um conceito, como pra um amigo | presente, voz passiva, conectores de causa |
  | Opinião | *I think / I'd argue*, concessão (*although, even if*), modais |
  | Resumir algo que consumiu em inglês | discurso indireto, vocabulário novo da fonte |
  | Interesse dele (trabalho, área, hobby) | vocabulário técnico ativo |
  Com menos dias, juntar categorias; priorizar história, futuro e opinião, que cobrem mais estrutura.
- **Um tema por célula**, tirado dos interesses dele e no nível da tabela da Fase 3. Tema concreto
  ("como funciona um juro composto"), não vago ("economia").
- Dia de viagem ou prova: troca por 2 minutos ou pelo texto escrito, sem pular a correção. Tema pulado
  vai pro próximo ciclo.
- Mostrar o ciclo e deixar ele trocar o que quiser antes de gravar.

---

## Fase 5: Exposição e rotina

**Exposição** (sugestão, ele aceita o que quiser): 2-3 fontes por interesse, no nível dele.

- A1-A2: material feito pra aprendiz (podcasts pra estudantes, *graded readers*, vídeo com legenda
  em inglês).
- B1-B2: conteúdo nativo do interesse dele, com legenda **em inglês**.
- C1+: nativo sem legenda; podcast de **duas pessoas conversando** é melhor pra shadowing que narração
  roteirizada.
- Pra qualquer nível: celular e contas em inglês; **pensar em inglês** (narrar na cabeça o que faz, e
  a palavra que faltar vira `/ingles:vocab`); comunidade de interesse real em inglês (Discord, Reddit de
  um hobby) em vez de servidor de "prática de idioma".

**Shadowing:** clipe de 1-3 min de fala conversacional com transcrição confiável (legenda manual, não
automática). Sequência: entender tudo → ouvir lendo → pausar e repetir frase a frase → falar junto
lendo → falar junto sem texto. Mesmo clipe por alguns dias, até sair fluido.

**Rotina:** montar uma tabela de blocos que caiba no tempo que ele disse ter. Ordem de corte quando
faltar tempo: tópico de gramática sai antes da **leitura em voz alta da correção**. O gargalo de quem
trava é produzir a forma certa em tempo real, não saber a regra.

---

## Fase 6: Gravar e fechar

1. Escrever `<pasta>/ingles-plano.md` inteiro (substituir os marcadores `<!-- ... -->`). §Checkpoint: data
   ~4 semanas à frente, **mesmo tema do monólogo diagnóstico**, pra comparar antes e depois. Segunda
   medida: queda no número de dias por categoria em `ingles-erros.md`.
2. §Agora: primeiro tema do ciclo, primeiro tópico de gramática (trilha sequencial: unit 1 ou a
   apontada pelo diagnóstico; guiada por erro: sai do primeiro monólogo) e o que ficou pendente do
   diagnóstico.
3. Commit só do que o setup tocou, nunca `git add -A` (o repo dele pode ter outras mudanças em
   andamento): `git add "<pasta>" CLAUDE.md .gitignore` (mais a skill de fechamento, se foi editada) e
   `git commit -m "ingles: instala o plugin e monta o plano inicial"`. Pasta sem git e ele recusou o
   `git init`: pular.
4. Resumo em 5 linhas: nível, trilha, frequência, próximo passo concreto ("grave o monólogo de
   amanhã sobre X e diga `/ingles:monologo`").
