from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EmprestimoIn
from app.services import emprestimos as emprestimo_service

router = APIRouter(prefix="/emprestimos", tags=["Biblioteca - Empréstimos"])


@router.get("/pegar-dados-emprestimo")
def pegar_dados_emprestimo(db: Session = Depends(get_db)):
    return emprestimo_service.pegar_dados_emprestimo(db)


@router.post("/criar-emprestimo", status_code=201)
def criar_emprestimo(emprestimo: EmprestimoIn, db: Session = Depends(get_db)):
    return emprestimo_service.criar_emprestimo(emprestimo, db)


@router.put("/devolver-livro/{id}")
def devolver_livro(id: int, db: Session = Depends(get_db)):
    return emprestimo_service.devolver_livro(id, db)
