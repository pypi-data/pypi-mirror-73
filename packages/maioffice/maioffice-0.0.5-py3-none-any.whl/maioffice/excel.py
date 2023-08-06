import openpyxl

def load(filename):
    """return openpyxl.Workbook object by filename
    """
    return openpyxl.load_workbook(filename)
