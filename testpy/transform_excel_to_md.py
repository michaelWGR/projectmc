# -*- coding: utf-8 -*-

import openpyxl

def get_excel_data(path):
    wb = openpyxl.load_workbook(path)
    sheet = wb.get_sheet_by_name('Sheet1')
    data_list = []
    count = 0
    for row in sheet.rows:

        if count == 0:
            row_str = u'| id |'
            for cell in row:
                if cell.value == None:
                    row_str = row_str + u'  |'
                    continue
                row_str = row_str + u' {} |'.format(cell.value)
            data_list.append(row_str + u'\n')

            rp_list = row_str.split(u'|')
            separator_str = row_str
            for rp in rp_list:
                if rp != u'':
                    separator_str = separator_str.replace(rp, u' -- ')
            data_list.append(separator_str+u'\n')
        else:
            row_str = u'| {} |'.format(count)
            for cell in row:
                if cell.value == None:
                    row_str = row_str + u'  |'
                    continue
                row_str = row_str + u' {} |'.format(cell.value)
            data_list.append(row_str+u'\n')

        count += 1

    return data_list

def write_md(wt_path, data_list):
    with open(wt_path, 'wb') as wt:
        for data in data_list:
            d_encode = data.encode('utf-8')
            wt.write(d_encode)

if __name__ == '__main__':
    path = r'E:\panF\MichaelFile.xlsx'
    data_list = get_excel_data(path)
    w_path = r'E:\panF\file.md'
    write_md(w_path, data_list)
