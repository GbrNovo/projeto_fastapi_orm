from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Aluno
from app.schemas import AlunoIn, AlunoUpdateIn

def pegar_dados_alunos(db: Session):
  aluno = db.scalars(select(Aluno).order_by(Aluno.id)).all()
  return aluno

def pegar_dados_alunos_por_id(id: int, db: Session):
  aluno = db.get(Aluno, id)
  return aluno

def criar_aluno(aluno: AlunoIn, db: Session):
  dados = Aluno(
    matricula = aluno.matricula,
    nome_aluno = aluno.nome_aluno,
    email = aluno.email,
    endereco_id = aluno.endereco_id
  )

  db.add(dados)
  db.commit()
  return {"mensagem": "Aluno cadastrado com sucesso!"}

def atualizar_aluno(id: int, aluno: AlunoUpdateIn, db: Session):
  dados = db.get(Aluno, id)
  campos = aluno.model_dump(exclude_unset=True)
  for campo, valor in campos.items():
    setattr(dados, campo, valor)
  db.commit()
  return {"mensagem": "Aluno atualizado com sucesso"}

def deletar_aluno(id: int, db: Session):
  dados = db.get(Aluno, id)
  db.delete(dados)
  db.commit()
  return {"mensagem": "Aluno deletado com sucesso"}
