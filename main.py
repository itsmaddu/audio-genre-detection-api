import os
from transformers import pipeline


DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    try:
        
        token_hf = os.getenv("HF_TOKEN")
        
        # Modelo m-a-p: Rápido, leve e excelente para Gêneros Musicais
        pipe = pipeline(
            "audio-classification", 
            model="m-a-p/music-genre-classification",
            token=token_hf
        )
        
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados
        }
    except Exception as e:
       
        return {"sucesso": False, "erro": str(e)}