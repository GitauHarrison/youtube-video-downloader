# Save YouTube Video Downloader

![save](app/static/images/save.png)

_April 2023: The [PyTube](https://pytube3.readthedocs.io/en/latest/) package has a lot of issues that make using it unsatisfactory. From REGEX errors to the package breaking down all of a sudden. As a result, the current application does not work. Until a time I will be interested in a fix, I will leave it at that: Unfortunately the URL does not get processed. The only upgrade to the project is UI enhancementst to utilize Tailwind CSS._

## Overview
Want to download any YouTube video? No problem! Just type in the URL of the video and press the download button.

The application allows an anonymous user to download any YouTube video. Instances where certain URLs are not allowed include:
- URL from a local machine ex. http://127.0.0.0:5000
- Empty URL
- URL from a non-YouTube video

The user will be shown a friendly and polite error message if the URL is not valid.

## Tools Used

- Flask and python
- Bootstrap and custom CSS
- Pytube

## Other Details

| Design    |  Contribution   | Licence | Demo |
| --- | --- |  --- | --- |
|  [Figma](https://www.figma.com/proto/TAHwcWIrhvHNMvqmjQBkV1/bold-YT-downloader?node-id=0%3A3&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=4%3A31)   |  [![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/youtube-video-downloader)](https://github.com/GitauHarrison/youtube-video-downloader/graphs/contributors)   | [MIT](LICENCE) | [On Render](https://save-yt-downloader.onrender.com)


## Test Locally

- Clone this repo:

    ```python
    $ git clone git@github.com:GitauHarrison/youtube-video-downloader.git
    ```

- Change directory to the cloned repo:

    ```python
    $ cd youtube-video-downloader
    ```

- Create and active your virtual environment:

    ```python
    $ mkvirtualenv venv
    ```

- Install project dependencies:

    ```python
    (venv)$ pip3 install -r requirements.txt
    ```

- Run the flask server:

    ```python
    (venv)$ flask run
    ```

- Paste the localhost link in your browser to see the application

## Pytube Usage

- Install `pytube` from PyPI with `pip` in your virtual environment:

    ```python
    (venv)$ python -m pip install pytube
    ```

- To install from source, in the event PyPI becomes outdated, run:

    ```python
    (venv)$ python -m pip install git+https://github.com/pytube/pytube
    ```

- To quickly download a YouTube video, you can do so in your terminal as follows:

    ```python
    (venv)$ pytube https://youtube.com/watch?v=2lAe1cqCOXo
    ```

- To create a download script, you can do:

    ```python
    >>> from pytube import YouTube

    # Download the video from YouTube in your current working directory
    >>> yt = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ").streams.get_highest_resolution().download()

    # Choose a different directory to download the video to
    >>> yt = YouTube("https://www.youtube.com/watch?v=dQw4w9WgXcQ").streams.get_highest_resolution().download("/path/to/download/location")

    # Get whatever information you want about the video, ex. title, description, etc.
    >>> yt.title
    >>> yt.description
    >>> yt.thumbnail_url
    ```

## Help Needed

Working with flask bootstrap forms is quick and easy. However, I am not able to get around a particular error in this second attempt at downloading a video:

```python
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = DownloadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            url = form.url.data
            if url:
                try:
                    yt = YouTube(url)
                    yt.check_availability()
                    flash(f'Downloading {title}')
                except Exception as e:
                    flash('Error: invalid link')
                    return redirect(url_for('index'))
                return redirect(url_for('download', url=url))
    return render_template('index.html', title='Home', form=form)


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        url = request.args.get('url')
        parsed = urlparse(url)
        download_url = f'{parsed.geturl()}'
        buffer = BytesIO()
        yt = YouTube(download_url) # < ----------- causes error here
        itag = request.form['itag']
        video = yt.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(
            buffer,
            attachment_filename=f'{yt.title}.mp4',
            as_attachment=True)
    else:
        url = request.args.get('url')
        parsed = urlparse(url)
        download_url = f'{parsed.geturl()}'
        yt = YouTube(download_url)
        form = ConvertForm()        
        resolution = yt.streams.filter(progressive=True)
        return render_template(
            'download.html',            
            form=form,
            resolution=resolution)
```

Clicking the 'Download' button in the Download page causes `pytube` to highlight this regex error:

```python
pytube.exceptions.RegexMatchError: regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*
```

It might be another bug in the `extract.py` file after updating the `cipher.py` file to the latest regex version from

```python
class Cipher:
    def __init__(self, js: str):
        # ...
        var_regex = re.compile(r"^\w+\W")
        # ...
```

to:

```python
class Cipher:
    def __init__(self, js: str):
        # ...
        var_regex = re.compile(r"^\$*\w+\W")
        # ...
```

See the patch [here](https://github.com/pytube/pytube/issues/1199).