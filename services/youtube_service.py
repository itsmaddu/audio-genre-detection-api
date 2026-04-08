import os
import yt_dlp
from pydub import AudioSegment
from dotenv import load_dotenv

# Puxa as informações do cofre
load_dotenv()
arquivo_de_cookies = os.getenv("CAMINHO_COOKIES")

def procurar_e_baixar_youtube(pesquisa: str, pasta_destino: str):
    """
    Pesquisa no YouTube, baixa o áudio do 1º resultado e corta os primeiros 30 segundos.
    """
    # Configurações para baixar apenas o áudio com a melhor qualidade
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(pasta_destino, 'temp_yt_full.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch', # Diz ao yt-dlp que é uma pesquisa e não um link
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        # 1. Faz a pesquisa e o download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # ytsearch1 significa: pegue apenas o 1º resultado da pesquisa
            info = ydl.extract_info(f"ytsearch1:{pesquisa}", download=True)
            
            # Acessa os dados do vídeo encontrado
            video_info = info['entries'][0] if 'entries' in info else info
            
            titulo = video_info.get('title', 'Vídeo Desconhecido')
            url_video = video_info.get('webpage_url', '')

        # 2. O arquivo original baixado
        caminho_original = os.path.join(pasta_destino, 'temp_yt_full.mp3')
        caminho_30s = os.path.join(pasta_destino, 'preview_youtube.mp3')

        # 3. Cortando os primeiros 30 segundos com a Pydub
        audio = AudioSegment.from_file(caminho_original)
        audio_cortado = audio[:30000] # O tempo é em milissegundos (30s = 30000ms)
        audio_cortado.export(caminho_30s, format="mp3")

        # 4. Faxina: apaga a música inteira para não lotar o servidor
        if os.path.exists(caminho_original):
            os.remove(caminho_original)

        return caminho_30s, titulo, url_video

    except Exception as e:
        return None, f"Erro ao processar o YouTube: {str(e)}", ""