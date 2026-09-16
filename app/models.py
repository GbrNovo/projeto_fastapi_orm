from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Endereco(Base):
  __tablename__ = 'tb_enderecos'
  id: Mapped[int] = mapped_column(primary_key=True)
  cep: Mapped[str] = mapped_column(String(10), unique=True)
  Endereco: Mapped[str] = mapped_column(String(255))


# FAZER ALUNOS E DISCIPLINAS P/ PRÓXIMA AULA