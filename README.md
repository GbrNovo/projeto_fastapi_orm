# Guia de Configuração e Execução do Projeto (FastAPI + SQLAlchemy + Alembic + Streamlit)

Guia completo para **montar o banco PostgreSQL, executar o backend FastAPI, abrir o frontend Streamlit e testar todos os módulos**, incluindo a nova Biblioteca. As instruções foram escritas para reconstruir o projeto em outro computador, como na avaliação da faculdade.

> **Atenção:** execute os comandos no terminal e na pasta indicados. Backend e frontend têm ambientes virtuais separados. Não é necessário instalar ou abrir o Postman para usar o sistema; o Streamlit faz as requisições HTTP.

## 1. Clonar e Preparar o Ambiente

### Pré-requisitos na máquina da faculdade

- **PostgreSQL** instalado e em execução, com acesso ao `pgAdmin`, DBeaver ou ferramenta equivalente para criar um banco de dados.
- **uv** instalado e disponível no terminal. Instalação: <https://docs.astral.sh/uv/getting-started/installation/>.
- **Python 3.14**, usado nos arquivos `.python-version` dos dois projetos. O próprio `uv` pode instalá-lo, caso haja acesso à internet.
- A pasta extraída com `backend/` e `frontend/`, incluindo os dois arquivos `uv.lock` e todo o histórico de `backend/alembic/versions/`.
- Acesso à internet na **primeira instalação** para baixar dependências, caso ainda não estejam no cache. A busca pelo ViaCEP também depende de internet.

Abra o **PowerShell** (Windows) na pasta extraída, aquela que contém `backend` e `frontend`.

Se o Python 3.14 ainda não estiver disponível:

```powershell
uv python install 3.14
```

Entre na pasta do **backend** e crie/sincronize seu ambiente:

```powershell
cd .\backend
uv venv --python 3.14
uv sync --locked
```

`uv venv` cria o ambiente `.venv` e `uv sync --locked` instala as dependências previstas no `pyproject.toml`/`uv.lock` **sem alterar o arquivo de lock**. Os comandos `uv run ...` das próximas seções usam automaticamente esse ambiente; não é necessário ativá-lo manualmente.

> **Importante:** você ainda está na pasta `backend` neste momento.

## 2. Configuração das Variáveis de Ambiente (`.env`)

Dentro de `backend/`, o arquivo `.env.example` mostra os campos esperados. Copie-o para `.env` (em PowerShell):

```powershell
Copy-Item .env.example .env
```

Abra `backend/.env` em um editor e preencha com as **credenciais do PostgreSQL da máquina em que o projeto será executado**:

```env
user=postgres
senha=sua_senha_do_postgres
host=localhost
porta=5432
banco=escola
```

- `user`: usuário do PostgreSQL (frequentemente `postgres`).
- `senha`: senha configurada para aquele usuário.
- `host`: `localhost` quando o banco roda no mesmo computador; outro endereço se houver servidor remoto acessível.
- `porta`: normalmente `5432`.
- `banco`: nome exato do banco que você vai criar no passo seguinte.

**Não coloque aspas nos valores nem espaços ao redor de `=`.** O `.env` contém credenciais particulares: **não deve ser enviado ao GitHub ou compartilhado publicamente**. Por segurança, o pacote contém apenas `.env.example`; o `.env` original permanece no seu computador e deve ser recriado na máquina da faculdade.

## 3. Remontar o Banco de Dados (Alembic)

1. Inicie o serviço do **PostgreSQL**.
2. Abra `pgAdmin` (ou DBeaver) e conecte-se ao PostgreSQL com o usuário e senha do `.env`.
3. Em **Databases / Bancos de dados**, crie um **banco vazio** com o nome escolhido em `banco` (no exemplo, `escola`). **Não crie tabelas manualmente**.
4. No terminal, ainda dentro da pasta `backend`, execute:

```powershell
uv run alembic upgrade head
```

Esse comando aplica **todas as migrações do histórico existente**, criando as tabelas:

