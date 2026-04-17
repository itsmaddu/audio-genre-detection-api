import torch
from transformers import pipeline
import os

def classificar_genero(caminho_audio):
    try:
        # Modelo focado em Gênero Musical (GTZAN)
        pipe = pipeline("audio-classification", model="dima806/music-genre-classification")
        
        # Pedimos para retornar todos os gêneros (top_k=None)
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados # Retorna a lista completa para o gráfico
        }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}
    