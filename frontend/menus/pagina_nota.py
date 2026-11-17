import streamlit as st
from connection.base_api import BaseApi
import pandas as pd
from components.base_tela import TelaBase

class NotaTela(TelaBase):

    def __init__(self):
        self.base = BaseApi()
        self.titulo = "Tela de notas"
        self.descricao = "Essa tela é usada para consulta de notas"

    def consultar(self):
        endpoint = "/notas/pegar-dados-nota"
        dados = self.base.get(endpoint)
        return dados
   
    def consultar_por_id(self, id):
        endpoint = f"/notas/pegar-dados-nota-por-id/{id}"
        dados = self.base.get(endpoint)
        return dados
   
    def criar(self, params):
        endpoint = "/notas/criar-nota"
        return self.base.post(endpoint, params)

    def atualizar(self, id, params):
        endpoint = f"/notas/atualizar-nota/{id}"
        return self.base.put(endpoint, params)

    def deletar(self, id):
        endpoint = f"/notas/deletar-nota/{id}"
        return self.base.delete(endpoint)
   
    def criar_dataframe(self, dados):
        if isinstance(dados, dict):
            dados = [dados]
        df = pd.DataFrame(dados)
        st.dataframe(df)

    def renderizar(self):
        super().cabecalho(self.titulo, self.descricao)
        abas = st.tabs(["Consultar", "Consultar por ID", "Criar", "Atualizar", "Excluir"])
        
        with abas[0]:
            dados = self.consultar()
            self.criar_dataframe(dados)
            
        with abas[1]:
            id = st.text_input("Digite o ID da Nota")
            if id:
                id = int(id)
                dados = self.consultar_por_id(id)
                self.criar_dataframe(dados)
                
        with abas[2]:
            aluno_id = st.text_input("Digite o ID do Aluno")
            disciplina_id = st.text_input("Digite o ID da Disciplina")
            nota = st.text_input("Digite a Nota")
            
            if st.button("Cadastrar Nota"):
                params = {
                    "aluno_id": aluno_id,
                    "disciplina_id": disciplina_id,
                    "nota": nota
                }
                retorno = self.criar(params)
                st.success("Cadastrado com sucesso!")
                
        with abas[3]:
            id_atualizar = st.text_input("Digite o ID da nota a ser atualizada")
            aluno_id_novo = st.text_input("Digite o novo ID do Aluno (deixe vazio para não mudar)")
            disciplina_id_novo = st.text_input("Digite o novo ID da Disciplina (deixe vazio para não mudar)")
            nota_nova = st.text_input("Digite a nova Nota (deixe vazio para não mudar)")
            
            if st.button("Atualizar Nota"):
                params = {}
                
                if aluno_id_novo: 
                    params["aluno_id"] = aluno_id_novo
                if disciplina_id_novo: 
                    params["disciplina_id"] = disciplina_id_novo
                if nota_nova: 
                    params["nota"] = nota_nova
                
                retorno = self.atualizar(id_atualizar, params)
                st.success("Atualizado com sucesso!")
                
        with abas[4]:
            id_deletar = st.text_input("Digite o ID da nota a ser deletada")
            
            if st.button("Excluir Nota"):
                retorno = self.deletar(id_deletar)
                st.success("Deletado com sucesso!")
                
        super().rodape()

NotaTela().renderizar()