- `tb_enderecos`
- `tb_alunos`
- `tb_disciplinas`
- `tb_notas`
- `tb_livros` **(nova)**
- `tb_emprestimos` **(nova)**

As duas novas tabelas foram adicionadas por uma **migração incremental**, sem substituir as migrações anteriores. Se o banco já existia e estava na última migração antiga, o mesmo `upgrade head` aplica apenas as migrações ainda pendentes.

Para conferir qual revisão está aplicada:

```powershell
uv run alembic current
```

A revisão final deste pacote é `b1b11017c026`. **Não rode `alembic revision --autogenerate` para instalar o projeto**: as migrações necessárias já estão entregues na pasta `alembic/versions`. Se os arquivos de migração estiverem faltando, recupere o pacote completo em vez de gerar uma nova história de migrações.

## 4. Rodar o Servidor (Uvicorn)

Depois de configurar o PostgreSQL e aplicar o Alembic, inicie o backend **na pasta `backend`**:

```powershell
uv run uvicorn app.main:app --reload
```

Deixe esse terminal aberto. O endereço esperado é:

- API: <http://127.0.0.1:8000>
- Documentação interativa (Swagger): <http://127.0.0.1:8000/docs>

Se o terminal mostrar `Application startup complete`, o servidor iniciou. Abra `/docs` no navegador: a documentação deve listar as rotas antigas e as novas de **Biblioteca - Livros** e **Biblioteca - Empréstimos**.

### Abrir o frontend Streamlit (segundo terminal)

**Não feche o terminal do Uvicorn.** Abra um **segundo PowerShell** na pasta extraída que contém `backend` e `frontend` e execute:

```powershell
cd .\frontend
uv venv --python 3.14
uv sync --locked
uv run streamlit run app.py
```

Abra no navegador:

- **Frontend Streamlit:** <http://localhost:8501>

A navegação lateral deve mostrar **Alunos, Endereço, Disciplinas, Notas e Biblioteca**. O frontend envia requisições HTTP para `http://127.0.0.1:8000`, endereço já definido no arquivo `frontend/connection/base_api.py`. Portanto, o Uvicorn precisa continuar rodando na porta **8000**.

**Resumo dos terminais:**

| Terminal | Pasta | Comando que fica executando |
|---|---|---|
| 1 | `backend` | `uv run uvicorn app.main:app --reload` |
| 2 | `frontend` | `uv run streamlit run app.py` |

Para parar um servidor, pressione `Ctrl+C` no terminal correspondente.

## 5. Populando o Banco de Dados (Streamlit e Postman)

As tabelas se relacionam por chaves estrangeiras. Para cadastrar alunos e notas num banco vazio, respeite a ordem abaixo. **Agora a forma principal de interação é o Streamlit**; as rotas HTTP e os exemplos JSON permanecem disponíveis para testes no Swagger ou Postman.

### Passo 1: Criar Endereço

**No Streamlit:** menu **Endereço → Criar**. Você pode informar o CEP e clicar em **Buscar CEP** para preencher os dados consultando o ViaCEP; depois clique em **Cadastrar Endereço**. Também é possível preencher os campos manualmente.

**Rota:** `POST http://127.0.0.1:8000/enderecos/criar-endereco`

Exemplo de JSON:

```json
{
  "cep": "70000-000",
  "endereco": "Rua das Flores, 123",
  "bairro": "Centro",
  "cidade": "Brasília",
  "estado": "DF",
  "regiao": "Centro-Oeste"
}
```

O backend também oferece `GET /enderecos/consultar-cep/{cep}` e `POST /enderecos/criar-endereco-por-cep/{cep}` (este último retorna o ID do endereço criado ou existente).

**Anote o ID do endereço** na aba de consulta (ou consulte diretamente a tabela `tb_enderecos`), pois será usado para cadastrar o aluno.

### Passo 2: Criar Aluno

**No Streamlit:** menu **Alunos → Criar**. Informe matrícula, nome, e-mail e o ID do endereço cadastrado; clique em **Cadastrar Aluno**.

