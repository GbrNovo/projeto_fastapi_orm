import json
from urllib.request import urlopen
from urllib.error import URLError
from fastapi import HTTPException

def buscar_cep(cep: str):
  cep = cep.replace("-", "").replace(" ", "")
  if len(cep) != 8 or not cep.isdigit():
    raise HTTPException(status_code=400, detail="CEP inválido. Informe 8 dígitos.")

  try:
    with urlopen(f"https://viacep.com.br/ws/{cep}/json/", timeout=5) as resposta:
      dados = json.load(resposta)
  except (URLError, TimeoutError, ValueError) as erro:
    raise HTTPException(status_code=502, detail="Não foi possível consultar o ViaCEP.") from erro

  if dados.get("erro"):
    raise HTTPException(status_code=404, detail="CEP não encontrado.")

  return {
    "cep": dados["cep"],
    "endereco": dados["logradouro"],
    "bairro": dados["bairro"],
    "cidade": dados["localidade"],
    "estado": dados["estado"],
    "regiao": dados["regiao"]
  }
