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


class FailedToDispose(Exception):
    def __str__(self) -> str:
        return "Failed to dispose resource."