**Rota:** `POST http://127.0.0.1:8000/alunos/criar-aluno`

```json
{
  "matricula": "202612345",
  "nome_aluno": "João Silva",
  "email": "joao@email.com",
  "endereco_id": 1
}
```

Substitua `endereco_id` pelo valor real. Consulte a lista de alunos e **anote o `id`** para usar em empréstimos ou notas. A matrícula não é o ID do aluno.

### Passo 3: Criar Disciplina

**No Streamlit:** menu **Disciplinas → Criar**. Informe nome, carga horária e semestre; clique em **Cadastrar Disciplina**.

**Rota:** `POST http://127.0.0.1:8000/disciplinas/criar-disciplina`

```json
{
  "nome_disciplina": "Cálculo Multivariável",
  "carga": 60,
  "semestre": 3
}
```

### Passo 4: Criar Nota

**No Streamlit:** menu **Notas → Criar**. Informe o ID de um aluno existente, o ID de uma disciplina existente e a nota; clique em **Cadastrar Nota**.

**Rota:** `POST http://127.0.0.1:8000/notas/criar-nota`

```json
{
  "aluno_id": 1,
  "disciplina_id": 1,
  "nota": 9.5
}
```

### Passo 5: Cadastrar livro (novo módulo Biblioteca)

**No Streamlit:** menu **Biblioteca → Cadastrar livro**. Informe o título e o autor. O ISBN é opcional. Clique em **Cadastrar livro**. A aba **Consultar livros** exibe os IDs e os livros cadastrados.

**Rota:** `POST http://127.0.0.1:8000/livros/criar-livro`

```json
{
  "titulo": "Dom Casmurro",
  "autor": "Machado de Assis",
  "isbn": "9780000000000"
}
```

Cada registro em `tb_livros` representa **um exemplar emprestável**. Se a escola possui dois exemplares físicos do mesmo título, podem ser cadastrados dois registros distintos, com IDs diferentes.

### Passo 6: Registrar empréstimo (novo módulo Biblioteca)

**No Streamlit:** menu **Biblioteca → Registrar empréstimo**. Selecione um aluno já cadastrado e um livro existente. Clique em **Registrar empréstimo**.

**Rota:** `POST http://127.0.0.1:8000/emprestimos/criar-emprestimo`

```json
{
  "aluno_id": 1,
  "livro_id": 1
}
```

Regras implementadas pelo `Emprestimo Service`:

1. **Aluno inexistente:** resposta HTTP **404**, `Aluno não encontrado.`
2. **Livro inexistente:** resposta HTTP **404**, `Livro não encontrado.`
3. **Livro atualmente emprestado:** resposta HTTP **409**, `Este livro já está emprestado.`
4. Em caso de sucesso, registra em `tb_emprestimos` os IDs do aluno/livro, a data do empréstimo e o status `Emprestado`.

O registro do empréstimo **não duplica dados do aluno nem do livro**. A tabela `tb_emprestimos` contém chaves estrangeiras que referenciam `tb_alunos` e `tb_livros`.

### Passo 7: Consultar e devolver livros

- **Biblioteca → Consultar empréstimos:** mostra ID, aluno, livro, datas e status.
- **Biblioteca → Devolver livro:** selecione um empréstimo ainda aberto e clique em **Registrar devolução**. O status muda para `Devolvido` e a data de devolução é preenchida.
- Um livro devolvido **pode ser emprestado novamente**; o histórico anterior permanece armazenado.

**Rota de consulta:** `GET http://127.0.0.1:8000/emprestimos/pegar-dados-emprestimo`

**Rota de devolução:** `PUT http://127.0.0.1:8000/emprestimos/devolver-livro/{id}`

> O `{id}` da devolução é o **ID do empréstimo**, não o ID do livro. Exemplo: `/emprestimos/devolver-livro/1`.

## 6. Lista das Rotas

