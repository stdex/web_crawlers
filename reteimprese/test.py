import xlsxwriter
import os.path
from PIL import Image


#output_filename = '427.xlsx'
#workbook = xlsxwriter.Workbook(output_filename)
#worksheet = workbook.add_worksheet()

imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__))+'/52516.png')
im = Image.open(imgpath)
print(im.format, im.size, im.mode)
"""
if(im.format == 'GIF'):
    try:
        Image.open(imgpath).save(imgpath)
    except IOError:
        print("cannot convert", imgpath)
        
im = Image.open(imgpath)
"""
#print(im.format, im.size, im.mode)
#worksheet.insert_image(1, 1, imgpath, {'positioning': 2, 'x_offset': 15, 'y_offset': 2})


#workbook.close()

