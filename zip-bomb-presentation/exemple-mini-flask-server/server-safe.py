import os
import secrets
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'images'

app = Flask(__name__, template_folder='.')
app.run(debug=True)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route("/add", methods=['POST'])
def add_image():
    files = request.files.getlist("images")
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, str(int(
            time.time())) + "-" + secrets.token_urlsafe(5)) + ".png")  # image type not relvantp
    return redirect("/")


@app.route("/")
def gallery():
    images = map(lambda filename: UPLOAD_FOLDER + "/" +
                 filename, os.listdir(UPLOAD_FOLDER))
    return render_template("gallery.html", img=images)
