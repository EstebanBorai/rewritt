import os
import shutil


class InvalidEpubFile(Exception):
    def __str__(self) -> str:
        return f'The provided EPUB file must have a ".epub" extension'


class EpubFileNotFound(Exception):
    def __str__(self) -> str:
        return "The EPUB file wasnt found in the provided path."


def copy_as_zip(path: str) -> str:
    """
    Creates a copy of the EPUB file provided as "path" and return
    the path to the copied file renamed as ZIP
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
