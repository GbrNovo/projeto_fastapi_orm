from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LivroIn
from app.services import livros as livro_service

router = APIRouter(prefix="/livros", tags=["Biblioteca - Livros"])


@router.get("/pegar-dados-livro")
def pegar_dados_livro(db: Session = Depends(get_db)):
    return livro_service.pegar_dados_livro(db)


@router.get("/pegar-dados-livro-por-id/{id}")
def pegar_dados_livro_por_id(id: int, db: Session = Depends(get_db)):
    return livro_service.pegar_dados_livro_por_id(id, db)


@router.post("/criar-livro", status_code=201)
def criar_livro(livro: LivroIn, db: Session = Depends(get_db)):
    return livro_service.criar_livro(livro, db)
