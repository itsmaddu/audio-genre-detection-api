import streamlit as st
import os
from services.youtube_service import procurar_e_baixar_youtube
from main import classificar_genero, DIRETORIO_TEMP

st.set_page_config(page_title="Classificador Musical", page_icon="🎧")

st.title("🎧 Classificador de Gêneros Musicais")
st.write("Link público e estável! Desenvolvido por Duda.")

# Interface
with st.form(key="form_pesquisa"):
    nome_musica = st.text_input("Qual música você quer analisar?", placeholder="Ex: BTS - Dynamite")
    botao = st.form_submit_button("Pesquisar e Classificar 🚀")

if botao:
    if not nome_musica:
        st.warning("Digite o nome de uma música.")
    else:
        with st.spinner("Processando áudio... 🧠"):
            # Chamada direta das funções (Sem precisar de API/FastAPI rodando separado)
            caminho_30s, titulo, url_video = procurar_e_baixar_youtube(nome_musica, DIRETORIO_TEMP)
            
            if caminho_30s:
                resultado = classificar_genero(caminho_30s)
                
                st.success(f"💿 Encontrado: **{titulo}**")
                st.success(f"🎵 Gênero: **{resultado['genero_predominante']}**")
                st.info(f"Confiança: {resultado['confianca_porcentagem']}%")
                st.video(url_video)
                
                if os.path.exists(caminho_30s):
                    os.remove(caminho_30s)
            else:
                st.error("Música não encontrada no SoundCloud.")
