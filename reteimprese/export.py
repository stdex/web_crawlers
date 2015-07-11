import sqlite3
import os.path
import sys
from os.path import basename, splitext
import xlsxwriter
import os.path
from PIL import Image

output_filename = 'test_tbl.xlsx'

workbook = xlsxwriter.Workbook(output_filename)
worksheet = workbook.add_worksheet()

header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})

main_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'valign': 'top', 'border': 1})
                                     
worksheet.set_column('A:A', 35)
worksheet.set_column('B:B', 24)
worksheet.set_column('C:C', 5)
worksheet.set_column('D:D', 8)
worksheet.set_column('E:E', 15)
worksheet.set_column('F:F', 10)
worksheet.set_column('G:G', 11)
worksheet.set_column('H:H', 7)
worksheet.set_column('I:I', 30)
worksheet.set_column('J:J', 32)
worksheet.set_column('K:K', 37)
worksheet.set_column('L:L', 36)
worksheet.set_column('M:M', 11)
worksheet.set_column('N:N', 35)
worksheet.set_column('O:O', 19)

workbook.add_format({'text_wrap': 1, 'valign': 'top'})

worksheet.write(0, 0, 'NOME', header_format)
worksheet.write(0, 1, 'INDIRIZZO', header_format)
worksheet.write(0, 2, 'CAP', header_format)
worksheet.write(0, 3, 'COMUNE', header_format)
worksheet.write(0, 4, 'PROVINCIA', header_format)
worksheet.write(0, 5, 'TELEONO', header_format)
worksheet.write(0, 6, 'PIVA', header_format)
worksheet.write(0, 7, 'REA', header_format)
worksheet.write(0, 8, 'URL', header_format)
worksheet.write(0, 9, 'CATEGORIA', header_format)
worksheet.write(0, 10, 'GEOCATEGORIA', header_format)
worksheet.write(0, 11, 'URL RETE IMPRESA', header_format)
worksheet.write(0, 12, 'URL SEARCH', header_format)
worksheet.write(0, 13, 'DESCRIZIONE', header_format)
worksheet.write(0, 14, 'IMAGE', header_format)

row = 1
col = 0


DATABASE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'proxy.db')

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("""SELECT * FROM Reteimprese""")
rows = cursor.fetchall()

#print(rows)

for item in rows:
    worksheet.set_row(row, 80)
    worksheet.write(row, 0, item[1], main_format)
    worksheet.write(row, 1, item[2], main_format)
    worksheet.write(row, 2, item[3], main_format)
    worksheet.write(row, 3, item[4], main_format)
    worksheet.write(row, 4, item[5], main_format)
    worksheet.write(row, 5, item[6], main_format)
    worksheet.write(row, 6, item[7], main_format)
    worksheet.write(row, 7, item[8], main_format)
    worksheet.write(row, 8, item[9], main_format)
    worksheet.write(row, 9, item[10], main_format)
    worksheet.write(row, 10, item[11], main_format)
    worksheet.write(row, 11, item[12], main_format)
    worksheet.write(row, 12, item[13], main_format)
    worksheet.write(row, 13, item[14], main_format)
    
    image_scr = item[15]
    imgname = item[16]
    if(imgname != ''):
        imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__))+'/img/', imgname+'.png')
        try:
            im = Image.open(imgpath)
            if(im.format == 'GIF'):
                try:
                    Image.open(imgpath).save(imgpath)
                except IOError:
                    print("cannot convert", imgpath)
        except:
            image_scr = ''
            #print("cannot open", imgpath)
    else:
        imgpath = ''
        
    if(image_scr != ''):
        worksheet.write(row, 14, "", main_format)
        worksheet.insert_image(row, 14, imgpath, {'positioning': 2, 'x_offset': 15, 'y_offset': 2})
    else:
        worksheet.write(row, 14, image_scr, main_format)
    row += 1
    


    #print (item[16])
connection.commit()
connection.close()
workbook.close()