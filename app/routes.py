from app import app
from flask import render_template, request, redirect, url_for, flash, send_file, session
from pytube import YouTube
from io import BytesIO


@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    """
    When the form is submitted, the video link is
    parsed and made ready for download.
    """
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()

            def find_video_length():
                duration = url.length
                hours = duration // 3600
                minutes = duration // 60
                seconds = duration % 60
                video_length = str(hours) + ':' + str(minutes) + ':' + str(seconds)
                return video_length
            video_duration = find_video_length()
            resolution = url.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
            flash(f'Downloading {url.title}')
        except:
            flash('Error: invalid link or no link provided')
            return redirect(url_for('index'))
        return render_template(
            "download.html",
            url=url,
            video_duration=video_duration,
            resolution=resolution)
    return render_template("index.html", title="Home")


@app.route("/download", methods = ["GET", "POST"])
def download():
    """Downloads the video and saves it to the user's computer"""
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, attachment_filename=f'{url.title}.mp4',
                        as_attachment=True, mimetype='video/mp4')
    return redirect(url_for("index"))
