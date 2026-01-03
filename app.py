from flask import Flask, render_template, request, Response, stream_with_context
import yt_dlp
import requests


app = Flask(__name__)

def get_video_info(url):
    """Extrait l'URL directe de la vidéo Facebook"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return info.get('url'), info.get('title', 'video_fb')
        except Exception:
            return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        direct_link, title = get_video_info(url)
        if direct_link:
            video_url = direct_link
        else:
            error = "Impossible de récupérer cette vidéo. Vérifiez le lien ou réessayez."

    return render_template('index.html', video_url=video_url, error=error)

@app.route('/download')
def download():
    """Force le téléchargement du fichier au lieu de la lecture"""
    video_url = request.args.get('url')
    if not video_url:
        return "URL manquante", 400

    # On récupère le flux vidéo de Facebook
    req = requests.get(video_url, stream=True)

    # On définit les headers pour forcer le téléchargement
    headers = {
        'Content-Disposition': 'attachment; filename="video_facebook.mp4"',
        'Content-Type': 'video/mp4'
    }

    # On renvoie le flux petit à petit (Streaming) pour ne pas saturer la RAM
    return Response(
        stream_with_context(req.iter_content(chunk_size=1024*1024)),
        headers=headers
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)