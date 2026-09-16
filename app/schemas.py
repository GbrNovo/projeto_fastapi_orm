from pydantic import BaseModel
from typing import Optional

# Schema de entrada para o tb_enderecos
class EnderecoIn(BaseModel):
  cep: str
  endereco: str
  bairro: int
  cidade: str
  estado: str
  regiao: str

# Schema de Entrada para o tb_aluno
class AlunoUpdateIn(BaseModel):
  matricula: Optional[str] = None
  nome_aluno: Optional[str] = None
  email: Optional[str] = None