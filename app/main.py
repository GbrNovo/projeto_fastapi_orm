from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from app.database import engine
from app.schemas import EnderecoIn, AlunoUpdateIn

app = FastAPI()

@app.get("/pegar-mensagem")
def primeira_api():
  return {"message": "Hello, World!"}

@app.get("/pegar-dados-alunos")
def pegar_dados_alunos():
  query = "SELECT * FROM tb_alunos ORDER BY id"
  df = pd.read_sql(query, engine)
  return df.to_dict(orient="records")

@app.get("/pegar-dados-enderecos")
def pegar_dados_enderecos():
  query = "SELECT * FROM tb_enderecos"
  df = pd.read_sql(query, engine)
  return df.to_dict(orient="records")

@app.get("/pegar-dados-alunos-por-id/{id}")
def pegar_dados_alunos_por_id(id: int):
  query = f"SELECT * FROM tb_alunos WHERE id = {id}"
  df = pd.read_sql(query, engine)
  return df.to_dict(orient="records")

@app.post("/criar-aluno")
def criar_aluno(aluno: dict):
  # Transformando dict em df
  df = pd.DataFrame([aluno])
  # Insert no banco de dados
  df.to_sql("tb_alunos", engine, if_exists="append", index=False)
  return {"mensagem": "Aluno cadastrado com sucesso!"}

@app.post("/criar-endereco")
def criar_endereco(endereco: EnderecoIn):
  # Transformando dict em df
  df = pd.DataFrame([endereco.model_dump()])
  # Insert no banco de dados
  df.to_sql("tb_enderecos", engine, if_exists="append", index=False)
  return {"mensagem": "Endereço cadastrado com sucesso!"}

@app.put("/atualizar-aluno/{id}")
def atualizar_aluno(id: int, aluno: AlunoUpdateIn):
  campos_sql = ", ".join([f"{chave} = :{chave}" for chave in aluno.model_dump(exclude_unset=True).keys()])
  query = f"""
      UPDATE tb_alunos
      SET {campos_sql}
      WHERE id = :id
  """ 
  with engine.connect() as conn:
    conn.execute(
      text(query),
      {"id":id, **aluno.model_dump(exclude_unset=True)}
    )
    conn.commit(

    )
  return {"mensagem": "Aluno atualizado com sucesso."}

@app.delete("/deletar-aluno/{id}")
def deletar_aluno(id: int):
  query = f"DELETE FROM tb_alunos WHERE id = {id}"
  with engine.connect() as conn:
    conn.execute( text(query))
    conn.commit() 
  return {"mensagem": "Aluno deletado com sucesso."}