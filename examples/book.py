import pyxlhandler as pyxl


def main():
    book: pyxl.Book = pyxl.Book.from_file("./examples/data/test.xlsx")
    print(book.get_sheet_names())


if __name__ == "__main__":
    main()
