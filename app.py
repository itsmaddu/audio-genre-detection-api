import streamlit as st
import plotly.express as px
import os
from main import classificar_genero, DIRETORIO_TEMP
from services.youtube_service import buscar_e_baixar_audio

# Configuração da página

st.set_page_config(page_title="Classificador Musical", page_icon="🎧")

st.markdown("# 🎧 Classificador de Gêneros Musicais")
st.write("Desenvolvido por Duda. Link público e estável!")

# Input do usuário
busca = st.text_input("Qual música você quer analisar?", placeholder="Ex: Dynamite - BTS")

if st.button("Pesquisar e Classificar 🚀"):
    if busca:
        with st.spinner("Buscando e processando áudio..."):
            # 1. Busca e Baixa o áudio (Aqui que a variável é definida!)
            resultado_download = buscar_e_baixar_audio(busca)
            
            if resultado_download["sucesso"]:
                caminho_local = resultado_download["caminho"] # <--- AQUI ELA NASCE!
                nome_musica = resultado_download["titulo"]
                
                st.success(f"✅ Encontrado: {nome_musica}")
                
                # 2. Classifica
                resultado_ia = classificar_genero(caminho_local)
                
                if resultado_ia["sucesso"]:
                    dados = resultado_ia["dados"]
                    top_genero = dados[0]['label'].capitalize()
                    
                    st.subheader(f"🎵 Gênero Predominante: {top_genero}")
                    
                    # 3. Gráfico de Pizza (Plotly)
                    df_pizza = {
                        "Gênero": [d['label'].capitalize() for d in dados[:5]],
                        "Confiança": [d['score'] for d in dados[:5]]
                    }
                    
                    fig = px.pie(
                        df_pizza, 
                        values='Confiança', 
                        names='Gênero', 
                        title='Análise de Probabilidade',
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    
                    st.plotly_chart(fig)
                    
                    # 4. Player de Áudio (Opcional, mas legal)
                    st.audio(caminho_local)
                else:
                    st.error(f"Erro na IA: {resultado_ia.get('erro')}")
            else:
                st.error(f"Erro no download: {resultado_download.get('erro')}")
    else:
        st.warning("Por favor, digite o nome de uma música.")

# Rodapé
st.markdown("---")
st.caption("Nota: O processamento pode levar alguns segundos dependendo do tamanho da música.")