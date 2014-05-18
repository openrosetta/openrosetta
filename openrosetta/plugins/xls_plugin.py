import datetime
from openrosetta.exceptions import InvalidFileFormat
import xlrd

def dictify(file_=None):
    if file_ is None:
        file_ = open("/home/gas/Desktop/porocodio.xls", "r")
    try:
        workbook = xlrd.open_workbook(file_contents=file_.read(), encoding_override="cp1252")
    except:
        raise InvalidFileFormat
    worksheets = workbook.sheet_names()
    resp = []
    for worksheet_name in worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = -1
        column_headers = []
        normalized_worksheet = []
        is_first_row = True
        #row iterations
        while curr_row < num_rows:
            curr_row += 1
            curr_cell = -1
            empty_cell = 0
            normalized_row = {}
            #check if junk row
            while curr_cell < num_cells:
                curr_cell += 1
                cell_type = worksheet.cell_type(curr_row, curr_cell)
                if cell_type == 0:
                    empty_cell += 1
            if not empty_cell > num_cells/2:
                curr_cell = -1
                #iterate cells
                while curr_cell < num_cells:
                    curr_cell += 1
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    cell_value = worksheet.cell_value(curr_row, curr_cell)
                    cell_type = worksheet.cell_type(curr_row, curr_cell)
                    if is_first_row:
                        column_headers.append(cell_value)
                    else:
                        value = cell_value if cell_type != 3 else \
                            datetime.datetime(*xlrd.xldate_as_tuple(cell_value, 0))
                        normalized_row.update({column_headers[curr_cell]: value})
                is_first_row = False
            if len(normalized_row):
                normalized_worksheet.append(normalized_row)

        resp.append(normalized_worksheet)
    if len(resp) < 2:
        resp = resp[0]
    return resp