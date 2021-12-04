import os

from typing import Optional
from bs4 import BeautifulSoup
from epub import Epub
from epub.ncx import Ncx
from weasyprint import HTML

from .errors import EpubMissingNcx, MissingTmpDirPath, TmpPathDoesntExists


class Pdf:
    def __init__(self) -> None:
        self.contents_dir = None
        self.epub = None
        self.tmp_dir_path = None

    def _ensure_pdf_output_dir(self, tmp_dir_path: Optional[str]) -> str:
        """
        Makes sure the PDF book output directory is available.

        Raises a `TmpPdfDirectoryAlreadyExists` if the `$pwd/tmp/tmp_pdf`
        already exists.

        If the `tmp_dir_path` is provided, then a `$tmp_dir_path/tmp_pdf`
        file is created inside.

        If the `tmp_dir_path` is not provided then `$pwd/tmp/tmp_pdf` is
        created.
        """
        cwd = os.getcwd()
        tmp = None

        if tmp_dir_path is None:
            tmp = os.path.join(cwd, r"tmp")
        else:
            tmp = tmp_dir_path

        if not os.path.exists(tmp):
            raise TmpPathDoesntExists

        tmp_pdf_path = os.path.join(tmp, r"tmp_pdf")
        os.makedirs(tmp_pdf_path)

        return tmp_pdf_path

    def _write(self, contents: str):
        html = HTML("HEllo")
        html.write_pdf("out.pdf")

    def from_epub(self, epub: Epub):
        self.epub = epub
        self.tmp_dir_path = epub.tmp_dir_path
        self.pages_sources = list()

        if self.epub.ncx is None:
            raise EpubMissingNcx()

        ncx = self.epub.ncx.open()
        ncx_soup = BeautifulSoup(ncx, "html.parser")
        contents = ncx_soup.find_all("content")

        for content in contents:
            source: str = content.get("src")
            page_path = source.split("#")[0]
            self.pages_sources.append(page_path)

    def write_book(self):
        if self.tmp_dir_path is None:
            raise MissingTmpDirPath()

        tmp_pdf_path = self._ensure_pdf_output_dir(self.tmp_dir_path)

        self._write(tmp_pdf_path)

        # for page_source in self.pages_sources:
        #     text_file_path = os.path.join(self.tmp_dir_path, page_source)
        #     text_file_copy_path = os.path.join(tmp_pdf_path, page_source)

        #     shutil.copy2(text_file_path, text_file_copy_path)