from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import EnderecoIn, EnderecoUpdateIn
from app.services import enderecos as endereco_service
from app.services.cep import buscar_cep

router = APIRouter(prefix="/enderecos")

@router.get("/pegar-mensagem")
def primeira_api():
  return {"message": "você está na rota endereços"}

@router.get("/pegar-dados-endereco")
def pegar_dados_endereco():
  return endereco_service.pegar_dados_endereco()

@router.get("/consultar-cep/{cep}")
def consultar_cep(cep: str):
  return buscar_cep(cep)

@router.post("/criar-endereco")
def criar_endereco(endereco: EnderecoIn):
  return endereco_service.criar_endereco(endereco)

@router.post("/criar-endereco-por-cep/{cep}")
def criar_endereco_por_cep(cep: str, db: Session = Depends(get_db)):
  return endereco_service.criar_endereco_por_cep(cep, db)

@router.put("/atualizar-endereco/{id}")
def atualizar_endereco(id: int, endereco: EnderecoUpdateIn):
  return endereco_service.atualizar_endereco(id, endereco)

@router.delete("/deletar-endereco/{id}")
def deletar_endereco(id: int):
  return endereco_service.deletar_endereco(id)
