import os
import shutil
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importando os nossos serviços
from services.audio_service import classificar_genero
from services.spotify_service import procurar_e_baixar_preview

app = FastAPI(title="Audio Genre Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

DIRETORIO_TEMP = "temp_audio"
os.makedirs(DIRETORIO_TEMP, exist_ok=True)


# --- ESTRUTURAS DE DADOS ---

# Isso define o formato exato que a API espera receber do frontend
class PesquisaSpotify(BaseModel):
    nome_musica: str


# --- ROTAS DA API ---

# Rota 1: O Upload de Arquivo Local (O que já estava pronto)
@app.post("/api/classificar")
async def classificar_musica(file: UploadFile = File(...)):
    extensoes_permitidas = ('.wav', '.mp3', '.flac')
    if not file.filename.lower().endswith(extensoes_permitidas):
        raise HTTPException(status_code=400, detail="Envie apenas arquivos de áudio.")

    caminho_arquivo_temp = os.path.join(DIRETORIO_TEMP, file.filename)

    try:
        with open(caminho_arquivo_temp, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resultado_ia = classificar_genero(caminho_arquivo_temp)

        return {
            "sucesso": True,
            "arquivo": file.filename,
            "resultado": resultado_ia
        }

    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    finally:
        if os.path.exists(caminho_arquivo_temp):
            os.remove(caminho_arquivo_temp)


# Rota 2: A Nova Integração com o Spotify
@app.post("/api/classificar-spotify")
async def classificar_via_spotify(pesquisa: PesquisaSpotify):
    
    # Passo 1: Pede ao serviço do Spotify para achar a música
    url_preview, nome_encontrado = procurar_e_baixar_preview(pesquisa.nome_musica)

    # Se a função retornou None na URL, o nome_encontrado contém a mensagem de erro
    if not url_preview:
        raise HTTPException(status_code=404, detail=nome_encontrado) 

    # Criamos um nome padrão para o arquivo temporário baixado da internet
    caminho_arquivo_temp = os.path.join(DIRETORIO_TEMP, "preview_spotify.mp3")

    try:
        # Passo 2: Baixamos os 30 segundos de áudio do link do Spotify
        resposta_audio = requests.get(url_preview)
        with open(caminho_arquivo_temp, "wb") as arquivo:
            arquivo.write(resposta_audio.content)

        # Passo 3: Entregamos para a Inteligência Artificial analisar
        resultado_ia = classificar_genero(caminho_arquivo_temp)

        # Passo 4: Devolvemos tudo mastigado para o frontend (Streamlit)
        return {
            "sucesso": True,
            "nome_encontrado": nome_encontrado,
            "preview_url": url_preview,
            "resultado": resultado_ia
        }

    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    finally:
        # Passo 5: A faxina. Apaga a prévia para não lotar o servidor.
        if os.path.exists(caminho_arquivo_temp):
            os.remove(caminho_arquivo_temp)


@app.get("/")
async def raiz():
    return {
        "mensagem": "Bem-vindo à API de Classificação Musical!",
        "status": "Online e operante 🚀",
        "documentacao": "Acesse /docs para ver os endpoints."
    }