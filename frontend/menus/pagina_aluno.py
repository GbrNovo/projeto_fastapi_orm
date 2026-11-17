import streamlit as st
from connection.base_api import BaseApi
import pandas as pd
from components.base_tela import TelaBase

class AlunoTela(TelaBase):

    def __init__(self):
        self.base = BaseApi()
        self.titulo = "Tela de aluno"
        self.descricao = "Essa tela é usada para consulta de alunos"

    def consultar(self):
        endpoint = "/alunos/pegar-dados-aluno"
        dados = self.base.get(endpoint)
        return dados
   
    def consultar_por_id(self, id):
        endpoint = f"/alunos/pegar-dados-aluno-por-id/{id}"
        dados = self.base.get(endpoint)
        return dados
   
    def criar(self, params):
        endpoint = "/alunos/criar-aluno"
        return self.base.post(endpoint, params)

    def atualizar(self, id, params):
        endpoint = f"/alunos/atualizar-aluno/{id}"
        return self.base.put(endpoint, params)

    def deletar(self, id):
        endpoint = f"/alunos/deletar-aluno/{id}"
        return self.base.delete(endpoint)
   
    def criar_dataframe(self, dados):
        df = pd.DataFrame(dados)
        st.dataframe(df)

    def renderizar(self):
        super().cabecalho(self.titulo, self.descricao)
        abas = st.tabs(["Consultar", "Consultar por ID", "Criar", "Atualizar", "Excluir"])
        
        with abas[0]:
            dados = self.consultar()
            self.criar_dataframe(dados)
            
        with abas[1]:
            id = st.text_input("Digite o ID")
            if st.button("Consultar Aluno"):
                dados = self.consultar_por_id(id)
                df = pd.DataFrame([dados])
                st.dataframe(df)
                
        with abas[2]:
            matricula = st.text_input("Digite a Matricula")
            nome_aluno = st.text_input("Digite o Nome")
            email = st.text_input("Digite o Email")
            endereco_id = st.text_input("Digite o ID do endereco")
            params = {
                "matricula": matricula,
                "nome_aluno": nome_aluno,
                "email": email,
                "endereco_id": endereco_id
            }
            if st.button("Cadastrar Aluno"):
                retorno = self.criar(params)
                if retorno.ok:
                    st.success("Aluno cadastrado com sucesso!")
                else:
                    try:
                        st.error(str(retorno.json().get("detail", "Erro ao cadastrar aluno.")))
                    except ValueError:
                        st.error("Erro ao cadastrar aluno.")
            
        with abas[3]:
            id_atualizar = st.text_input("Digite o ID do aluno a ser atualizado")
            matricula_nova = st.text_input("Digite a nova Matricula (deixe vazio para não mudar)")
            nome_novo = st.text_input("Digite o novo Nome (deixe vazio para não mudar)")
            email_novo = st.text_input("Digite o novo Email (deixe vazio para não mudar)")
            endereco_id_novo = st.text_input("Digite o novo ID do endereco (deixe vazio para não mudar)")
            
            if st.button("Atualizar Aluno"):
                params = {}
                

                if matricula_nova: 
                    params["matricula"] = matricula_nova
                if nome_novo: 
                    params["nome_aluno"] = nome_novo
                if email_novo: 
                    params["email"] = email_novo
                if endereco_id_novo: 
                    params["endereco_id"] = endereco_id_novo
                
                retorno = self.atualizar(id_atualizar, params)
                st.success("Atualizado com sucesso!")
                
        with abas[4]:
            id_deletar = st.text_input("Digite o ID do aluno a ser deletado")
            
            if st.button("Excluir Aluno"):
                retorno = self.deletar(id_deletar)
                st.success("Deletado com sucesso!")
                
        super().rodape()

AlunoTela().renderizar()