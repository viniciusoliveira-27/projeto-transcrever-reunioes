# 🧠🎙️ Transcrição Inteligente de Reuniões com IA

## 1. 📌 Descrição

Este projeto em Python utiliza Inteligência Artificial para **gravar conversas**, **transcrevê-las em tempo real** e **gerar resumos automáticos**, ideal para reuniões, aulas ou qualquer outro contexto que envolva áudio. A interface foi desenvolvida com **Streamlit**, proporcionando uma experiência simples e direta para o usuário. A aplicação utiliza a **API da OpenAI** para realizar a transcrição e sumarização com alta precisão.

---

## 2. 🚀 Funcionalidades

- 🎙️ Gravação de áudio em tempo real via navegador.
- ✍️ Transcrição automática utilizando modelos da OpenAI.
- 📄 Geração de resumo do conteúdo falado.
- 🧼 Interface leve, simples e intuitiva com Streamlit.
- 🔐 Gerenciamento de chave de API via `.env`.

---

## 3. 🛠️ Tecnologias Utilizadas

| Tecnologia           | Finalidade                                       |
|----------------------|--------------------------------------------------|
| **Python**           | Linguagem principal do projeto                   |
| **Streamlit**        | Interface web interativa e leve                  |
| **streamlit-webrtc** | Captura de áudio pelo navegador                  |
| **OpenAI**           | Transcrição e resumo com modelos de IA           |
| **pydub**            | Manipulação de arquivos de áudio (conversões)    |
| **python-dotenv**    | Carregamento de variáveis de ambiente            |
| **ipykernel**        | Suporte a notebooks interativos (Jupyter, VSCode)|

---

## 4. ⚙️ Requisitos

Antes de iniciar, certifique-se de ter as seguintes ferramentas instaladas:

- Python 3.8 ou superior
- [Node.js](https://nodejs.org/) (necessário para Streamlit WebRTC)
- `ffmpeg` instalado e acessível no PATH do sistema

---

## 5. 🚧 Instalação e Execução

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows 

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
    ```bash
    OPENAI_API_KEY=sua-chave-aqui

5. Execute a aplicação:
    ```bash
    streamlit run app.py


## 6. 🧪 Estrutura do Projeto

```plaintext
transcricao-reunioes/
├── app.py               # Arquivo principal da aplicação Streamlit
├── requirements.txt     # Dependências do projeto
├── .env                 # Chave da API (não subir no GitHub!)
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo

```

## 7. 🧠 Créditos

Projeto desenvolvido por Vinícius Ribeiro de Oliveira seguindo o curso da Asimov academy com o propósito de facilitar a captura, transcrição e entendimento de reuniões / conversas, para facilitar meus estudos utilizando IA.



