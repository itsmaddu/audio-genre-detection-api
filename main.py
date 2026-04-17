import torch
from transformers import pipeline
import os

DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    try:
        # Modelo oficial de música
        pipe = pipeline("audio-classification", model="dima806/music-genre-classification")
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados
        }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}