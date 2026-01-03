from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url')
        try:
            ydl_opts = {'format': 'best', 'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get('url')
        except Exception as e:
            error = "Impossible de récupérer la vidéo. Vérifiez le lien."

    return render_template('index.html', video_url=video_url, error=error)

if __name__ == '__main__':
    app.run(debug=True)