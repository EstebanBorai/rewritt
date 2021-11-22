from sys import argv
from epub import into_pdf

if __name__ == "__main__":
    if len(argv) > 1:
        _, file_path = argv
        into_pdf(file_path)
    else:
        print(f"Missing EPUB file path")
