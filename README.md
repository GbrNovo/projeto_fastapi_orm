# Projeto em Ciência de Dados II — Sistema Escolar

Sistema escolar com **FastAPI, SQLAlchemy, PostgreSQL e Alembic** no backend e **Streamlit** no frontend. Gerencia endereços, alunos, disciplinas, notas e biblioteca (livros, empréstimos e devoluções).

Este guia prepara o projeto **do zero na máquina da faculdade (Windows/PowerShell)** e mostra como demonstrar as operações disponíveis pelo **Postman**. O Streamlit também pode ser aberto para mostrar a interface.

> **Diferença importante:** o **Alembic cria/atualiza as tabelas** do banco. **Cadastrar, consultar, atualizar e excluir registros** são operações HTTP executadas no Postman (ou no Streamlit), não comandos do Alembic.

## 1. Instalação na máquina da faculdade

### Pré-requisitos

- Git;
- PostgreSQL em execução e pgAdmin (ou outro gerenciador) para criar o banco;
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/), com internet para instalar as dependências;
- Postman (para realizar as requisições HTTP);
- Internet para consultas opcionais ao ViaCEP.

O `uv` pode instalar o Python 3.14. Depois de instalar Git e `uv`, abra um PowerShell novo.

### 1.1. Clonar o repositório

No PowerShell, a partir da pasta onde deseja salvar o projeto:

```powershell
git clone https://github.com/GbrNovo/projeto_fastapi_orm.git
cd projeto_fastapi_orm
```

Estrutura principal:

```text
projeto_fastapi_orm/
├── backend/       # FastAPI, Models, Routers, Services e Alembic
├── frontend/      # Streamlit
└── README.md
```

### 1.2. Instalar as dependências do backend

**Na raiz do projeto:**

```powershell
uv python install 3.14
cd backend
uv venv --python 3.14
uv sync --locked
```

O ambiente do backend ficará em `backend/.venv`. Não é necessário ativá-lo: `uv run` usa o ambiente correto. Se outro `.venv` estiver ativado, execute `deactivate` antes para evitar avisos.

### 1.3. Criar o banco PostgreSQL e configurar o `.env`

1. Inicie o PostgreSQL e abra o pgAdmin.
2. Em **Databases → Create → Database**, crie um banco **vazio** chamado `escola` (ou use outro nome).
3. **Ainda na pasta `backend`** do PowerShell, execute:

```powershell
Copy-Item .env.example .env
notepad .env
```

Preencha o `.env` com os dados reais **desta máquina**:

```dotenv
user=postgres
senha=SUA_SENHA_DO_POSTGRES
host=localhost
porta=5432
banco=escola
```

Salve o arquivo. **Não compartilhe nem envie `.env` para o GitHub.**

### 1.4. Criar as tabelas com Alembic

**Na pasta `backend`:**

```powershell
uv run alembic upgrade head
```

Isso aplica as migrações existentes e cria as tabelas `tb_enderecos`, `tb_alunos`, `tb_disciplinas`, `tb_notas`, `tb_livros` e `tb_emprestimos` no banco vazio.

Para conferir a versão aplicada:

```powershell
uv run alembic current
```

Na versão atual, o esperado é **`b1b11017c026 (head)`**. **Não execute `alembic revision --autogenerate` e não crie as tabelas manualmente.**

### 1.5. Ligar o backend — Terminal 1

**Na pasta `backend`:**

```powershell
uv run uvicorn app.main:app --reload
```

Mantenha o terminal aberto. API: **http://127.0.0.1:8000**.

### 1.6. Ligar o Streamlit — Terminal 2 (opcional para a apresentação)

Abra outro PowerShell na **raiz do projeto** e execute:

```powershell
cd frontend
uv venv --python 3.14
uv sync --locked
uv run streamlit run app.py
```

Interface: **http://localhost:8501**. Mantenha os dois terminais abertos. Para encerrar, use **Ctrl+C** em cada um.

## 2. Configurar o Postman

1. Com o Uvicorn executando na porta 8000, abra o Postman.
2. Crie uma requisição (**New → HTTP Request**).
3. Escolha o método **GET, POST, PUT ou DELETE**, conforme a operação.
4. Insira a URL iniciando com `http://127.0.0.1:8000`.
5. Para **POST** e **PUT** com dados: **Body → raw → JSON** e cole o JSON indicado. Confirme o cabeçalho `Content-Type: application/json`.
6. Clique em **Send** e confira a resposta. Reutilize a mesma requisição mudando método, URL e corpo.

**Atenção aos IDs:** `1` nos exemplos é ilustrativo. Após cadastrar, faça uma consulta `GET` para encontrar o ID real. Os IDs são gerados pelo PostgreSQL e não precisam começar em 1.

## 3. Endereços — todas as operações disponíveis

Recomendação: cadastre o endereço **antes** do aluno. O aluno precisa de `endereco_id` válido.

### 3.1. Cadastrar endereço (POST)

