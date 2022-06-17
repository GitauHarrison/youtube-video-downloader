from app import app
from flask import render_template, request, redirect, url_for, flash, send_file, session
from pytube import YouTube
from io import BytesIO


@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        print(session['link'])
        try:
            url = YouTube(session['link'])
            url.check_availability()
            print(url)
            flash(f'Downloading {url.title}')
        except:
            flash('Error: invalid link')
        return render_template("download.html", url = url)
    return render_template("index.html", title="Home")

@app.route("/download", methods = ["GET", "POST"])
def download():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        print(url)
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, attachment_filename=f'{url.title}.mp4',
                        as_attachment=True, mimetype='video/mp4')
    return redirect(url_for("index"))