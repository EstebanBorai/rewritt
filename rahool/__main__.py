from epub import Epub
from pdf import Pdf

from sys import argv

if __name__ == "__main__":
    if len(argv) > 1:
        _, file_path = argv
        epub = Epub(file_path)
        epub.open()

        if epub.ncx is not None:
            print(epub.ncx.content)

        pdf = Pdf()
        pdf.from_epub(epub)
        pdf.write_book()

        # epub.dispose()
    else:
        print(f"Missing EPUB file path")
