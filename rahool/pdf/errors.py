class EpubMissingNcx(Exception):
    def __str__(self) -> str:
        return "The provided EPUB file is missing the Ncx declaration file."


class TmpPdfDirectoryAlreadyExists(Exception):
    def __str__(self) -> str:
        return "Attempted to create a TMP directory. But one already exists."


class TmpPathDoesntExists(Exception):
    def __str__(self) -> str:
        return "The TMP directory is not available in the provided path."


class MissingTmpDirPath(Exception):
    def __str__(self) -> str:
        return "The TMP directory path is not present."
