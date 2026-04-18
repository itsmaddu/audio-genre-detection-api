import os
from transformers import pipeline

# Adicionamos isto de volta para manter o código limpo
DIRETORIO_TEMP = "temp_audio"

# Esta linha vai buscar o Token que você salvou nos Secrets do Space
token_hf = os.getenv("HF_TOKEN")

def classificar_genero(caminho_audio):
    try:
        # Usamos o modelo 'anton-l' que é mais leve e estável para Spaces
        pipe = pipeline(
            "audio-classification", 
            model="anton-l/wav2vec2-base-superb-gtzan",
            token=token_hf
        )
        
        resultados = pipe(caminho_audio, top_k=None)
        return {"sucesso": True, "dados": resultados}
        
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}