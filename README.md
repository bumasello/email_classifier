# 🚀 Classificador de E-mails AutoU

Este projeto é uma simulação prática de uma solução para a AutoU, desenvolvida para automatizar a classificação de e-mails e a sugestão de respostas automáticas utilizando Inteligência Artificial. O objetivo é liberar tempo da equipe, eliminando a necessidade de classificação manual de um alto volume de e-mails diários.

## ✨ Funcionalidades

A aplicação web desenvolvida permite:

1.  **Upload de E-mails:** Inserção direta do conteúdo do e-mail via campo de texto ou upload de arquivos nos formatos `.txt` (suporte a `.pdf` planejado).
2.  **Classificação Inteligente:** Categoriza o e-mail em `Produtivo` (requer ação/resposta) ou `Improdutivo` (não requer ação imediata).
3.  **Sugestão de Resposta:** Gera uma resposta automática adequada à categoria identificada do e-mail.
4.  **Interface Intuitiva:** Design minimalista, responsivo, com sombras suaves, cantos arredondados e animações on-hover, seguindo a paleta de cores da AutoU.
5.  **Keep-Alive:** O frontend realiza chamadas periódicas ao backend para evitar o "spin down" do servidor em plataformas de deploy gratuitas, garantindo uma melhor experiência do usuário.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com uma stack moderna e robusta, dividida entre Backend e Frontend:

### Backend

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI
- **Processamento de Linguagem Natural (NLP):** `spaCy` (para pré-processamento de texto em português)
- **Inteligência Artificial:** OpenAI API (ChatGPT)
- **Gerenciamento de Dependências:** `pip`
- **Servidor Web:** `uvicorn`
- **Testes:** `pytest`, `unittest.mock`
- **Variáveis de Ambiente:** `python-dotenv`

### Frontend

- **Runtime & Package Manager:** Bun
- **Build Tool:** Vite
- **Linguagem:** TypeScript
- **Framework UI:** React
- **Estilização:** Tailwind CSS
- **Componentes UI:** Shadcn/ui
- **Validação de Formulário:** `react-hook-form` com `zod`
- **Ícones:** `lucide-react`

## 🚀 Como Rodar Localmente

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

- Python 3.10+ instalado
- Bun instalado (alternativamente, você pode usar `npm` ou `yarn` para o frontend, mas os comandos serão `npm install`, `npm run dev`, etc.)
- Uma chave de API válida do OpenAI com créditos.

### 1. Configuração do Backend

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/bumasello/email_classifier.git
    cd email_classifier
    ```
2.  **Navegue até a pasta do backend:**
    ```bash
    cd backend
    ```
3.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
4.  **Instale as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Crie um arquivo `.env`:**
    Na pasta `backend`, crie um arquivo chamado `.env` e adicione sua chave de API do OpenAI:
    ```
    OPENAI_API_KEY=sua_chave_secreta_do_openai_aqui
    ```
    Substitua `sua_chave_secreta_do_openai_aqui` pela sua chave real.
6.  **Inicie o servidor FastAPI:**
    ```bash
    uvicorn main:app --reload
    ```
    O backend estará rodando em `http://127.0.0.1:8000`. Você pode acessar a documentação interativa em `http://127.0.0.1:8000/docs`.

### 2. Configuração do Frontend

1.  **Navegue de volta para a pasta raiz do projeto e depois para a pasta do frontend:**
    ```bash
    cd ..
    cd frontend
    ```
2.  **Instale as dependências do Bun:**
    ```bash
    bun install
    ```
3.  **Inicie o servidor de desenvolvimento do frontend:**
    ```bash
    bun dev
    ```
    O frontend estará rodando em `http://localhost:5173`.

Agora você pode acessar a aplicação em seu navegador e testar a integração localmente.

## ☁️ Deploy na Nuvem

A aplicação está deployada nas seguintes plataformas:

- **Frontend (Vercel ):** [Link para o Frontend Deployado no Vercel](https://email-classifier-sand-chi.vercel.app/)
- **Backend (Render):** [Link para o Backend Deployado no Render](https://email-classifier-98w2.onrender.com/)

### Considerações sobre o Deploy

- **Vercel (Frontend):** Utilizado pela sua facilidade de deploy de aplicações React/Vite e integração com GitHub.
- **Render (Backend):** Escolhido pela simplicidade de deploy de aplicações Python/FastAPI.
- **Keep-Alive:** Para mitigar o "spin down" do servidor no Render (comum em planos gratuitos por inatividade), o frontend realiza chamadas periódicas (a cada 5 minutos) ao endpoint `/healthcheck` do backend. Isso mantém o serviço "quente" e reduz o tempo de resposta inicial para o usuário.
- **Variáveis de Ambiente:** A `OPENAI_API_KEY` está configurada como variável de ambiente no Render. A URL do backend (`VITE_API_BASE_URL`) é configurada como variável de ambiente no Vercel.
- **CORS:** O backend está configurado para permitir requisições CORS da URL do frontend deployado no Vercel.

## 🎥 Vídeo Demonstrativo

Assista ao vídeo abaixo para uma demonstração rápida da aplicação e uma breve explicação técnica:

## 💡 Decisões de Design e Arquitetura

- **Arquitetura Modular (Backend):** O backend segue uma estrutura MVC-like com Services, separando as responsabilidades de roteamento (controllers/routers), lógica de negócio (services) e integração com APIs externas (OpenAIService, NLPService). Isso promove a manutenibilidade, testabilidade e escalabilidade.
- **Injeção de Dependência (FastAPI):** Utilizada para gerenciar as dependências dos serviços nos endpoints da API, facilitando o mocking em testes e a flexibilidade.
- **Testes Abrangentes:** Testes unitários para os serviços e testes de integração para os endpoints da API garantem a robustez e a confiabilidade da solução. A preocupação com a tipagem estrita (TypeScript no frontend, type hints no Python) e a cobertura de testes foi uma prioridade.
- **Frontend Moderno:** A escolha de Bun, Vite, React, TypeScript, Tailwind CSS e Shadcn/ui oferece uma experiência de desenvolvimento ágil, performance otimizada e uma interface de usuário moderna e responsiva.
- **Design Minimalista:** A paleta de cores da AutoU foi cuidadosamente aplicada para criar uma interface limpa, com bom contraste e hierarquia visual, utilizando sombras e cantos arredondados para um toque suave e profissional.
- **Tratamento de Erros:** Implementação de feedback visual para o usuário em caso de erros na comunicação com o backend ou validação de formulário.

## 🔮 Melhorias Futuras

- **Leitura de PDF:** Implementar a extração de texto de arquivos PDF no backend.
- **Modelos de IA Customizados:** Explorar o fine-tuning de modelos de linguagem para classificações e respostas mais específicas ao domínio da AutoU.
- **Histórico de E-mails:** Adicionar funcionalidade para armazenar e visualizar e-mails processados e suas classificações.
- **Autenticação de Usuários:** Implementar um sistema de login para acesso restrito.
- **Feedback do Usuário:** Permitir que os usuários avaliem a classificação e a resposta sugerida para melhorar o modelo.

---

Agradeço a oportunidade de participar deste processo seletivo e espero que esta solução demonstre minhas habilidades em resolver problemas complexos com tecnologia.

Atenciosamente,

Bruno Masello
