import streamlit as st
from connection.base_api import BaseApi
import pandas as pd
from components.base_tela import TelaBase

class DisciplinaTela(TelaBase):

    def __init__(self):
        self.base = BaseApi()
        self.titulo = "Tela de disciplinas"
        self.descricao = "Essa tela é usada para consulta de disciplinas"

    def consultar(self):
        endpoint = "/disciplinas/pegar-dados-disciplina"
        dados = self.base.get(endpoint)
        return dados
   
    def consultar_por_id(self, id):
        endpoint = f"/disciplinas/pegar-dados-disciplina-por-id/{id}"
        dados = self.base.get(endpoint)
        return dados
   
    def criar(self, params):
        endpoint = "/disciplinas/criar-disciplina"
        return self.base.post(endpoint, params)

    def atualizar(self, id, params):
        endpoint = f"/disciplinas/atualizar-disciplina/{id}"
        return self.base.put(endpoint, params)

    def deletar(self, id):
        endpoint = f"/disciplinas/deletar-disciplina/{id}"
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
            id = st.text_input("Digite o ID da Disciplina")
            if id:
                id = int(id)
                dados = self.consultar_por_id(id)
                self.criar_dataframe(dados)
                
        with abas[2]:
            nome_disciplina = st.text_input("Digite o Nome da Disciplina")
            carga = st.text_input("Digite a Carga Horária")
            semestre = st.text_input("Digite o Semestre")
            
            if st.button("Cadastrar Disciplina"):
                params = {
                    "nome_disciplina": nome_disciplina,
                    "carga": carga,
                    "semestre": semestre
                }
                retorno = self.criar(params)
                st.success("Cadastrado com sucesso!")
                
        with abas[3]:
            id_atualizar = st.text_input("Digite o ID da disciplina a ser atualizada")
            nome_disciplina_novo = st.text_input("Digite o novo Nome da Disciplina (deixe vazio para não mudar)")
            carga_nova = st.text_input("Digite a nova Carga Horária (deixe vazio para não mudar)")
            semestre_novo = st.text_input("Digite o novo Semestre (deixe vazio para não mudar)")
            
            if st.button("Atualizar Disciplina"):
                params = {}
                
                if nome_disciplina_novo: 
                    params["nome_disciplina"] = nome_disciplina_novo
                if carga_nova: 
                    params["carga"] = carga_nova
                if semestre_novo: 
                    params["semestre"] = semestre_novo
                
                retorno = self.atualizar(id_atualizar, params)
                st.success("Atualizado com sucesso!")
                
        with abas[4]:
            id_deletar = st.text_input("Digite o ID da disciplina a ser deletada")
            
            if st.button("Excluir Disciplina"):
                retorno = self.deletar(id_deletar)
                st.success("Deletado com sucesso!")
                
        super().rodape()

DisciplinaTela().renderizar()