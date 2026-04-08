from transformers import pipeline

print("Carregando modelo de IA... Isso pode levar alguns segundos na primeira vez.")
classificador_ia = pipeline(
    "audio-classification", 
    model="dima806/music_genres_classification"
)
print("Modelo carregado com sucesso!")

def classificar_genero(caminho_do_arquivo: str) -> dict:
    try:
        resultados = classificador_ia(caminho_do_arquivo)
        
        if not resultados:
            raise ValueError("O modelo não conseguiu classificar o áudio.")

        melhor_palpite = resultados[0]
        
        resposta = {
            "genero_predominante": melhor_palpite["label"].capitalize(),
            "confianca_porcentagem": round(melhor_palpite["score"] * 100, 2),
            "top_3_resultados": resultados[:3]
        }
        
        return resposta

    except Exception as erro:
        raise Exception(f"Erro ao processar o áudio com a IA: {str(erro)}")