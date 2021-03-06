import os
import shutil

from zipfile import ZipFile

from .errors import (
    InvalidEpubFile,
    EpubFileNotFound,
    FailedToDispose,
    TemporalDirectoryAlreadyExists,
)
from .ncx import Ncx


def cleanup(tmp_dir_path: str, zip_copy_path: str):
    """
    Removes directories and files created by this procedure
    """
    shutil.rmtree(tmp_dir_path)
    os.remove(zip_copy_path)


class Epub:
    def __init__(self, working_dir: str, filename: str) -> None:
        self.filename = filename
        self.path = working_dir
        self.fullpath = os.path.join(working_dir, filename)
        self.tmp_dir_path = None
        self.ncx = None

    def open(self):
        if self.ncx is not None:
            return self.ncx

        try:
            self.zip_copy_path = self._copy_as_zip(self.fullpath)
            self.tmp_dir_path = self._create_temporal_directory()
            self._extract_zip(self.zip_copy_path, self.tmp_dir_path)

            # Retrieve NCX file contents
            ncx = Ncx(self.tmp_dir_path)
            ncx.open()
            self.ncx = ncx

        except TemporalDirectoryAlreadyExists:
            print(
                'A "tmp" directory already exists in the current working directory.\nRemove it before proceeding'
            )

    def dispose(self):
        """
        Removes directories and files created by this procedure
        """
        if self.tmp_dir_path is None:
            raise FailedToDispose(
                f"The temportal directory is not defined. Value is: {self.tmp_dir_path}"
            )
        else:
            shutil.rmtree(self.tmp_dir_path)
            os.remove(self.zip_copy_path)

    def _copy_as_zip(self, path: str) -> str:
        """
        Creates a copy of the EPUB file provided as "path" and return the path to
        the copied file renamed as ZIP.
        """
        filepath = self.path + '/' + self.filename

        if filepath.endswith(".epub"):
            if os.path.isfile(filepath):
                new_name = path.replace(".epub", ".zip")
                shutil.copyfile(path, new_name)

                return new_name
            else:
                raise EpubFileNotFound
        else:
            raise InvalidEpubFile

    def _create_temporal_directory(self) -> str:
        """
        Attempts to create a "tmp" directory in the current working directory.
        Returns the path to the created directory if successful.
        """
        tmp = os.path.join(self.path, r"tmp")

        if not os.path.exists(tmp):
            os.makedirs(tmp)

            return tmp
        else:
            raise TemporalDirectoryAlreadyExists

    def _extract_zip(self, zip_file_path: str, extract_dir_path: str):
        """
        Extracts contentes compressed in the ZIP file provided into the
        "extract_dir_path".
        """
        with ZipFile(zip_file_path, "r") as zip:
            zip.extractall(extract_dir_path)
