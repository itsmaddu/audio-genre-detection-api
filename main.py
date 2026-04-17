from transformers import pipeline
import os

DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    # Lista de modelos estáveis (se um falhar, tenta o outro)
    modelos = [
        "superb/wav2vec2-base-superb-gtzan", 
        "anton-l/wav2vec2-base-superb-gtzan"
    ]
    
    ultimo_erro = ""
    
    for nome_modelo in modelos:
        try:
            # O 'trust_remote_code' ajuda em alguns servidores
            pipe = pipeline("audio-classification", model=nome_modelo)
            resultados = pipe(caminho_audio, top_k=None)
            return {"sucesso": True, "dados": resultados}
        except Exception as e:
            ultimo_erro = str(e)
            continue # Tenta o próximo modelo da lista
            
    return {"sucesso": False, "erro": f"Nenhum modelo carregou. Erro: {ultimo_erro}"}