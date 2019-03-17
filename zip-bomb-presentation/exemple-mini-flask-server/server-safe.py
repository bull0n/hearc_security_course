import os
import secrets
import time
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = 'images'
MAX_IMAGE_WIDTH = 5000
MAX_IMAGE_HEIGHT = 5000

app = Flask(__name__, template_folder='.')
app.run(debug=True)


@app.route('/images/<path:path>')
def send_images(path):
	return send_from_directory('images', path)


@app.route("/add", methods=['POST'])
def add_image():
	files = request.files.getlist("images")
	for file in files:
		filename = str(int(time.time())) + "-" + secrets.token_urlsafe(5) + ".png"
		path = UPLOAD_FOLDER + "/" + filename
		file.save(path)
		remove_invalid_image(path)
	return redirect("/")

def remove_invalid_image(path)
	invalid = False
	try:
		with Image.open(path) as img:
			width, height = img.size
			if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
				invalid = True
	except:
		invalid = True
	if invalid:
		os.remove(path)

@app.route("/")
def gallery():
	images=map(lambda filename: UPLOAD_FOLDER + "/"
				 + filename, os.listdir(UPLOAD_FOLDER))
	return render_template("gallery.html", img = images)
