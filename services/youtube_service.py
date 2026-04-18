import os
import yt_dlp
from pydub import AudioSegment

def buscar_e_baixar_audio(pesquisa: str):
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
            # scsearch1 busca no SoundCloud para evitar bloqueios do YouTube
            info = ydl.extract_info(f"scsearch1:{pesquisa}", download=True)
            video_info = info['entries'][0] if 'entries' in info else info
            
            titulo = video_info.get('title', 'Música Desconhecida')
            caminho_original = os.path.join(pasta_destino, 'temp_full.mp3')
            caminho_30s = os.path.join(pasta_destino, 'preview_audio.mp3')

        # O nosso novo corte focado no refrão (40s a 70s)
        audio = AudioSegment.from_file(caminho_original)
        inicio_refrao = 40 * 1000 
        fim_refrao = 70 * 1000
        audio[inicio_refrao:fim_refrao].export(caminho_30s, format="mp3")

        # Limpa o arquivo completo pesado
        if os.path.exists(caminho_original):
            os.remove(caminho_original)

        
        return {"sucesso": True, "caminho": caminho_30s, "titulo": titulo}

    except Exception as e:
        return {"sucesso": False, "erro": str(e)}