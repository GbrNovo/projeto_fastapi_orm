from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Aluno, Livro, Emprestimo
from app.schemas import EmprestimoIn


def pegar_dados_emprestimo(db: Session):
    consulta = (
        select(Emprestimo, Aluno.nome_aluno, Livro.titulo)
        .join(Aluno, Emprestimo.aluno_id == Aluno.id)
        .join(Livro, Emprestimo.livro_id == Livro.id)
        .order_by(Emprestimo.id)
    )
    registros = db.execute(consulta).all()
    return [
        {
            "id": emprestimo.id,
            "aluno_id": emprestimo.aluno_id,
            "aluno": nome_aluno,
            "livro_id": emprestimo.livro_id,
            "livro": titulo,
            "data_emprestimo": emprestimo.data_emprestimo,
            "data_devolucao": emprestimo.data_devolucao,
            "status": emprestimo.status,
        }
        for emprestimo, nome_aluno, titulo in registros
    ]


def criar_emprestimo(dados: EmprestimoIn, db: Session):
    # Regras obrigatórias do Desafio 2.
    if db.get(Aluno, dados.aluno_id) is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    if db.get(Livro, dados.livro_id) is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")

    # Um exemplar não pode estar com dois alunos ao mesmo tempo.
    emprestimo_ativo = db.scalars(
        select(Emprestimo).where(
            Emprestimo.livro_id == dados.livro_id,
            Emprestimo.data_devolucao.is_(None),
        )
    ).first()
    if emprestimo_ativo is not None:
        raise HTTPException(status_code=409, detail="Este livro já está emprestado.")

    emprestimo = Emprestimo(aluno_id=dados.aluno_id, livro_id=dados.livro_id)
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    return {"mensagem": "Empréstimo registrado com sucesso!", "id": emprestimo.id}


def devolver_livro(id: int, db: Session):
    emprestimo = db.get(Emprestimo, id)
    if emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado.")
    if emprestimo.data_devolucao is not None:
        raise HTTPException(status_code=409, detail="Este empréstimo já foi devolvido.")

    emprestimo.data_devolucao = datetime.now(timezone.utc)
    emprestimo.status = "Devolvido"
    db.commit()
    return {"mensagem": "Devolução registrada com sucesso!", "id": id}
