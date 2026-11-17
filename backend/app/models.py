from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import String, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Endereco(Base):
    __tablename__ = 'tb_enderecos'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cep: Mapped[str] = mapped_column(String(10), unique=True)
    endereco: Mapped[str] = mapped_column(String(255))
    bairro: Mapped[str] = mapped_column(String(50))
    cidade: Mapped[str] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(50))
    regiao: Mapped[str] = mapped_column(String(50))

class Aluno(Base):
    __tablename__ = 'tb_alunos'

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20), unique=True)
    nome_aluno: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100))
    endereco_id: Mapped[int] = mapped_column(ForeignKey("tb_enderecos.id"))

class Disciplina(Base):
    __tablename__ = 'tb_disciplinas'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_disciplina: Mapped[str] = mapped_column(String(255))
    carga: Mapped[int] = mapped_column()
    semestre: Mapped[int] = mapped_column()

class Nota(Base):
    __tablename__ = 'tb_notas'

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("tb_alunos.id"))
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("tb_disciplinas.id"))
    nota: Mapped[float] = mapped_column(Numeric(5, 2))

# Módulo Biblioteca: cada registro de Livro representa um exemplar emprestável.
class Livro(Base):
    __tablename__ = 'tb_livros'

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255))
    autor: Mapped[str] = mapped_column(String(255))
    isbn: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


class Emprestimo(Base):
    __tablename__ = 'tb_emprestimos'

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey('tb_alunos.id'))
    livro_id: Mapped[int] = mapped_column(ForeignKey('tb_livros.id'))
    data_emprestimo: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data_devolucao: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='Emprestado')
