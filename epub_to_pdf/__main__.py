from sys import argv
from epub import copy_as_zip

if __name__ == "__main__":
    if len(argv) > 1:
        _, file_path = argv
        copy_as_zip(file_path)
    else:
        print(f"Missing EPUB file path")
