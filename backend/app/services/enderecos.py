from sqlalchemy import select, text
from sqlalchemy.orm import Session
import pandas as pd
from app.database import engine
from app.models import Endereco
from app.schemas import EnderecoIn, EnderecoUpdateIn
from app.services.cep import buscar_cep

def pegar_dados_endereco():
  query = "SELECT * FROM tb_enderecos"
  df = pd.read_sql(query, engine)
  return df.to_dict(orient="records")

def criar_endereco(endereco: EnderecoIn):
  df = pd.DataFrame([endereco.model_dump()])
  df.to_sql("tb_enderecos", engine, if_exists="append", index=False)
  return {"mensagem": "Endereço cadastrado com sucesso!"}

def criar_endereco_por_cep(cep: str, db: Session):
  dados = buscar_cep(cep)
  cep_sem_hifen = dados["cep"].replace("-", "")
  existente = db.scalars(select(Endereco).where(Endereco.cep.in_([dados["cep"], cep_sem_hifen]))).first()
  if existente:
    return {"mensagem": "Endereço já cadastrado.", "id": existente.id}

  endereco = Endereco(**dados)
  db.add(endereco)
  db.commit()
  db.refresh(endereco)
  return {"mensagem": "Endereço cadastrado com sucesso!", "id": endereco.id}

def atualizar_endereco(id: int, endereco: EnderecoUpdateIn):
  campos_sql = ", ".join([f"{chave} = :{chave}" for chave in endereco.model_dump(exclude_unset=True).keys()])
  query = f"""
      UPDATE tb_enderecos
      SET {campos_sql}
      WHERE id = :id
  """
  with engine.connect() as conn:
    conn.execute(
      text(query),
      {"id":id, **endereco.model_dump(exclude_unset=True)}
    )
    conn.commit()
  return {"mensagem": "Endereço atualizado com sucesso."}

def deletar_endereco(id: int):
  query = f"DELETE FROM tb_enderecos WHERE id = {id}"
  with engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()
  return {"mensagem": "Endereço deletado com sucesso."}
