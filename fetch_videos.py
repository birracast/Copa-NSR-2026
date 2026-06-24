import os
import json
from googleapiclient.discovery import build

# Pegando a chave da API salva no GitHub Secrets
API_KEY = os.environ.get('YOUTUBE_API_KEY')

# Substitua pelo ID da PLAYLIST (Fica na URL do YouTube depois de "list=")
PLAYLIST_ID = 'PLZuM_Kl1KELkV0PiJMj-zr5gJ9zVKhBvC' 

def fetch_latest_videos():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Busca os 5 primeiros vídeos da playlist especificada
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=PLAYLIST_ID,
        maxResults=5
    )
    response = request.execute()

    videos = []
    for item in response.get('items', []):
        snippet = item['snippet']
        
        # Pega a melhor thumbnail disponível (tenta 'medium', se não achar pega 'default')
        thumbnails = snippet.get('thumbnails', {})
        thumb_url = thumbnails.get('medium', thumbnails.get('default', {})).get('url', '')

        videos.append({
            'title': snippet['title'],
            'videoId': snippet['resourceId']['videoId'],
            'thumbnail': thumb_url
        })

    # Salva o resultado em um arquivo JSON que seu HTML vai ler
    with open('videos.json', 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    fetch_latest_videos()
