from bs4 import BeautifulSoup
from bs4.element import Tag

from .errors import (
    ContaierMissingRootfile,
    ContainerFileNotFound,
    ManifestNotFound,
    MissingNcxTagManifest,
    MissingHrefForNcxTag,
)


class Ncx:
    def __init__(self, path: str) -> None:
        self.path = path
        self.content = None

    def open(self):
        """
        Retrieves the Navigation Control XML (NCX) file contained in EPUB files as
        pointed out in the EPUB eBook Specification.

        The NCX XML file is usually located under META-INF directory on the top
        level directory. The file name must be "container.xml".

        ## References

        Refer: https://www.w3.org/publishing/epub3/epub-packages.html#sec-opf2-ncx
        """

        try:
            container_file_path = f"{self.path}/META-INF/container.xml"
            with open(container_file_path, "r") as container:
                contents = container.read()
                soup = BeautifulSoup(contents, "html.parser")
                rootfiles = soup.find_all("rootfile")

                if len(rootfiles) > 0:
                    content = self._read_ncx_file(self.path, rootfiles)
                    self.content = content

                    return content

                raise ContaierMissingRootfile
        except FileNotFoundError:
            # The actual error at this point is a "FileNotFound", but in order to
            # give more context we are actually raising a "NcxNotFound" exception.
            raise ContainerFileNotFound

    def _read_ncx_file(self, tmp_dir_path, rootfiles):
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
