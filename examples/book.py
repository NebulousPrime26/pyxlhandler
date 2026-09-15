import pyxlhandler as pyxl


def main():
    book: pyxl.Book = pyxl.Book.from_file("./examples/data/test.xlsx")
    sheet = pyxl.Sheet("NewSheet")
    book.add_sheet(sheet, index=0)

    print(book.get_sheet_names())

    book.save("./examples/output/test_modified.xlsx", overwrite=True)


if __name__ == "__main__":
    main()
