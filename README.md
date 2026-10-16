# ingles-kit

Um plugin do Claude Code que transforma o agente num professor de inglês **com memória**. Você grava
monólogos e conversa com ele; o agente corrige tudo, conta cada erro por categoria e usa essa contagem
pra decidir o que você estuda em seguida. Feito pra quem fala português.

> **Versão de teste (out/2026).** O método está rodando com quem montou o kit e ainda não passou pelo
> primeiro checkpoint. Se algo não fizer sentido pra você, me avise.

---

## Instalar

Dentro do Claude Code:

```
/plugin marketplace add magutolou/ingles-kit
/plugin install ingles@ingles-kit
```

Depois, **abra o Claude Code na pasta onde você quer guardar seu inglês** (seu segundo cérebro, um repo
qualquer ou uma pasta nova) e rode:

```
/ingles:setup
```

O agente olha a pasta, propõe onde guardar os dados e encaixa o inglês no que você já tem, sem
sobrescrever nada. Depois ele pergunta uma coisa por vez, pede um teste de nível (EF SET, grátis) e
uma amostra sua falando, e monta o plano. São uns 20 minutos, sem contar o teste.

Se a instalação reclamar de SSH, rode isto no terminal antes de abrir o Claude Code e tente de novo:

```bash
export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1
```

(No PowerShell: `$env:CLAUDE_CODE_PLUGIN_PREFER_HTTPS = "1"`.)

---

## Onde ficam as coisas

O plugin traz só o **comportamento** (as skills). **Seus dados ficam no seu repo**, numa pasta que o
setup cria com você:

| Onde | O quê |
|---|---|
| Plugin (instalado pelo Claude Code, fora do seu repo) | as 5 skills, os modelos de arquivo, o guia de ferramentas |
| `<sua pasta>/` (ex.: `memory/projects/ingles/` num segundo cérebro) | plano, erros recorrentes, monólogos, quiz, vocabulário |
| Seu `CLAUDE.md` | um bloco curto, entre marcadores `ingles-kit`, dizendo onde está a pasta |
| Seu `.gitignore` | 2 linhas que deixam áudio e livros fora do git |

Se você já tem uma rotina de fim de sessão (tipo `/flush`), o setup oferece encaixar o inglês nela,
pra você não ter duas rotinas de fechamento.

---

## O método em uma página

**Loop:** produzir → ser corrigido → fixar → produzir de novo.

1. **Monólogo gravado**, na frequência que você escolher (todo dia, 3x por semana, sob demanda), sobre
   um tema de um ciclo de 4 semanas montado com os seus interesses. O agente transcreve num modo que
   preserva os erros, corrige frase por frase e devolve uma versão pra você **ler em voz alta**. A
   leitura é o passo principal.
2. **Suas mensagens em inglês no chat** também são corrigidas e entram na mesma contagem.
3. **Gramática pelos seus erros.** O que se repete em vários dias vira o próximo tópico. O agente lê a
   unit do livro e ensina passo a passo, com checagem a cada passo e um quiz no fim. No nível inicial,
   a trilha segue a ordem do livro.
4. **Vocabulário.** O `/ingles:vocab` é um dicionário no chat. As palavras pesquisadas viram cards com
   frases escritas **por você**, com Anki ou sem.
5. **Exposição.** Sugestões de conteúdo pelo seu nível e pelos seus interesses, shadowing e ambiente em
   inglês. Você escolhe o que aceitar.

O que diferencia isto de pedir correção pro ChatGPT é o arquivo `ingles-erros.md`, que guarda a contagem de
uma correção pra outra.

---

## Skills

| Comando | Quando |
|---|---|
| `/ingles:setup` | uma vez por pasta, e pra reconfigurar (nível, frequência) |
| `/ingles:monologo` | depois de gravar: "corrige o de hoje" |
| `/ingles:gramatica` | sessão de gramática |
| `/ingles:vocab <palavra>` | dúvida de vocabulário; `cards` monta os cards; `revisa` revisa |
| `/ingles:fecha` | **fim de toda sessão**, antes de limpar a conversa (se o inglês não está no seu `/flush`) |

Você também pode pedir em português ("corrige o monólogo de hoje", "aula de gramática").

---

## Ferramentas opcionais

Whisper (transcrição local do áudio), Anki (cards) e livros de gramática. O setup oferece, e o agente
guia a instalação; você não precisa fazer nada sozinho. Os livros cada um consegue por conta própria.
Detalhes em [`plugins/ingles/referencia/ferramentas.md`](plugins/ingles/referencia/ferramentas.md).

---

## Atualizar

Pra puxar a versão mais nova do kit, no terminal (PowerShell ou bash), **fora** do Claude Code:

```bash
claude plugin marketplace update ingles-kit
claude plugin update ingles@ingles-kit
```

São os dois: o primeiro baixa o kit novo, o segundo troca o plugin instalado. Só o primeiro não muda
nada. Depois **feche e abra o Claude Code**. Pra conferir, `claude plugin list` mostra a versão
instalada, que é o começo do último commit deste repo.

Seus dados não são tocados: eles estão no seu repo, não no plugin.

---

*Montado a partir do workflow de inglês do Maguto ([github.com/magutolou](https://github.com/magutolou)).*
