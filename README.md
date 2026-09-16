## Instalação

- uv init
- uv venv --python 3.14
- uv add link_github
- uv sync

## Montar as tabelas com o alembic

- alembic init "nome_da_pasta"
  (Cria a estrutura inicial do alembic)

- alembic revision --autogenerate -m "mensagem"
  (Cria os comandos de integração das tabelas ORM definidas no models.py para aplicar no DB)

- alembic upgrade head
  (Aplica o que foi gerado pelo comando anterior (Revision --autogenerate))

- alembic history