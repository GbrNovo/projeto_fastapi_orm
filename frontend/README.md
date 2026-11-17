## Execução (Windows / PowerShell)

Primeiro, siga as seções 1–4 do guia do backend e deixe o servidor FastAPI ligado em <http://127.0.0.1:8000>.

Abra **outro terminal** na pasta `frontend`:

```powershell
uv python install 3.14
uv venv --python 3.14
uv sync --locked
uv run streamlit run app.py
```

Depois abra <http://localhost:8501>. O menu lateral possui Alunos, Endereço, Disciplinas, Notas e **Biblioteca**. A Biblioteca permite cadastrar e consultar livros, registrar empréstimos para alunos existentes e registrar devoluções.

O endereço da API está configurado em `connection/base_api.py` como `http://127.0.0.1:8000`; mantenha a porta 8000 no backend.
