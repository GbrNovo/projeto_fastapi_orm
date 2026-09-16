from sqlalchemy import String
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


# FAZER ALUNOS E DISCIPLINAS P/ PRÓXIMA AULA