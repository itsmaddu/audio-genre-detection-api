import os
from transformers import pipeline


token_hf = os.getenv("HF_TOKEN")

def classificar_genero(caminho_audio):
    try:
        
        pipe = pipeline(
            "audio-classification", 
            model="superb/wav2vec2-base-superb-gtzan",
            token=token_hf
        )
        
        resultados = pipe(caminho_audio, top_k=None)
        return {"sucesso": True, "dados": resultados}
        
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}