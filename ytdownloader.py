import yt_dlp

def list_formats(video_url):
    ydl_opts = {
        'listformats': True,  # Liste tous les formats disponibles
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(video_url, download=False)

def download_youtube_video(video_url, format_code):
    ydl_opts = {
        'format': format_code,  # Utilise le format spécifié
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Demander l'URL de la vidéo à l'utilisateur
video_url = input("Veuillez entrer l'URL complète de la vidéo YouTube : ")
# video_url = "https://www.youtube.com/watch?v=Yu0B903O_CA"

# Lister les formats disponibles
list_formats(video_url)

# Demander le code du format souhaité
format_code = input("Veuillez entrer le code du format à télécharger (ex: 137+140) : ")


try:
    print(f"Téléchargement de la vidéo dans le format {format_code}...")
    download_youtube_video(video_url, format_code)
    print("Téléchargement terminé avec succès.")
except ValueError as e:
    print(e)