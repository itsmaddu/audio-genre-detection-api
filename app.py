import streamlit as st
import plotly.express as px
import os
from main import classificar_genero
from services.youtube_service import buscar_e_baixar_audio
from pydub import AudioSegment

# Configuração da página
st.set_page_config(page_title="Classificador Musical", page_icon="🎧")

# Definição do diretório temporário (mesmo do main.py)
DIRETORIO_TEMP = "temp_audio"

# Garante que a pasta temporária existe para não dar erro de sistema
if not os.path.exists(DIRETORIO_TEMP):
    os.makedirs(DIRETORIO_TEMP)

# Inicialização de variáveis de controle
caminho_local = None 
nome_musica = ""

st.markdown("# 🎧 Classificador de Gêneros Musicais")
st.write("Desenvolvido por Maddu. Link público e estável!")

# Criando abas para organizar a interface entre Busca e Upload
aba_busca, aba_upload = st.tabs(["🔍 Buscar Música", "📁 Enviar Arquivo MP3"])

# --- ABA 1: BUSCA VIA YOUTUBE/SOUNDCLOUD ---
with aba_busca:
    busca = st.text_input("Qual música você quer analisar?", placeholder="Ex: Dynamite - BTS")
    if st.button("Pesquisar e Classificar 🚀"):
        if busca:
            with st.spinner("Buscando e processando áudio..."):
                resultado_download = buscar_e_baixar_audio(busca)
                
                if resultado_download["sucesso"]:
                    caminho_local = resultado_download["caminho"]
                    nome_musica = resultado_download["titulo"]
                    st.success(f"✅ Encontrado: {nome_musica}")
                else:
                    st.error(f"Erro no download: {resultado_download.get('erro')}")
        else:
            st.warning("Por favor, digite o nome de uma música.")

# --- ABA 2: UPLOAD DE ARQUIVO LOCAL ---
with aba_upload:
    arquivo_mp3 = st.file_uploader("Escolha um arquivo MP3", type=["mp3"])
    if st.button("Classificar Arquivo Carregado 🎶"):
        if arquivo_mp3:
            with st.spinner("Processando e isolando o refrão do seu arquivo..."):
                
                # Salva o arquivo original primeiro
                caminho_original = os.path.join(DIRETORIO_TEMP, "original_" + arquivo_mp3.name)
                with open(caminho_original, "wb") as f:
                    f.write(arquivo_mp3.getbuffer())
                
                # Define o caminho final que a IA vai ler
                caminho_local = os.path.join(DIRETORIO_TEMP, "cut_" + arquivo_mp3.name)
                
                # Aplica o corte para pegar a batida principal (40s a 70s)
                audio = AudioSegment.from_file(caminho_original)
                inicio = 40 * 1000
                fim = 70 * 1000
                audio[inicio:fim].export(caminho_local, format="mp3")
                
                nome_musica = arquivo_mp3.name
                st.success(f"✅ Arquivo processado e refrão isolado: {nome_musica}")
        else:
            st.warning("Por favor, selecione um arquivo MP3.")

# --- LÓGICA DE PROCESSAMENTO DA IA (Comum às duas formas de entrada) ---
if caminho_local and os.path.exists(caminho_local):
    st.markdown("---")
    with st.spinner("IA analisando as frequências musicais..."):
        resultado_ia = classificar_genero(caminho_local)
        
        if resultado_ia["sucesso"]:
            dados = resultado_ia["dados"]
            top_genero = dados[0]['label'].capitalize()
            
            st.subheader(f"🎵 Gênero Predominante: {top_genero}")
            
            # --- TRATAMENTO DE DADOS PARA PRECISÃO ---
            # Transformando decimais em porcentagens arredondadas para o gráfico
            generos = [d['label'].capitalize() for d in dados[:5]]
            confiancas = [round(d['score'] * 100, 2) for d in dados[:5]]
            
            df_pizza = {
                "Gênero": generos,
                "Confiança (%)": confiancas
            }
            
            # Criando o gráfico de pizza (Donut Chart)
            fig = px.pie(
                df_pizza, values='Confiança (%)', names='Gênero', 
                title='Análise de Probabilidade Detalhada', hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            # Refinando a visualização do gráfico
            fig.update_traces(
                textposition='inside', 
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Precisão da IA: %{value}%<extra></extra>'
            )
            
            st.plotly_chart(fig)
            
            # Player de áudio para conferência
            st.audio(caminho_local)
        else:
            st.error(f"Erro na análise da IA: {resultado_ia.get('erro')}")

st.markdown("---")