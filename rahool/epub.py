import os
import shutil

from zipfile import ZipFile
from bs4 import BeautifulSoup
from bs4.element import Tag


class InvalidEpubFile(Exception):
    def __str__(self) -> str:
        return f'The provided EPUB file must have a ".epub" extension.'


class EpubFileNotFound(Exception):
    def __str__(self) -> str:
        return "The EPUB file wasnt found in the provided path."


class TemporalDirectoryAlreadyExists(Exception):
    def __str__(self) -> str:
        return f"Attempted to create a temporal directory but one already exists."


class MissingNcxTagManifest(Exception):
    def __str__(self) -> str:
        return "Missing the NCX tag in the provided manifest"


class ContainerFileNotFound(Exception):
    def __str__(self) -> str:
        return "The container.xml file is missing from META-INF."


class ContaierMissingRootfile(Exception):
    def __str__(self) -> str:
        return "Mising rootfile in the current container.xml"


class ManifestNotFound(Exception):
    def __str__(self) -> str:
        return "The Ebook provided is invalid. The manifest in the OPF file is missing."


class MissingHrefForNcxTag(Exception):
    def __str__(self) -> str:
        return "The NCX tag lacks of a path to the NCX file."


def cleanup(tmp_dir_path: str, zip_copy_path: str):
    """
    Removes directories and files created by this procedure
    """
    shutil.rmtree(tmp_dir_path)
    os.remove(zip_copy_path)


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


def open_ncx(tmp_dir_path: str):
    """
    Retrieves the Navigation Control XML (NCX) file contained in EPUB files as
    pointed out in the EPUB eBook Specification.

    The NCX XML file is usually located under META-INF directory on the top
    level directory. The file name must be "container.xml".

    ## References

    Refer: https://www.w3.org/publishing/epub3/epub-packages.html#sec-opf2-ncx
    """
    try:
        container_file_path = f"{tmp_dir_path}/META-INF/container.xml"
        with open(container_file_path, "r") as container:
            contents = container.read()
            soup = BeautifulSoup(contents, "html.parser")
            rootfiles = soup.find_all("rootfile")

            if len(rootfiles) > 0:
                return read_ncx_file(tmp_dir_path, rootfiles)

            raise ContaierMissingRootfile
    except FileNotFoundError:
        # The actual error at this point is a "FileNotFound", but in order to
        # give more context we are actually raising a "NcxNotFound" exception.
        raise ContainerFileNotFound


def read_ncx_file(tmp_dir_path, rootfiles):
    """
    Locate a NCX file following the provided "rootfiles" entry.

    The rootfile will point to the OPF file path which contains the path
    to the NCX file.
    """
    rootfile_entry = rootfiles[0]
    opf_file_path = rootfile_entry.get("full-path")

    absolute_opf_file_path = f"{tmp_dir_path}/{opf_file_path}"

    with open(absolute_opf_file_path, "r") as opf_file:
        soup = BeautifulSoup(opf_file.read(), "lxml")
        manifest: Tag | None = soup.find("manifest")  # type: ignore

        if manifest is None:
            raise ManifestNotFound

        ncx_tag: Tag | None = manifest.find(id="ncx")  # type: ignore

        if ncx_tag is None:
            raise MissingNcxTagManifest

        ncx_file_path = ncx_tag.get("href")

        if ncx_file_path is None:
            raise MissingHrefForNcxTag

        absolute_ncx_file_path = f"{tmp_dir_path}/{ncx_file_path}"
        with open(absolute_ncx_file_path, "r") as ncx_file:
            return ncx_file.read()


def into_pdf(path: str):
    try:
        zip_copy_path = copy_as_zip(path)
        tmp_dir_path = create_temporal_directory()
        extract_zip(zip_copy_path, tmp_dir_path)
        print(open_ncx(tmp_dir_path))
        cleanup(tmp_dir_path, zip_copy_path)
    except TemporalDirectoryAlreadyExists:
        print(
            'A "tmp" directory already exists in the current working directory.\nRemove it before proceeding'
        )
