import sys
from pathlib import Path
import streamlit as st

# Configuraão do diretório onde o app.py do streamlit está sendo executado
BASE_DIR = Path(__file__).parent
sys.path.append(BASE_DIR)

# Configura as páginas
pagina_aluno = st.Page("menus/pagina_aluno.py", title="Alunos", icon=":material/school:")
pagina_endereco = st.Page("menus/pagina_endereco.py", title="Endereço", icon=":material/house:")
pagina_nota = st.Page("menus/pagina_nota.py", title="Notas", icon=":material/lab_profile:")
pagina_disciplina = st.Page("menus/pagina_disciplina.py", title="Disciplinas", icon=":material/grading:")
pagina_biblioteca = st.Page("menus/pagina_biblioteca.py", title="Biblioteca", icon=":material/local_library:")

# Cria o menu lateral do frontend
menus = {
  "Aluno": [pagina_aluno], 
  "Endereço": [pagina_endereco],
  "Disciplinas": [pagina_disciplina],
  "Notas": [pagina_nota],
  "Biblioteca": [pagina_biblioteca]
}

pg = st.navigation(menus)

# Executa o app.py
pg.run()