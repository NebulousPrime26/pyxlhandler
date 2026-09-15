import pyxlhandler.parser

parser = pyxlhandler.parser.ExcelReader("./examples/data/test.xlsx")
print(parser.sheets)
