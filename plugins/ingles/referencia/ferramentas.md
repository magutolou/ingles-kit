# Ferramentas opcionais

Instalação dos recursos que o método usa. **O aluno não instala nada sozinho:** o agente lê esta página
e conduz, rodando os comandos com ele (`/ingles:setup` oferece; ou o aluno pede "me ajuda a instalar
o Whisper"). `<pasta>` é a pasta do inglês, definida no bloco `ingles-kit` do `CLAUDE.md`.

---

## 1. Livros de gramática (recomendado)

A gramática do método sai de um livro-texto. O agente lê a unit e ensina passo a passo; o aluno não
precisa ler o livro. Sem livro, o agente ensina pelo próprio conhecimento, mas perde a ordem e a
terminologia de uma referência só.

| Nível | Livro | Papel |
|---|---|---|
| A1-A2 | *Essential Grammar in Use*, Raymond Murphy (Cambridge) | livro-texto, seguido em ordem |
| B1-B2 (e C1 com fala travada) | *English Grammar in Use*, Raymond Murphy (Cambridge), 5ª ed. | livro-texto; tem um teste diagnóstico (*Study guide*) que aponta as units |
| C1-C2 | *Advanced Grammar in Use*, Martin Hewings (Cambridge) | opcional, se o *English Grammar in Use* ficar fácil |
| todos | *Practical English Usage*, Michael Swan (Oxford) | consulta pra caso de borda, não se lê em sequência |

Edição **with answers** (tem gabarito) e PDF com **texto selecionável**: PDF escaneado como imagem o
agente não lê direito. O arquivo vai em `<pasta>/livros/`, que fica fora do git.

O aluno consegue os livros por conta própria; o plugin não traz nenhum.

---

## 2. Whisper: transcrição de áudio (recomendado pro monólogo)

O Whisper (da OpenAI) roda **no computador do aluno**, de graça e sem mandar o áudio pra lugar nenhum.

### 2a. ffmpeg (o Whisper precisa dele pra ler o áudio)

- **Windows:** `winget install Gyan.FFmpeg`, depois fechar e reabrir o terminal.
- **Mac:** `brew install ffmpeg` (precisa do [Homebrew](https://brew.sh)).
- **Linux:** `sudo apt install ffmpeg`.

Conferir com `ffmpeg -version`.

### 2b. Whisper

Precisa de Python 3.9 ou mais novo (`python --version`; sem Python, baixar em python.org e marcar
"Add Python to PATH" no instalador do Windows).

```bash
pip install -U openai-whisper
```

Teste com um áudio curto em inglês:

```bash
whisper teste.m4a --model small --language en
```

A primeira execução baixa o modelo `small` (uns 460 MB). Roda em CPU; com GPU NVIDIA fica bem mais
rápido. O modo que preserva erro está no `/ingles:monologo`.

### 2c. Sem Whisper

O gravador do celular costuma transcrever sozinho (iPhone e Pixel fazem isso). O aluno cola o texto e
o `/ingles:monologo` segue dali. **Funciona pior:** transcritor comum "limpa" ainda mais a fala (some
artigo, some `-s`, conserta o tempo verbal), e o agente vê menos erro do que houve.

### Gravar

Qualquer gravador de celular. O arquivo vai pra `<pasta>/audio/` com a data no nome
(`2026-10-16.m4a`). A pasta fica fora do git.

---

## 3. Anki: cards de vocabulário (opcional)

Sem Anki, o `/ingles:vocab` guarda tudo em `<pasta>/ingles-vocabulario.csv` e a revisão é o
`/ingles:vocab revisa`. Com Anki, o mesmo CSV vira um deck com repetição espaçada, que é o que o Anki
faz melhor que qualquer revisão no chat.

1. Instalar o **Anki** desktop: [apps.ankiweb.net](https://apps.ankiweb.net).
2. No Anki: *Tools → Add-ons → Get Add-ons*, código **`2055492159`** (AnkiConnect). Reiniciar o Anki.
   É o que deixa o agente criar os cards direto.
3. (Opcional) Conta no AnkiWeb e **AnkiDroid** (Android, grátis) ou AnkiMobile (iOS, pago) pra revisar
   no celular.
4. Em `<pasta>/ingles-plano.md` §Configuração, `Anki: sim`. O `/ingles:vocab cards` passa a empurrar os cards
   (o Anki precisa estar aberto).

**Sem o AnkiConnect** também dá: no Anki, *File → Import* e escolher o `ingles-vocabulario.csv`. O arquivo já
está no formato que o Anki importa.
