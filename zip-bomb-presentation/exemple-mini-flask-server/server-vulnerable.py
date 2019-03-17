import os
import secrets
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "images"

app = Flask(__name__, template_folder=".")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.run(debug=True)


@app.route("/images/<path:path>")
def send_images(path):
    return send_from_directory(UPLOAD_FOLDER, path)


@app.route("/add", methods=["POST"])
def add_image():
    files = request.files.getlist(UPLOAD_FOLDER)
    for file in files:
        filename = str(int(time.time())) + "-" + secrets.token_urlsafe(5) + ".png"
        path = UPLOAD_FOLDER + "/" + filename
        file.save(path)
    return redirect("/")


@app.route("/")
def gallery():
    images = map(lambda filename: UPLOAD_FOLDER + "/" +
                 filename, os.listdir(UPLOAD_FOLDER))
    return render_template("gallery.html", img=images)
