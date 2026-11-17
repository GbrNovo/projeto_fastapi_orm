import streamlit as st
from connection.base_api import BaseApi
import pandas as pd
from components.base_tela import TelaBase

class EnderecoTela(TelaBase):

    def __init__(self):
        self.base = BaseApi()
        self.titulo = "Tela de endereço"
        self.descricao = "Essa tela é usada para consulta de endereços"

    def consultar(self):
        endpoint = "/enderecos/pegar-dados-endereco"
        dados = self.base.get(endpoint)
        return dados
   
    def consultar_por_id(self, id):
        endpoint = f"/enderecos/pegar-dados-endereco-por-id/{id}"
        dados = self.base.get(endpoint)
        return dados
   
    def criar(self, params):
        endpoint = "/enderecos/criar-endereco"
        return self.base.post(endpoint, params)

    def buscar_cep(self, cep):
        dados = self.base.get(f"/enderecos/consultar-cep/{cep}")
        if "detail" in dados:
            st.error(dados["detail"])
            return None
        return dados

    def atualizar(self, id, params):
        endpoint = f"/enderecos/atualizar-endereco/{id}"
        return self.base.put(endpoint, params)

    def deletar(self, id):
        endpoint = f"/enderecos/deletar-endereco/{id}"
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
            id = st.text_input("Digite o ID do Endereço")
            if id:
                id = int(id)
                dados = self.consultar_por_id(id)
                self.criar_dataframe(dados)
                
        with abas[2]:
            cep = st.text_input("Digite o CEP")
            if st.button("Buscar CEP"):
                dados = self.buscar_cep(cep)
                if dados:
                    st.session_state["cadastro_endereco"] = dados.get("endereco", "")
                    st.session_state["cadastro_bairro"] = dados.get("bairro", "")
                    st.session_state["cadastro_cidade"] = dados.get("cidade", "")
                    st.session_state["cadastro_estado"] = dados.get("estado", "")
                    st.session_state["cadastro_regiao"] = dados.get("regiao", "")
            endereco = st.text_input("Digite o Endereço", key="cadastro_endereco")
            bairro = st.text_input("Digite o Bairro", key="cadastro_bairro")
            cidade = st.text_input("Digite a Cidade", key="cadastro_cidade")
            estado = st.text_input("Digite o Estado", key="cadastro_estado")
            regiao = st.text_input("Digite a Região", key="cadastro_regiao")
            
            if st.button("Cadastrar Endereço"):
                params = {
                    "cep": cep,
                    "endereco": endereco,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "regiao": regiao
                }
                retorno = self.criar(params)
                st.success("Cadastrado com sucesso!")
                
        with abas[3]:
            id_atualizar = st.text_input("Digite o ID do endereço a ser atualizado")
            cep_novo = st.text_input("Digite o novo CEP (deixe vazio para não mudar)")
            endereco_novo = st.text_input("Digite o novo Endereço (deixe vazio para não mudar)")
            bairro_novo = st.text_input("Digite o novo Bairro (deixe vazio para não mudar)")
            cidade_nova = st.text_input("Digite a nova Cidade (deixe vazio para não mudar)")
            estado_novo = st.text_input("Digite o novo Estado (deixe vazio para não mudar)")
            regiao_nova = st.text_input("Digite a nova Região (deixe vazio para não mudar)")
            
            if st.button("Atualizar Endereço"):
                params = {}
                
                if cep_novo: 
                    params["cep"] = cep_novo
                if endereco_novo: 
                    params["endereco"] = endereco_novo
                if bairro_novo: 
                    params["bairro"] = bairro_novo
                if cidade_nova: 
                    params["cidade"] = cidade_nova
                if estado_novo: 
                    params["estado"] = estado_novo
                if regiao_nova: 
                    params["regiao"] = regiao_nova
                
                retorno = self.atualizar(id_atualizar, params)
                st.success("Atualizado com sucesso!")
                
        with abas[4]:
            id_deletar = st.text_input("Digite o ID do endereço a ser deletado")
            
            if st.button("Excluir Endereço"):
                retorno = self.deletar(id_deletar)
                st.success("Deletado com sucesso!")
                
        super().rodape()

EnderecoTela().renderizar()