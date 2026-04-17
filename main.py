import torch
from transformers import pipeline
import os

DIRETORIO_TEMP = "temp_audio"

print("Iniciando motor de IA...")
try:
    pipe = pipeline("audio-classification", model="superb/wav2vec2-base-superb-gtzan")
except Exception as e:
    pipe = None
    print(f"Erro ao carregar modelo: {e}")

def classificar_genero(caminho_audio):
    if pipe is None:
        return {"sucesso": False, "erro": "A IA não carregou corretamente. Verifique os Logs."}
    
    try:
        # Realiza a classificação
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados
        }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}