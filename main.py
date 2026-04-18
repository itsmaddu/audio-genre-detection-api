import os
from transformers import pipeline

# Mantendo a variável para evitar erros no seu app.py
DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    try:
        # Puxamos o token para garantir o acesso livre
        token_hf = os.getenv("HF_TOKEN")
        
        # Modelo 100% verificado, ativo e super estável no Space
        pipe = pipeline(
            "audio-classification", 
            model="SeyedAli/Musical-genres-Classification-Hubert-V1",
            token=token_hf
        )
        
        resultados = pipe(caminho_audio, top_k=None)
        return {"sucesso": True, "dados": resultados}
        
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}