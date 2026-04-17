import torch
from transformers import pipeline
import os

DIRETORIO_TEMP = "temp_audio"
if not os.path.exists(DIRETORIO_TEMP):
    os.makedirs(DIRETORIO_TEMP)

def classificar_genero(caminho_audio):
    try:
        # Carrega o modelo só na hora de usar (evita crash no boot)
        pipe = pipeline("audio-classification", model="superb/wav2vec2-base-superb-sid")
        resultado = pipe(caminho_audio)
        top_result = resultado[0]
        return {
            "genero_predominante": top_result['label'].capitalize(),
            "confianca_porcentagem": round(top_result['score'] * 100, 2)
        }
    except Exception as e:
        return {"genero_predominante": f"Erro: {str(e)}", "confianca_porcentagem": 0}
    