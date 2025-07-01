
from flask import Flask, render_template, request, send_file, redirect, flash
import yt_dlp
import os
import uuid

app = Flask(__name__)
app.secret_key = "your_secret_key"

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['videoURL']
    quality = request.form['quality']
    custom_name = request.form.get('filename', '').strip()

    if not url:
        flash("Please enter a video URL.")
        return redirect('/')

    try:
        filename = custom_name + ".mp4" if custom_name else str(uuid.uuid4()) + ".mp4"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        flash("Error: " + str(e))
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
