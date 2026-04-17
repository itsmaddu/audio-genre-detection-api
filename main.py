from transformers import pipeline
import os

# Definimos o diretório para evitar erros de importação
DIRETORIO_TEMP = "temp_audio"

def classificar_genero(caminho_audio):
    try:
        # Carregamos a IA direto aqui para garantir que ela use o cache do servidor
        # Usaremos o modelo 'anton-l', que é muito leve e estável
        pipe = pipeline("audio-classification", model="anton-l/wav2vec2-base-superb-gtzan")
        
        resultados = pipe(caminho_audio, top_k=None)
        
        return {
            "sucesso": True,
            "dados": resultados
        }
    except Exception as e:
        # Se falhar, ele vai nos dizer o motivo real (ex: falta de memória)
        return {"sucesso": False, "erro": str(e)}