import os
import uuid

from converter.epub import Epub
from converter.pdf import Pdf
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

app = Flask("Rahool - EPUB to PDF Conversion")
app.config["UPLOAD_FOLDER"] = "uploads"


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"epub"}


@app.post("/api/v1/convert")
def upload_file():
    file = request.files["file"]
    working_dir_name = str(uuid.uuid4())

    if file:
        filename = secure_filename(file.filename)
        if is_allowed_file(filename):
            uploaded_file_working_dir = os.path.join(
                app.config["UPLOAD_FOLDER"], working_dir_name
            )
            os.makedirs(uploaded_file_working_dir)
            uploaded_file_name = "upload.epub"

            file.save(uploaded_file_working_dir + f"/{uploaded_file_name}")

            epub = Epub(uploaded_file_working_dir, uploaded_file_name)
            epub.open()

            pdf = Pdf()
            pdf.from_epub(epub)
            output_filename = filename.replace(".epub", ".pdf")
            output_path = pdf.write_book(output_filename)

            return send_file(output_path)

    return "No file provided"


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
