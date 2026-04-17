import torch
from transformers import pipeline
import os

# Configurações de diretório
DIRETORIO_TEMP = "temp_audio"
if not os.path.exists(DIRETORIO_TEMP):
    os.makedirs(DIRETORIO_TEMP)

# Carrega o modelo de IA (O Hugging Face vai baixar isso no primeiro boot)
# Usando um modelo popular de classificação de gênero

print("Carregando motor de IA...")
pipe = pipeline("audio-classification", model="anton-l/wav2vec2-base-superb-gtzan")

def classificar_genero(caminho_audio):
    """
    Função que recebe o caminho do arquivo e retorna o gênero musical
    """
    try:
        # A mágica acontece aqui
        resultado = pipe(caminho_audio)
        
        # Pegamos o resultado com maior score
        top_result = resultado[0]
        
        return {
            "genero_predominante": top_result['label'].capitalize(),
            "confianca_porcentagem": round(top_result['score'] * 100, 2)
        }
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return {
            "genero_predominante": "Desconhecido",
            "confianca_porcentagem": 0
        }