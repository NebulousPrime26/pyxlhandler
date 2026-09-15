import pyxlhandler as pyxl


def main():
    book: pyxl.Book = pyxl.Book.from_file("./examples/data/test.xlsx")
    book.add_sheet("NewSheet")

    print(book.get_sheet_names())

    book.save("./examples/output/test_modified.xlsx", overwrite=True)


if __name__ == "__main__":
    main()
