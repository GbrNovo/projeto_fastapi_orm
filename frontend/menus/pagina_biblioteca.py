import requests
import streamlit as st
from components.base_tela import TelaBase
from connection.base_api import BaseApi


class BibliotecaTela(TelaBase):

    def __init__(self):
        self.base = BaseApi()

    def consultar(self, endpoint):
        try:
            resposta = self.base.get(endpoint)
        except (requests.exceptions.RequestException, ValueError):
            st.error("Não foi possível consultar a API. Verifique se o FastAPI está rodando na porta 8000.")
            return None
        if isinstance(resposta, dict) and "detail" in resposta:
            st.error(str(resposta["detail"]))
            return None
        return resposta

    def executar(self, metodo, endpoint, dados=None):
        try:
            if metodo == "post":
                resposta = self.base.post(endpoint, dados)
            else:
                resposta = self.base.put(endpoint, dados)
        except requests.exceptions.RequestException:
            st.error("Não foi possível conectar à API. Verifique se o FastAPI está rodando.")
            return

        try:
            conteudo = resposta.json()
        except ValueError:
            conteudo = {}
        if resposta.ok:
            st.success(conteudo.get("mensagem", "Operação concluída."))
            if "id" in conteudo:
                st.write(f"ID: {conteudo['id']}")
        else:
            st.error(str(conteudo.get("detail", f"Erro HTTP {resposta.status_code}")))

    def renderizar(self):
        super().cabecalho("Biblioteca", "Cadastro de livros, empréstimos e devoluções")
        abas = st.tabs([
            "Consultar livros", "Cadastrar livro", "Registrar empréstimo",
            "Consultar empréstimos", "Devolver livro"
        ])

        with abas[0]:
            livros = self.consultar("/livros/pegar-dados-livro")
            if isinstance(livros, list):
                if livros:
                    st.dataframe(livros, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhum livro cadastrado.")

        with abas[1]:
            with st.form("form_cadastrar_livro", clear_on_submit=True):
                titulo = st.text_input("Título do livro")
                autor = st.text_input("Autor")
                isbn = st.text_input("ISBN (opcional)")
                enviar = st.form_submit_button("Cadastrar livro")
            if enviar:
                if not titulo.strip() or not autor.strip():
                    st.error("Informe título e autor.")
                else:
                    self.executar("post", "/livros/criar-livro", {
                        "titulo": titulo.strip(),
                        "autor": autor.strip(),
                        "isbn": isbn.strip() or None,
                    })

        with abas[2]:
            alunos = self.consultar("/alunos/pegar-dados-aluno")
            livros = self.consultar("/livros/pegar-dados-livro")
            if isinstance(alunos, list) and isinstance(livros, list):
                if not alunos:
                    st.info("Cadastre um aluno no módulo Alunos antes de registrar um empréstimo.")
                elif not livros:
                    st.info("Cadastre um livro antes de registrar um empréstimo.")
                else:
                    nomes = {a["id"]: a["nome_aluno"] for a in alunos}
                    titulos = {l["id"]: l["titulo"] for l in livros}
                    with st.form("form_emprestimo"):
                        aluno_id = st.selectbox(
                            "Aluno", list(nomes), format_func=lambda id: f"{id} - {nomes[id]}"
                        )
                        livro_id = st.selectbox(
                            "Livro", list(titulos), format_func=lambda id: f"{id} - {titulos[id]}"
                        )
                        enviar = st.form_submit_button("Registrar empréstimo")
                    if enviar:
                        self.executar("post", "/emprestimos/criar-emprestimo", {
                            "aluno_id": aluno_id, "livro_id": livro_id
                        })
                        st.caption("Se o livro já estiver emprestado, a API impedirá a operação.")

        with abas[3]:
            emprestimos = self.consultar("/emprestimos/pegar-dados-emprestimo")
            if isinstance(emprestimos, list):
                if emprestimos:
                    st.dataframe(emprestimos, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhum empréstimo registrado.")

        with abas[4]:
            emprestimos = self.consultar("/emprestimos/pegar-dados-emprestimo")
            if isinstance(emprestimos, list):
                ativos = [e for e in emprestimos if e["status"] == "Emprestado"]
                if not ativos:
                    st.info("Não existem empréstimos pendentes de devolução.")
                else:
                    descricoes = {
                        e["id"]: f"Empréstimo {e['id']} - {e['aluno']} - {e['livro']}"
                        for e in ativos
                    }
                    with st.form("form_devolucao"):
                        id_emprestimo = st.selectbox(
                            "Empréstimo a devolver",
                            list(descricoes),
                            format_func=lambda id: descricoes[id],
                        )
                        enviar = st.form_submit_button("Registrar devolução")
                    if enviar:
                        self.executar("put", f"/emprestimos/devolver-livro/{id_emprestimo}")

        super().rodape()


BibliotecaTela().renderizar()
