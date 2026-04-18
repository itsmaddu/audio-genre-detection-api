import os
import yt_dlp
from pydub import AudioSegment

def buscar_e_baixar_audio(pesquisa: str):
    """
    Pesquisa no SoundCloud, baixa e corta 30s.
    """
    pasta_destino = "temp_audio"
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_destino, 'temp_full.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # scsearch1 busca no SoundCloud
            info = ydl.extract_info(f"scsearch1:{pesquisa}", download=True)
            video_info = info['entries'][0] if 'entries' in info else info
            
            titulo = video_info.get('title', 'Música Desconhecida')
            caminho_original = os.path.join(pasta_destino, 'temp_full.mp3')
            caminho_30s = os.path.join(pasta_destino, f"preview_{info.get('id', 'audio')}.mp3")

        # Cortando os 30 segundos
        audio = AudioSegment.from_file(caminho_original)
        inicio_refrao = 40 * 1000 # 40 segundos em milissegundos
        fim_refrao = 70 * 1000
        
        audio[inicio_refrao:fim_refrao].export(caminho_30s, format="mp3")
    except Exception as e:
        print(f"Erro: {e}")