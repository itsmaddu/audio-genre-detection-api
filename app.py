import streamlit as st
import plotly.express as px
import os
from main import classificar_genero, DIRETORIO_TEMP
from services.youtube_service import buscar_e_baixar_audio

st.set_page_config(page_title="Classificador Musical", page_icon="🎧")

# MATANDO O ERRO: Inicializamos a variável aqui no topo do script
caminho_local = None 

st.markdown("# 🎧 Classificador de Gêneros Musicais")
st.write("Desenvolvido por Duda. Link público e estável!")

busca = st.text_input("Qual música você quer analisar?", placeholder="Ex: Dynamite - BTS")

if st.button("Pesquisar e Classificar 🚀"):
    if busca:
        with st.spinner("Buscando e processando áudio..."):
            resultado_download = buscar_e_baixar_audio(busca)
            
            if resultado_download["sucesso"]:
                # Aqui ela recebe valor, mas o Pylance já está calmo porque viu o 'None' lá em cima
                caminho_local = resultado_download["caminho"]
                nome_musica = resultado_download["titulo"]
                
                st.success(f"✅ Encontrado: {nome_musica}")
                
                resultado_ia = classificar_genero(caminho_local)
                
                if resultado_ia["sucesso"]:
                    dados = resultado_ia["dados"]
                    top_genero = dados[0]['label'].capitalize()
                    
                    st.subheader(f"🎵 Gênero Predominante: {top_genero}")
                    
                    # Gráfico de Pizza
                    df_pizza = {
                        "Gênero": [d['label'].capitalize() for d in dados[:5]],
                        "Confiança": [d['score'] for d in dados[:5]]
                    }
                    
                    fig = px.pie(
                        df_pizza, values='Confiança', names='Gênero', 
                        title='Análise de Probabilidade', hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    st.plotly_chart(fig)
                    st.audio(caminho_local)
                else:
                    st.error(f"Erro na IA: {resultado_ia.get('erro')}")
            else:
                st.error(f"Erro no download: {resultado_download.get('erro')}")
    else:
        st.warning("Por favor, digite o nome de uma música.")

st.markdown("---")