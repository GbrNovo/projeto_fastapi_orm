from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AlunoIn, AlunoUpdateIn
from app.services import alunos as aluno_service

router = APIRouter(prefix="/alunos")

@router.get("/pegar-mensagem")
def primeira_api():
  return {"message": "Hello, World!"}

@router.get("/pegar-dados-aluno")
def pegar_dados_alunos(db: Session = Depends(get_db)):
  return aluno_service.pegar_dados_alunos(db)

@router.get("/pegar-dados-aluno-por-id/{id}")
def pegar_dados_alunos_por_id(id: int, db: Session = Depends(get_db)):
  return aluno_service.pegar_dados_alunos_por_id(id, db)

@router.post("/criar-aluno")
def criar_aluno(aluno: AlunoIn, db: Session = Depends(get_db)):
  return aluno_service.criar_aluno(aluno, db)

@router.put("/atualizar-aluno/{id}")
def atualizar_aluno(id: int, aluno: AlunoUpdateIn, db: Session = Depends(get_db)):
  return aluno_service.atualizar_aluno(id, aluno, db)

@router.delete("/deletar-aluno/{id}")
def deletar_aluno(id: int, db: Session = Depends(get_db)):
  return aluno_service.deletar_aluno(id, db)
