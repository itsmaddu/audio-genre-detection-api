import streamlit as st
import requests

st.set_page_config(page_title="Classificador Musical", page_icon="🎧", layout="centered")

st.title("🎧 Classificador de Gêneros Musicais")
st.write("Descubra o gênero de qualquer música usando Inteligência Artificial!")

# 1. Mudamos o nome da aba para YouTube
aba_youtube, aba_upload = st.tabs(["▶️ Buscar no YouTube", "📁 Enviar Arquivo Local"])

# --- ABA 1: PESQUISA NO YOUTUBE ---
with aba_youtube:
    st.write("Digite o nome da música e do artista. A IA vai baixar o áudio e analisar 30 segundos!")
    
    # 2. Formulário para a tecla 'Enter' funcionar
    with st.form(key="form_pesquisa_youtube"):
        nome_musica = st.text_input("Qual música você quer analisar?", placeholder="Ex: Numb - Linkin Park, Californication - Red Hot...")
        botao_pesquisar = st.form_submit_button("Pesquisar e Classificar 🚀")
    
    if botao_pesquisar:
        if not nome_musica:
            st.warning("Por favor, digite o nome de uma música antes de pesquisar.")
        else:
            with st.spinner(f"Buscando '{nome_musica}' no YouTube e analisando as batidas... 🧠"):
                try:
                    # 3. Rota atualizada para bater no YouTube
                    resposta = requests.post(
                        "http://127.0.0.1:8000/api/classificar-youtube", 
                        json={"nome_musica": nome_musica}
                    )
                    dados = resposta.json()
                    
                    if dados.get("sucesso"):
                        st.success(f"💿 Música encontrada: **{dados['nome_encontrado']}**")
                        st.success(f"🎵 Gênero Detectado: **{dados['resultado']['genero_predominante']}**")
                        st.info(f"Nível de Certeza: {dados['resultado']['confianca_porcentagem']}%")
                        
                        # 4. Trocamos o player de áudio pelo vídeo do YouTube embutido na tela!
                        st.write("Assista ao clipe oficial:")
                        st.video(dados['youtube_url'])
                    else:
                        st.error(f"Ops! {dados.get('detail', 'Erro ao processar a música.')}")
                        
                except Exception as e:
                    st.error(f"Erro real da máquina: {e}")

# --- ABA 2: UPLOAD DE ARQUIVO (Mantida igual) ---
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
                    st.error(f"Erro real da máquina: {e}")