As rotas antigas permanecem disponíveis. Para testes manuais, utilize a interface em `/docs`, o frontend Streamlit ou o Postman.

**Endereços (`/enderecos`):**
- `GET /enderecos/pegar-mensagem`
- `GET /enderecos/pegar-dados-endereco`
- `GET /enderecos/consultar-cep/{cep}`
- `POST /enderecos/criar-endereco`
- `POST /enderecos/criar-endereco-por-cep/{cep}`
- `PUT /enderecos/atualizar-endereco/{id}`
- `DELETE /enderecos/deletar-endereco/{id}`

**Alunos (`/alunos`):**
- `GET /alunos/pegar-mensagem`
- `GET /alunos/pegar-dados-aluno`
- `GET /alunos/pegar-dados-aluno-por-id/{id}`
- `POST /alunos/criar-aluno`
- `PUT /alunos/atualizar-aluno/{id}`
- `DELETE /alunos/deletar-aluno/{id}`

**Disciplinas (`/disciplinas`):**
- `GET /disciplinas/pegar-mensagem`
- `GET /disciplinas/pegar-dados-disciplina`
- `GET /disciplinas/pegar-dados-disciplina-por-id/{id}`
- `POST /disciplinas/criar-disciplina`
- `PUT /disciplinas/atualizar-disciplina/{id}`
- `DELETE /disciplinas/deletar-disciplina/{id}`

**Notas (`/notas`):**
- `GET /notas/pegar-mensagem`
- `GET /notas/pegar-dados-nota`
- `GET /notas/pegar-dados-nota-por-id/{id}`
- `POST /notas/criar-nota`
- `PUT /notas/atualizar-nota/{id}`
- `DELETE /notas/deletar-nota/{id}`

**Biblioteca — Livros (`/livros`):**
- `GET /livros/pegar-dados-livro`
- `GET /livros/pegar-dados-livro-por-id/{id}`
- `POST /livros/criar-livro`

**Biblioteca — Empréstimos (`/emprestimos`):**
- `GET /emprestimos/pegar-dados-emprestimo`
- `POST /emprestimos/criar-emprestimo`
- `PUT /emprestimos/devolver-livro/{id}`

## 7. Estrutura do Projeto (arquivos e responsabilidades)

```text
projeto/
├── backend/
│   ├── .env.example              # modelo de credenciais; criar .env local
│   ├── README.md                 # este guia completo
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/            # histórico + migração da biblioteca
│   └── app/
│       ├── database.py          # engine, Base, sessão e get_db
│       ├── main.py              # registra os routers no FastAPI
│       ├── models.py            # tabelas antigas + Livro e Emprestimo
│       ├── schemas.py           # schemas antigos + LivroIn e EmprestimoIn
│       ├── routers/
│       │   ├── alunos.py
│       │   ├── enderecos.py
│       │   ├── disciplinas.py
│       │   ├── notas.py
│       │   ├── livros.py         # novo
│       │   └── emprestimos.py    # novo
│       └── services/
│           ├── alunos.py
│           ├── enderecos.py
│           ├── cep.py
│           ├── livros.py         # novo
│           └── emprestimos.py    # novo
└── frontend/
    ├── app.py                    # navegação; agora inclui Biblioteca
    ├── pyproject.toml
    ├── uv.lock
    ├── connection/base_api.py   # requisições HTTP para o FastAPI
    ├── components/base_tela.py
    └── menus/
        ├── pagina_aluno.py
        ├── pagina_endereco.py
        ├── pagina_disciplina.py
        ├── pagina_nota.py
        └── pagina_biblioteca.py  # nova
```

**Por que não foram movidos `models.py` e `schemas.py` para pastas novas?**

O projeto original importa diretamente `from app.models import ...` e `from app.schemas import ...`. Já existem diretórios vazios chamados `app/models/` e `app/schemas/` no arquivo de origem. Transformá-los em pacotes Python ao mesmo tempo em que existem `models.py`/`schemas.py` pode gerar conflitos de importação; mover todos os arquivos exigiria adaptar vários imports e o Alembic. Como a prioridade da prova é **não quebrar funcionalidades existentes**, mantivemos a organização original e acrescentamos os novos routers/services nas pastas já utilizadas. O módulo Biblioteca está separado no frontend em `pagina_biblioteca.py`. Uma migração organizacional dos Models/Schemas pode ser feita em outro momento, com testes específicos.

