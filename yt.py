import yt_dlp

def download_youtube_video(video_url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

video_url = input("Veuillez entrer l'URL complète de la vidéo YouTube : ")
download_youtube_video(video_url)