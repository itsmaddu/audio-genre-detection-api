import os
import shutil
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Importando os nossos serviços
from services.audio_service import classificar_genero
from services.youtube_service import procurar_e_baixar_youtube

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
@app.post("/api/classificar-youtube")
async def classificar_via_youtube(pesquisa: PesquisaSpotify): # Podemos manter o modelo com esse nome por enquanto
    
    # Passo 1: Pede ao serviço do YouTube para achar, baixar e cortar
    caminho_30s, titulo, url_video = procurar_e_baixar_youtube(pesquisa.nome_musica, DIRETORIO_TEMP)

    if not caminho_30s:
        raise HTTPException(status_code=404, detail=titulo) # O título aqui contém o erro

    try:
        # Passo 2: Entregamos os 30s cortados para a IA
        resultado_ia = classificar_genero(caminho_30s)

        # Passo 3: Devolvemos os dados para o frontend
        return {
            "sucesso": True,
            "nome_encontrado": titulo,
            "youtube_url": url_video,
            "resultado": resultado_ia
        }

    except Exception as erro:
        raise HTTPException(status_code=500, detail=str(erro))
    finally:
        # Passo 4: A faxina final
        if caminho_30s and os.path.exists(caminho_30s):
            os.remove(caminho_30s)

@app.get("/")
async def raiz():
    return {
        "mensagem": "Bem-vindo à API de Classificação Musical!",
        "status": "Online e operante 🚀",
        "documentacao": "Acesse /docs para ver os endpoints."
    }