## 8. Checklist para a Avaliação e Solução de Problemas

### Checklist rápido — banco vazio

1. [ ] PostgreSQL está instalado e em execução.
2. [ ] Criei um banco vazio com o nome do `backend/.env`.
3. [ ] Executei `uv sync --locked` **dentro de `backend`**.
4. [ ] Executei `uv run alembic upgrade head` sem erro.
5. [ ] Iniciei `uv run uvicorn app.main:app --reload` e mantive o terminal aberto.
6. [ ] Abri <http://127.0.0.1:8000/docs> e vi as rotas antigas e da Biblioteca.
7. [ ] Executei `uv sync --locked` **dentro de `frontend`**.
8. [ ] Iniciei `uv run streamlit run app.py` em outro terminal.
9. [ ] Abri <http://localhost:8501> e vi o menu Biblioteca.
10. [ ] Cadastrei endereço, aluno, livro e empréstimo. Registrei uma devolução.

### Problemas comuns

| Sintoma | Conferência / solução |
|---|---|
| `uv` não é reconhecido | Instale o `uv` e reabra o terminal; confira `uv --version`. |
| `No solution found` / erro Python | Confira o Python 3.14 (`uv python install 3.14`) e rode `uv sync --locked` na pasta correta. |
| `connection refused` / `OperationalError` no Alembic | Confira se PostgreSQL está ligado e se `host`, `porta`, `user`, `senha` e `banco` estão corretos no `backend/.env`. |
| `database ... does not exist` | Crie o banco vazio no pgAdmin **antes** do Alembic. |
| `relation ... already exists` ao reconstruir | Não misture tabelas criadas manualmente com um banco novo; use um banco realmente vazio e `upgrade head`, sem apagar bancos que tenham dados importantes. |
| Erro ao consultar ou cadastrar no Streamlit | O backend precisa estar ativo em `127.0.0.1:8000`. Abra `/docs` para verificar. |
| `404 Aluno não encontrado` no empréstimo | Cadastre o aluno e use seu `id` real (não a matrícula). |
| `404 Livro não encontrado` no empréstimo | Cadastre o livro e use seu `id` real. |
| `409 Este livro já está emprestado` | Registre a devolução antes de emprestar o mesmo exemplar novamente. |
| CEP não consulta | Verifique a conexão com a internet e se o CEP tem 8 dígitos. O cadastro manual de endereço continua disponível. |

### Verificação manual das regras do Desafio 2 (Swagger)

No <http://127.0.0.1:8000/docs>, teste `POST /emprestimos/criar-emprestimo` com:

- `{"aluno_id": 999999, "livro_id": 1}` após cadastrar o livro 1: deve retornar **404** para aluno inexistente.
- `{"aluno_id": 1, "livro_id": 999999}` após cadastrar o aluno 1: deve retornar **404** para livro inexistente.
- IDs válidos de aluno e livro ainda disponíveis: deve retornar **201**, com o ID do empréstimo.
- Os mesmos IDs novamente, sem devolução: deve retornar **409**.
- Após `PUT /emprestimos/devolver-livro/{id}`, novo empréstimo do mesmo exemplar deve retornar **201**.

Se o banco estiver em branco, os IDs são gerados na ordem dos cadastros; não presuma que serão `1` se já existirem registros.

> **Limitação do modelo simples:** cada `tb_livros` representa um exemplar físico; não foi criado um sistema de obras/edições/cópias separado, pois isso extrapolaria o exercício. A consulta de empréstimos conserva o histórico. Alunos e livros já vinculados a empréstimos não devem ser apagados diretamente no banco sem considerar a integridade das chaves estrangeiras.
