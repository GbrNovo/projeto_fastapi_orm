# Projeto em Ciência de Dados II — Sistema Escolar

Sistema de administração escolar com **FastAPI, SQLAlchemy, PostgreSQL e Alembic** no backend e **Streamlit** no frontend. Permite administrar alunos, endereços, disciplinas, notas e a biblioteca (livros, empréstimos e devoluções).

Este guia mostra **como instalar e iniciar o projeto do zero em um computador Windows**, usando o PowerShell. As operações do sistema são feitas pela interface do Streamlit.

## 1. Pré-requisitos

Na máquina em que o sistema será executado, tenha:

- **Git**, para baixar o projeto do GitHub.
- **PostgreSQL**, em execução, e **pgAdmin** (ou outro gerenciador) para criar o banco.
- **uv**, gerenciador dos ambientes e dependências Python: [instruções de instalação](https://docs.astral.sh/uv/getting-started/installation/).
- **Conexão com a internet** na primeira instalação das dependências e para consultas ao ViaCEP.

O Python **3.14** será instalado pelo próprio `uv` se necessário. Abra um **PowerShell novo** depois de instalar o Git e o `uv`, para que seus comandos sejam reconhecidos.

## 2. Baixar o projeto

Abra o PowerShell na pasta onde deseja guardar o projeto e execute:

```powershell
git clone https://github.com/GbrNovo/projeto_fastapi_orm.git
cd projeto_fastapi_orm
```

A pasta baixada possui:

```text
projeto_fastapi_orm/
├── backend/        # API FastAPI, models, services e migrações Alembic
├── frontend/       # Interface Streamlit
└── README.md       # Este guia
```

**Importante:** nos próximos passos, os comandos indicam explicitamente a pasta em que devem ser executados.

## 3. Preparar o backend

No PowerShell, partindo da **raiz do projeto** (`projeto_fastapi_orm`):

```powershell
uv python install 3.14
cd backend
uv venv --python 3.14
uv sync --locked
```

Isso cria o ambiente `backend/.venv` e instala as dependências registradas no projeto. **Não é necessário ativar o `.venv` manualmente**: `uv run` já utiliza o ambiente correto. Evite deixar outro ambiente virtual ativado nesse terminal.

## 4. Criar e configurar o banco PostgreSQL

1. Abra o **pgAdmin** e conecte-se ao servidor PostgreSQL local (ele precisa estar ligado).
2. Em **Databases**, clique com o botão direito e escolha **Create → Database**.
3. Crie um banco vazio chamado **`escola`** (ou outro nome que você escolher). **Não crie tabelas manualmente.**
4. Volte ao PowerShell, **ainda na pasta `backend`**, e crie seu arquivo de configuração:

```powershell
Copy-Item .env.example .env
notepad .env
```

Preencha o arquivo com os dados reais do PostgreSQL desta máquina:

```env
user=postgres
senha=SUA_SENHA_DO_POSTGRES
host=localhost
porta=5432
banco=escola
```

Salve e feche o editor. Se criou um banco com outro nome, substitua `escola`. O `.env` contém sua senha e **não deve ser enviado ao GitHub**.

### Criar as tabelas com Alembic

Ainda na pasta **`backend`**, execute:

```powershell
uv run alembic upgrade head
```

O Alembic cria as tabelas de endereços, alunos, disciplinas, notas, livros e empréstimos em seu banco vazio. **Não precisa executar `alembic revision` nem criar tabelas no pgAdmin.**

## 5. Iniciar o backend — Terminal 1

Na pasta **`backend`**:

```powershell
uv run uvicorn app.main:app --reload
```

Deixe esse terminal aberto. O FastAPI ficará em **`http://127.0.0.1:8000`**.

## 6. Iniciar o frontend — Terminal 2

Abra **outro PowerShell na raiz do projeto**, sem fechar o Terminal 1. Execute:

```powershell
cd frontend
uv venv --python 3.14
uv sync --locked
uv run streamlit run app.py
```

O Streamlit ficará em **http://localhost:8501**. Abra esse endereço no navegador para utilizar o sistema.

**Mantenha os dois terminais abertos:** o Streamlit faz requisições HTTP para o FastAPI em `127.0.0.1:8000`.

| Terminal | Pasta | Processo |
|---|---|---|
| 1 | `backend` | `uv run uvicorn app.main:app --reload` |
| 2 | `frontend` | `uv run streamlit run app.py` |

Para encerrar, pressione **Ctrl+C** em cada terminal.

## 7. Primeiros cadastros no Streamlit

O banco criado na faculdade estará **vazio**. Cadastre os dados fictícios diretamente na interface, nesta ordem:

1. **Endereço:** cadastre um endereço e anote o **ID** gerado.
2. **Alunos:** cadastre um aluno utilizando um endereço existente; anote o ID do aluno.
3. **Disciplinas:** cadastre uma disciplina. Se quiser, vincule uma nota ao aluno e à disciplina existentes.
4. **Biblioteca → Cadastrar livro:** cadastre um livro e consulte a lista para obter seu ID.
5. **Biblioteca → Registrar empréstimo:** selecione um aluno e um livro existentes. Depois, consulte os empréstimos e registre a devolução.

O módulo Biblioteca impede empréstimos para alunos ou livros inexistentes e bloqueia o empréstimo simultâneo do mesmo exemplar.

## 8. Como abrir o projeto novamente

Depois da primeira instalação, **não é necessário recriar os ambientes ou o banco**. Basta iniciar dois PowerShells:

**Terminal 1:**

```powershell
cd CAMINHO_DO_PROJETO\projeto_fastapi_orm\backend
uv run uvicorn app.main:app --reload
```

**Terminal 2:**

```powershell
cd CAMINHO_DO_PROJETO\projeto_fastapi_orm\frontend
uv run streamlit run app.py
```

Abra **http://localhost:8501**. O PostgreSQL também precisa estar em execução.

> **Se aparecer `relation "tb_livros" does not exist` ou outra tabela inexistente:** confirme que o banco e o `.env` estão corretos e, dentro de `backend`, execute `uv run alembic upgrade head`. Se o Streamlit não conseguir carregar os dados, verifique se o Terminal 1 (Uvicorn) continua rodando.
