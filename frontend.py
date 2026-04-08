import streamlit as st
import requests

st.set_page_config(page_title="Classificador Musical", page_icon="🎧", layout="centered")

st.title("🎧 Classificador de Gêneros Musicais")
st.write("Descubra o gênero de qualquer música usando Inteligência Artificial!")

# Criando as abas para separar as funcionalidades visualmente
aba_spotify, aba_upload = st.tabs(["🔍 Buscar no Spotify", "📁 Enviar Arquivo Local"])

# --- ABA 1: PESQUISA NO SPOTIFY ---
with aba_spotify:
    st.write("Digite o nome da música e do artista. A IA vai ouvir uma prévia de 30 segundos!")
    nome_musica = st.text_input("Qual música você quer analisar?", placeholder="Ex: Numb - Linkin Park, Californication - Red Hot...")
    
    if st.button("Pesquisar e Classificar 🚀"):
        if not nome_musica:
            st.warning("Por favor, digite o nome de uma música antes de pesquisar.")
        else:
            with st.spinner(f"Buscando '{nome_musica}' no Spotify e analisando as batidas... 🧠"):
                try:
                    # Avisamos a API (que vamos atualizar já já) para buscar o texto
                    resposta = requests.post(
                        "http://127.0.0.1:8000/api/classificar-spotify", 
                        json={"nome_musica": nome_musica}
                    )
                    dados = resposta.json()
                    
                    if dados.get("sucesso"):
                        st.success(f"💿 Música encontrada: **{dados['nome_encontrado']}**")
                        st.success(f"🎵 Gênero Detectado: **{dados['resultado']['genero_predominante']}**")
                        st.info(f"Nível de Certeza: {dados['resultado']['confianca_porcentagem']}%")
                        
                        # Bônus: Coloca o player de 30s do Spotify na tela para o usuário ouvir!
                        st.write("Ouça a prévia analisada:")
                        st.audio(dados['preview_url'])
                    else:
                        st.error(f"Ops! {dados.get('detail', 'Música não encontrada ou sem amostra.')}")
                        
                except Exception as e:
                    st.error("Erro de conexão! O servidor FastAPI está ligado?")

# --- ABA 2: UPLOAD DE ARQUIVO (O que já tínhamos feito) ---
with aba_upload:
    st.write("Ou envie um arquivo de áudio direto do seu computador (.wav, .mp3).")
    arquivo_upado = st.file_uploader("Escolha um arquivo", type=["wav", "mp3", "flac"])
    
    if arquivo_upado is not None:
        st.audio(arquivo_upado)
        if st.button("Classificar Arquivo 📂"):
            with st.spinner("A IA está analisando a música... 🧠"):
                arquivos = {"file": (arquivo_upado.name, arquivo_upado.getvalue(), arquivo_upado.type)}
                try:
                    resposta = requests.post("http://127.0.0.1:8000/api/classificar", files=arquivos)
                    dados = resposta.json()
                    
                    if dados.get("sucesso"):
                        st.success(f"🎵 Gênero Detectado: **{dados['resultado']['genero_predominante']}**")
                        st.info(f"Nível de Certeza: {dados['resultado']['confianca_porcentagem']}%")
                    else:
                        st.error("Ops! A API retornou um erro.")
                except Exception as e:
                    st.error("Erro de conexão! O servidor FastAPI está ligado?")