```http
POST http://127.0.0.1:8000/enderecos/criar-endereco
```

**Body → raw → JSON:**

```json
{
  "cep": "01001000",
  "endereco": "Praca da Se",
  "bairro": "Se",
  "cidade": "Sao Paulo",
  "estado": "SP",
  "regiao": "Sudeste"
}
```

O CEP precisa ser único na tabela. Você também pode usar a integração externa:

```http
GET http://127.0.0.1:8000/enderecos/consultar-cep/01001000
POST http://127.0.0.1:8000/enderecos/criar-endereco-por-cep/01001000
```

Para o `POST` por CEP, **não envie body**: a API consulta o ViaCEP e cadastra o endereço, retornando seu ID. Necessita internet. Se o CEP já estiver cadastrado, retorna o ID existente.

### 3.2. Consultar todos (GET)

```http
GET http://127.0.0.1:8000/enderecos/pegar-dados-endereco
```

### 3.3. Atualizar endereço (PUT)

```http
PUT http://127.0.0.1:8000/enderecos/atualizar-endereco/1
```

**Body:**

```json
{
  "bairro": "Centro"
}
```

Troque `1` pelo ID real. O schema permite enviar apenas os campos que quer atualizar.

### 3.4. Excluir endereço (DELETE)

```http
DELETE http://127.0.0.1:8000/enderecos/deletar-endereco/1
```

Envie **sem body**. Se houver alunos referenciando o endereço, o PostgreSQL poderá impedir a exclusão pela chave estrangeira. Exclua primeiro os registros dependentes.

## 4. Alunos — todas as operações disponíveis

### 4.1. Cadastrar aluno (POST)

```http
POST http://127.0.0.1:8000/alunos/criar-aluno
```

**Body:**

```json
{
  "matricula": "20260001",
  "nome_aluno": "Maria Silva",
  "email": "maria@example.com",
  "endereco_id": 1
}
```

Use um `endereco_id` que exista. A matrícula deve ser única.

### 4.2. Consultar todos (GET)

```http
GET http://127.0.0.1:8000/alunos/pegar-dados-aluno
```

### 4.3. Consultar por ID (GET)

```http
GET http://127.0.0.1:8000/alunos/pegar-dados-aluno-por-id/1
```

### 4.4. Atualizar aluno (PUT)

```http
PUT http://127.0.0.1:8000/alunos/atualizar-aluno/1
```

**Body:**

```json
{
  "nome_aluno": "Maria Oliveira",
  "email": "maria.oliveira@example.com"
}
```

### 4.5. Excluir aluno (DELETE)

```http
DELETE http://127.0.0.1:8000/alunos/deletar-aluno/1
```

Envie sem body. Se o aluno possuir notas ou empréstimos vinculados, a chave estrangeira pode impedir a exclusão. Verifique isso antes de excluir.

## 5. Disciplinas — todas as operações disponíveis

### 5.1. Cadastrar disciplina (POST)

```http
POST http://127.0.0.1:8000/disciplinas/criar-disciplina
```

**Body:**

```json
{
  "nome_disciplina": "Matematica",
  "carga": 60,
  "semestre": 2
}
```

### 5.2. Consultar todas (GET)

```http
GET http://127.0.0.1:8000/disciplinas/pegar-dados-disciplina
```

### 5.3. Consultar por ID (GET)

```http
GET http://127.0.0.1:8000/disciplinas/pegar-dados-disciplina-por-id/1
```

### 5.4. Atualizar disciplina (PUT)

```http
PUT http://127.0.0.1:8000/disciplinas/atualizar-disciplina/1
```

**Body:**

```json
{
  "carga": 80,
  "semestre": 3
}
```

### 5.5. Excluir disciplina (DELETE)

```http
DELETE http://127.0.0.1:8000/disciplinas/deletar-disciplina/1
```

Envie sem body. Se houver notas referenciando essa disciplina, exclua primeiro as notas de teste.

## 6. Notas — todas as operações disponíveis

Cadastre uma nota **somente depois de existirem um aluno e uma disciplina**.

### 6.1. Cadastrar nota (POST)

```http
POST http://127.0.0.1:8000/notas/criar-nota
```

**Body:**

```json
{
  "aluno_id": 1,
  "disciplina_id": 1,
  "nota": 8.5
}
```

### 6.2. Consultar todas (GET)

```http
GET http://127.0.0.1:8000/notas/pegar-dados-nota
```

### 6.3. Consultar por ID (GET)

```http
GET http://127.0.0.1:8000/notas/pegar-dados-nota-por-id/1
```

### 6.4. Atualizar nota (PUT)

```http
PUT http://127.0.0.1:8000/notas/atualizar-nota/1
```

**Body:**

```json
{
  "nota": 9.5
}
```

### 6.5. Excluir nota (DELETE)

```http
DELETE http://127.0.0.1:8000/notas/deletar-nota/1
```

Envie sem body. Para confirmar, faça novamente a consulta de todas as notas.

