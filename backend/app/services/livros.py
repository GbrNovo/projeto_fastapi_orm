from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Livro
from app.schemas import LivroIn


def pegar_dados_livro(db: Session):
    return db.scalars(select(Livro).order_by(Livro.id)).all()


def pegar_dados_livro_por_id(id: int, db: Session):
    livro = db.get(Livro, id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    return livro


def criar_livro(livro: LivroIn, db: Session):
    dados = Livro(**livro.model_dump())
    db.add(dados)
    db.commit()
    db.refresh(dados)
    return {"mensagem": "Livro cadastrado com sucesso!", "id": dados.id}
