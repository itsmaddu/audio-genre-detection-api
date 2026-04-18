import os
import torch
from transformers import pipeline


DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    try:
        
        token_hf = os.getenv("HF_TOKEN")
        
        pipe = pipeline(
            "audio-classification", 
            model="MIT/ast-finetuned-gtzan",
            token=token_hf
        )
        
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados
        }
        
    except Exception as e:
        
        return {"sucesso": False, "erro": str(e)}