from app import app
from flask import render_template


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
