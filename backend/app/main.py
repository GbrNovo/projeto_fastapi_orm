from fastapi import FastAPI
from app.routers import alunos 
from app.routers import enderecos
from app.routers import disciplinas
from app.routers import notas

app = FastAPI()

app.include_router(alunos.router)
app.include_router(enderecos.router)
app.include_router(disciplinas.router)
app.include_router(notas.router)
from app.routers import livros, emprestimos

app.include_router(livros.router)
app.include_router(emprestimos.router)
