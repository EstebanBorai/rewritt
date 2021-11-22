import os
import shutil

from zipfile import ZipFile


class InvalidEpubFile(Exception):
    def __str__(self) -> str:
        return f'The provided EPUB file must have a ".epub" extension.'


class EpubFileNotFound(Exception):
    def __str__(self) -> str:
        return "The EPUB file wasnt found in the provided path."


class TemporalDirectoryAlreadyExists(Exception):
    def __str__(self) -> str:
        return f"Attempted to create a temporal directory but one already exists."


def into_pdf(path: str):
    zip_copy_path = copy_as_zip(path)
    tmp_dir_path = create_temporal_directory()
    extract_zip(zip_copy_path, tmp_dir_path)

    return ""


def copy_as_zip(path: str) -> str:
    """
    Creates a copy of the EPUB file provided as "path" and return the path to
    the copied file renamed as ZIP.
    """
    if path.endswith(".epub"):
        if os.path.isfile(path):
            new_name = path.replace(".epub", ".zip")
            shutil.copyfile(path, new_name)

            return new_name
        else:
            raise EpubFileNotFound
    else:
        raise InvalidEpubFile


def create_temporal_directory() -> str:
    """
    Attempts to create a "tmp" directory in the current working directory.
    Returns the path to the created directory if successful.
    """
    cwd = os.getcwd()
    tmp = os.path.join(cwd, r"tmp")

    if not os.path.exists(tmp):
        os.makedirs(tmp)

        return tmp
    else:
        raise TemporalDirectoryAlreadyExists


def extract_zip(zip_file_path: str, extract_dir_path: str):
    """
    Extracts contentes compressed in the ZIP file provided into the
    "extract_dir_path".
    """
    with ZipFile(zip_file_path, "r") as zip:
        zip.extractall(extract_dir_path)
