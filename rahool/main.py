import os

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask("Rahool - EPUB to PDF Conversion")
app.config["UPLOAD_FOLDER"] = "uploads"


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"epub", "png"}


@app.post("/api/v1/convert")
def upload_file():
    file = request.files["file"]

    if file:
        filename = secure_filename(file.filename)
        if is_allowed_file(filename):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return filename

    return "no file"


@app.route("/")
def index():
    return """
    <!doctype html>
    <title>Welcome to Rahool!</title>
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data" action="/api/v1/convert" />
      <input type="file" name="file" />
      <input type="submit" value="Upload" />
    </form>
    """


app.run("0.0.0.0", 5000)
