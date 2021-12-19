import os
import uuid

from converter.epub import Epub
from converter.pdf import Pdf
from flask import Flask, request, send_file, send_from_directory, redirect
from flask.helpers import safe_join
from werkzeug.utils import secure_filename

app = Flask("rewritt - EPUB to PDF Conversion")
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


@app.route("/<path:path>")
def _static(path):
    if os.path.isdir(safe_join("static", path)):
        path = os.path.join(path, "index.html")
    return send_from_directory("static", path)


@app.route("/")
def index():
    return redirect("/index.html", 302)


app.run("0.0.0.0", os.environ["PORT"])