## 7. Biblioteca — Livros

**Nesta versão existem apenas rotas de cadastro e consulta de livros.** Atualizar e excluir livros **não são endpoints implementados** no projeto atual; não tente simular essas operações com URLs inventadas.

### 7.1. Cadastrar livro (POST)

```http
POST http://127.0.0.1:8000/livros/criar-livro
```

**Body:**

```json
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "isbn": "9788535914849"
}
```

O ISBN é opcional. A resposta inclui o `id` gerado.

### 7.2. Consultar todos os livros (GET)

```http
GET http://127.0.0.1:8000/livros/pegar-dados-livro
```

### 7.3. Consultar livro por ID (GET)

```http
GET http://127.0.0.1:8000/livros/pegar-dados-livro-por-id/1
```

Se o livro não existir, o endpoint retorna **404**.

## 8. Biblioteca — Empréstimos e devoluções

**Nesta versão existem rotas para criar empréstimo, consultar empréstimos e registrar devolução.** Não há endpoint para editar ou excluir um empréstimo. A devolução é uma atualização específica por `PUT`.

### 8.1. Registrar empréstimo (POST)

```http
POST http://127.0.0.1:8000/emprestimos/criar-emprestimo
```

**Body:**

```json
{
  "aluno_id": 1,
  "livro_id": 1
}
```

Use IDs existentes. Respostas de validação:

- **404 — Aluno não encontrado:** `aluno_id` inexistente;
- **404 — Livro não encontrado:** `livro_id` inexistente;
- **409 — Este livro já está emprestado:** há um empréstimo ativo para o mesmo livro.

O cadastro válido responde com mensagem e `id` do empréstimo.

### 8.2. Consultar empréstimos (GET)

```http
GET http://127.0.0.1:8000/emprestimos/pegar-dados-emprestimo
```

A resposta inclui ID, aluno, livro, datas e status do empréstimo.

### 8.3. Registrar devolução (PUT)

```http
PUT http://127.0.0.1:8000/emprestimos/devolver-livro/1
```

**Sem body.** O ID da URL é o **ID do empréstimo**, não o ID do livro. A operação atualiza a data de devolução e o status para `Devolvido`.

Se o empréstimo não existir, retorna **404**; se já tiver sido devolvido, retorna **409**. Após devolver, o mesmo livro poderá ser emprestado novamente.

## 9. Roteiro rápido para demonstrar ao professor

1. Abra o Postman e mostre `GET /enderecos/pegar-dados-endereco` (banco inicialmente vazio).
2. Cadastre um endereço e use `GET` para identificar seu ID.
3. Cadastre um aluno com esse `endereco_id`; consulte, atualize e consulte novamente.
4. Cadastre uma disciplina; consulte, atualize e consulte novamente.
5. Cadastre uma nota vinculada ao aluno e à disciplina; consulte, atualize e consulte novamente.
6. Cadastre um livro; consulte-o e anote seu ID.
7. Registre um empréstimo usando o ID do aluno e do livro; consulte o histórico.
8. Tente emprestar o mesmo livro novamente: deverá retornar **409**.
9. Teste empréstimo com ID de aluno e depois ID de livro inexistentes: deverá retornar **404**.
10. Registre a devolução usando o ID do **empréstimo**, consulte o histórico e empreste o livro novamente se quiser.
11. Para demonstrar `DELETE`, exclua **primeiro a nota**, depois uma disciplina ou um aluno **que não possuam outras referências**. Faça uma consulta `GET` após cada exclusão. Evite tentar apagar um aluno que tenha empréstimos registrados.

**Observações:** o banco estará vazio após `alembic upgrade head` numa instalação nova. Os endpoints antigos de atualização/exclusão (especialmente Alunos, Disciplinas, Notas e Endereços) nem sempre retornam erro HTTP adequado para IDs inexistentes; confira o resultado com `GET`. Se surgir erro de chave estrangeira, verifique quais registros dependem daquele ID. Não é necessário modificar o banco manualmente no pgAdmin para esta demonstração.

## 10. Abrir o projeto novamente

Depois da primeira instalação, não recrie os ambientes, o banco nem as migrações. Basta iniciar o PostgreSQL e abrir dois PowerShells:

**Terminal 1 — backend:**

```powershell
cd CAMINHO_DO_PROJETO\projeto_fastapi_orm\backend
uv run uvicorn app.main:app --reload
```

**Terminal 2 — frontend (se quiser apresentar a interface):**

```powershell
cd CAMINHO_DO_PROJETO\projeto_fastapi_orm\frontend
uv run streamlit run app.py
```

Para Postman, é suficiente manter o **Terminal 1** aberto e acessar `http://127.0.0.1:8000` nas requisições.

> **Erro `relation "tb_livros" does not exist` ou semelhante:** confira se o `.env` aponta para o banco correto e execute `uv run alembic upgrade head` na pasta `backend`. Erros HTTP 500 ou de conexão exigem conferir o terminal Uvicorn.
