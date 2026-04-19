import streamlit as st
import plotly.express as px
import os
from pydub import AudioSegment
from main import classificar_genero
from services.youtube_service import buscar_e_baixar_audio

st.set_page_config(page_title="Classificador Musical", page_icon="🎧")

DIRETORIO_TEMP = "temp_audio"
if not os.path.exists(DIRETORIO_TEMP):
    os.makedirs(DIRETORIO_TEMP)

caminho_local = None 
nome_musica = ""

st.markdown("# 🎧 Classificador de Gêneros Musicais")
st.write("Desenvolvido por Maddu. Link público e estável!")

aba_busca, aba_upload = st.tabs(["🔍 Buscar Música", "📁 Enviar Arquivo MP3"])

# --- ABA 1: BUSCA ---
with aba_busca:
    with st.form("form_busca"):
        busca = st.text_input("Qual música você quer analisar?", placeholder="Ex: Dynamite - BTS")
        # Mantemos o botão dentro do form para o "Enter" continuar funcionando
        submit_busca = st.form_submit_button("Pesquisar e Classificar 🚀")

    if submit_busca:
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

# --- ABA 2: UPLOAD ---
with aba_upload:
    with st.form("form_upload"):
        arquivo_mp3 = st.file_uploader("Escolha uma música do seu computador", type=["mp3"])
        submit_upload = st.form_submit_button("Classificar Arquivo Carregado 🎶")
    
    if submit_upload:
        if arquivo_mp3 is not None:
            with st.spinner("Processando e isolando o refrão..."):
                caminho_original = os.path.join(DIRETORIO_TEMP, "original_" + arquivo_mp3.name)
                with open(caminho_original, "wb") as f:
                    f.write(arquivo_mp3.getbuffer())
                
                caminho_local = os.path.join(DIRETORIO_TEMP, "cut_" + arquivo_mp3.name)
                
                # Corte do refrão
                audio = AudioSegment.from_file(caminho_original)
                inicio = 40 * 1000
                fim = 70 * 1000
                audio_cortado = audio[inicio:fim]
                audio_cortado.export(caminho_local, format="mp3")
                
                nome_musica = arquivo_mp3.name
                st.success(f"✅ Arquivo processado: {nome_musica}")
        else:
            st.warning("Por favor, envie um arquivo MP3.")

# --- LÓGICA DE PROCESSAMENTO DA IA ---
if caminho_local and os.path.exists(caminho_local):
    st.markdown("---")
    with st.spinner("IA analisando as frequências musicais..."):
        resultado_ia = classificar_genero(caminho_local)
        
        if resultado_ia["sucesso"]:
            dados = resultado_ia["dados"]
            top_genero = dados[0]['label'].capitalize()
            
            st.subheader(f"🎵 Gênero Predominante: {top_genero}")
            
            generos = [d['label'].capitalize() for d in dados]
            confiancas = [round(d['score'] * 100, 2) for d in dados]
            
            df_pizza = {
                "Gênero": generos,
                "Confiança (%)": confiancas
            }
            
            fig = px.pie(
                df_pizza, values='Confiança (%)', names='Gênero', 
                title='Análise de Probabilidade Detalhada', hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            
            fig.update_traces(
                textposition='inside', 
                textinfo='label+percent',
                hovertemplate='<b>%{label}</b><br>Precisão da IA: %{value}%<extra></extra>'
            )
            
            st.plotly_chart(fig)
            
            # --- O "PULO DO GATO" PARA UX (Leigos) ---
            st.info("🔊 **Dica:** Passe o mouse no ícone de alto-falante (no canto direito do player abaixo) para ajustar o volume na hora!")
            st.audio(caminho_local)
        else:
            st.error(f"Erro na análise da IA: {resultado_ia.get('erro')}")

st.markdown("---")
st.write("Feito com ❤️ por [Maddu](https://github.com/Maddu)")