# 🎬 Gerador de Legendas com IA

Gere legendas no formato **SRT** a partir de vídeos utilizando reconhecimento de voz e correção de texto com inteligência artificial, executados localmente.

O projeto combina o **OpenAI Whisper** para transcrever o áudio em português e o **Ollama com Llama 3** para corrigir possíveis erros de reconhecimento, fonética e gramática. Ao final, o sistema gera um arquivo `.srt` pronto para ser utilizado em editores de vídeo e players compatíveis.

## ✨ Funcionalidades

- 🎙️ **Transcrição automática:** converte o áudio do vídeo em texto usando o Whisper.
- 🇧🇷 **Português do Brasil:** configura o reconhecimento de voz para o idioma português.
- 🧠 **Correção com IA local:** utiliza o Llama 3 por meio do Ollama para corrigir erros de transcrição.
- 📝 **Geração de legendas SRT:** cria automaticamente um arquivo de legenda com numeração e timestamps.
- 📏 **Controle do tamanho das linhas:** divide o texto em trechos curtos para facilitar a leitura.
- 💻 **Processamento local:** utiliza modelos instalados na própria máquina, sem depender de APIs externas para a transcrição e correção.
- 🛡️ **Tratamento de falhas:** caso a correção pelo Ollama falhe em um trecho, o sistema utiliza o texto original reconhecido pelo Whisper.
- 📂 **Saída automática:** salva o arquivo `.srt` no mesmo diretório e com o mesmo nome-base do vídeo.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal do projeto |
| OpenAI Whisper | Reconhecimento de voz e transcrição |
| Ollama | Execução local de modelos de linguagem |
| Llama 3 | Correção textual dos trechos transcritos |
| SRT | Formato de saída das legendas |

## ⚙️ Pré-requisitos

Antes de executar o projeto, instale:

- Python 3.10 ou outra versão compatível com as dependências utilizadas.
- [FFmpeg](https://ffmpeg.org/download.html), necessário para o processamento de áudio pelo Whisper.
- [Ollama](https://ollama.com/download), para executar o modelo de linguagem localmente.
- Git, caso queira clonar o repositório.

**Hardware:** o desempenho depende do processador, da memória RAM e, quando disponível, da GPU. O primeiro carregamento dos modelos pode levar algum tempo.

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
```

Entre na pasta do projeto:

```bash
cd SEU-REPOSITORIO
```

Substitua o endereço acima pelo endereço real do seu repositório no GitHub.

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
.venv\Scripts\activate
```

No Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
python -m pip install --upgrade pip
pip install openai-whisper ollama
```

O pacote Python `ollama` é o cliente utilizado pelo script. Ele não substitui a instalação do aplicativo Ollama.

### 4. Instale e prepare o Ollama

Baixe e instale o Ollama pelo site oficial:

https://ollama.com/download

Em seguida, baixe o modelo utilizado pelo projeto:

```bash
ollama pull llama3
```

Certifique-se de que o Ollama esteja em execução antes de iniciar a geração das legendas.

## ▶️ Como utilizar

Execute o script informando o caminho do vídeo como argumento:

```bash
python gerar_legenda_global.py video.mp4
```

Também é possível informar um caminho completo:

```bash
python gerar_legenda_global.py "C:\Videos\partida.mp4"
```

No Linux:

```bash
python gerar_legenda_global.py "/home/usuario/Videos/partida.mp4"
```

### Exemplo de execução

```text
Carregando o modelo Whisper local para o vídeo: video.mp4...
Realizando a transcrição bruta...
Processando e corrigindo trechos com o Ollama local...
Sucesso! Legenda perfeita gerada em: video.srt
```

As mensagens acima representam o fluxo esperado de execução; o tempo de processamento e o resultado dependem do vídeo e do hardware.

## 📄 Arquivo gerado

Se o vídeo de entrada for:

```text
video.mp4
```

O sistema criará:

```text
video.srt
```

O conteúdo segue a estrutura padrão do formato SRT:

```srt
1
00:00:01,000 --> 00:00:02,500
Texto inicial da legenda

2
00:00:02,500 --> 00:00:04,000
Continuação da fala
```

Cada legenda possui um número sequencial, um intervalo de tempo e o texto correspondente.

## 🔍 Como funciona

O processamento segue estas etapas:

1. **Validação do arquivo:** verifica se o caminho informado existe.
2. **Carregamento do Whisper:** utiliza o modelo `base` para reconhecer a fala do vídeo.
3. **Transcrição:** extrai os segmentos de texto com seus tempos iniciais e finais.
4. **Correção textual:** envia cada segmento ao Llama 3 para tentar corrigir erros fonéticos e gramaticais, preservando o sentido informal.
5. **Divisão do texto:** separa o conteúdo corrigido em linhas de até 28 caracteres.
6. **Distribuição temporal:** divide o intervalo original do segmento entre os trechos criados.
7. **Exportação:** salva todas as legendas em um arquivo `.srt`, utilizando codificação UTF-8.

## ⚠️ Limitações conhecidas

- A correção com IA não garante uma transcrição perfeita e pode alterar palavras ou o sentido original.
- A divisão do tempo entre as linhas é proporcional, não baseada no instante exato de cada palavra.
- Linhas curtas podem melhorar a leitura, mas a divisão de um segmento em vários trechos pode produzir tempos de exibição pouco naturais.
- O modelo `base` oferece um equilíbrio entre desempenho e velocidade, mas pode apresentar dificuldades com ruído, falas sobrepostas, sotaques e termos específicos.
- O Ollama precisa estar instalado e disponível para realizar as correções. Se ocorrer uma falha durante uma chamada, o script mantém o texto original daquele segmento.
- A primeira execução pode exigir o download dos modelos e consumir mais tempo.

**Importante:** revise o arquivo SRT antes de utilizá-lo em uma publicação, transmissão ou edição profissional.

## 🔒 Privacidade

A transcrição e a correção são realizadas com modelos locais. O script não utiliza serviços externos de transcrição por API, embora o Ollama precise estar disponível na máquina.

Os vídeos e textos processados não são enviados automaticamente para serviços de nuvem pelo fluxo apresentado. O comportamento de privacidade também depende do ambiente e das configurações locais.

## 📌 Melhorias futuras

- Sincronização mais precisa das legendas com a fala.
- Ajuste automático do tempo mínimo e máximo de exibição.
- Configuração do tamanho máximo das linhas.
- Suporte a diferentes modelos do Whisper.
- Interface gráfica para selecionar vídeos sem utilizar o terminal.
- Processamento de vários vídeos em lote.
- Opção para revisar e editar as legendas antes de exportar.

## 👨‍💻 Autor

**Arthur Luiz da Silva Oliveira**

Projeto desenvolvido para automatizar a criação e a correção de legendas utilizando ferramentas de inteligência artificial executadas localmente.

## 📜 Licença

Defina uma licença antes de distribuir o projeto publicamente. Caso escolha a licença MIT, adicione um arquivo `LICENSE` com o texto correspondente e confirme que ela é adequada para o código e suas dependências.

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório!
