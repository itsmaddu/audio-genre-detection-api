import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Avisa o Python para procurar e abrir o "cofre" (.env)
load_dotenv()

# 2. Pega as senhas guardadas lá dentro
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

# 3. Liga o Spotify de forma 100% segura
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

def procurar_e_baixar_preview(nome_musica):
    resultado = sp.search(q=nome_musica, limit=1, type='track')
    
    if not resultado['tracks']['items']:
        return None, "Música não encontrada."

    item = resultado['tracks']['items'][0]
    nome = item['name']
    url_preview = item['preview_url'] 
    
    if not url_preview:
        return None, "Esta música não tem uma amostra de 30 segundos disponível."
    
    return url_preview, nome