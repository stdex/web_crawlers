from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from socket import timeout
import re
import sys
import os
import json, csv, sys
import unicodedata
import codecs
from unicodedata import normalize
import xlsxwriter
import os.path
from http.cookiejar import CookieJar
import collections
import math

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

        
class Aggregator(object):
    
    def __init__(self, config):
        main_url, output_file = [config.get(k) for k in sorted(config.keys())]
        self.main_url = main_url
        self.output_file = output_file

    def request_to_page(self, url):
        try:
            page = urllib.request.urlopen(url)
            content = page.read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to connect to server.')
                print('Reason: ', e.reason)
                print(current_url)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
            sys.exit(1)
        except timeout:
            print('socket timed out - URL %s', current_url)
            
        return content

    def start_process(self):
    
        output = csv.writer(open(self.output_file, 'w', newline=''),  delimiter=';')
        home = 'http://loftdesigne.ru'
        result = []
        content = self.request_to_page(self.main_url+'seating/')
        soup = BeautifulSoup(content, "lxml")
        all_catalog_lists = soup.findAll('div', {'class': 'catalogInList'})
        print(len(all_catalog_lists))
        for cat_list in all_catalog_lists:
            obj = {'id': '', 'img_url': '', 'img_url_big': '', 'img_alt': '', 'price': '', 'name': '', 'type': '', 'width': '', 'height': '', 'depth': '', 'width_seat': '', 'height_seat': '', 'depth_seat': '', 'material': ''}
            id = cat_list.find('a').attrs['onclick'].replace('catalogShowFull(','').replace(');','').strip()
            print(id)
            obj['id'] = id
            image = cat_list.find('p', {'class': 'image'}).find('img')
            img_url = home+image.attrs['src'].strip()
            obj['img_url'] = img_url
            img_alt = image.attrs['alt'].strip()
            obj['img_alt'] = img_alt
            price = cat_list.find('p', {'class': 'price'}).text.strip()
            obj['price'] = price
            name = cat_list.find('p', {'class': 'name'}).text.strip()
            obj['name'] = name
            current_item_details = soup.find('div', {'id': 'catalogInListFull'+id}).find('div', {'class': 'someData'})
            type = current_item_details.find('p', {'class': 'type'}).text.strip()
            obj['type'] = type
            img_url_big = soup.find('div', {'id': 'catalogInListFull'+id}).find('p', {'class': 'image'}).find('script').text
            obj['img_url_big'] = img_url_big
            
            obj['img_url_big'] = home+img_url_big.replace('imagesFace['+id+'] = "','').replace('";','')
            tbl = current_item_details.find('table')
            if( tbl != None):
                details_table_tr = tbl.findAll('tr')
                
                fl_seat = 0
                for tr in details_table_tr:
                    tds = tr.findAll('td')
                    if(len(tds) == 2):
                        type_td = tds[0].text.strip()
                        text_td = tds[1].text.strip().lower()
                        if ( ((type_td == 'ширина') or (type_td == 'длина')) and fl_seat == 0):
                            width = text_td
                            obj['width'] = width
                        elif(type_td == 'высота' and fl_seat == 0):
                            height = text_td
                            obj['height'] = height
                        elif(type_td == 'глубина' and fl_seat == 0):
                            depth = text_td
                            obj['depth'] = depth
                        # высота сидения?
                        # Высота сидения
                        # Размер сидения
                        elif(type_td == 'ширина' and fl_seat == 1):
                            width_seat = text_td
                            obj['width_seat'] = width_seat
                        elif(type_td == 'высота' and fl_seat == 1):
                            height_seat = text_td
                            obj['height_seat'] = height_seat
                        elif(type_td == 'глубина' and fl_seat == 1):
                            depth_seat = text_td
                            obj['depth_seat'] = depth_seat
                        elif(type_td == 'материал'):
                            material = text_td
                            obj['material'] = material
                    elif(len(tds) == 1):
                        fl_seat = 1
            
            else:
                try:
                    descr = current_item_details.find('div', {'class': 'desc'})
                    if(len(descr) > 0):
                        desc = descr.findAll('p')
                        if(len(desc) > 0):
                            for d in desc:
                                if(re.findall('высота - '+re.escape('$'), d.text.strip(), re.DOTALL) != None):
                                    obj['width'] = re.findall('высота - '+re.escape('$'), d.text.strip(), re.DOTALL)[0].strip()
                                elif(re.findall('ширина - '+re.escape('$'), d.text.strip(), re.DOTALL) != None):
                                    obj['height'] = re.findall('ширина - '+re.escape('$'), d.text.strip(), re.DOTALL)[0].strip()
                                elif(re.findall('глубина - '+re.escape('$'), d.text.strip(), re.DOTALL) != None):
                                    obj['depth'] = re.findall('глубина - '+re.escape('$'), d.text.strip(), re.DOTALL)[0].strip()
                                elif(re.findall('материал - '+re.escape('$'), d.text.strip(), re.DOTALL) != None):
                                    obj['material'] = re.findall('материал - '+re.escape('$'), d.text.strip(), re.DOTALL)[0].strip()
                except:
                    print(id)
            
            result.append(obj)
            
        print(len(result))
            
        #print(id, img_url, img_alt, price, name, type)
        #print(width, depth, height, width_seat, depth_seat, height_seat, material)

        
        """
        keywords = ['seating', 'tables', 'storage', 'lighting', 'accessories']
        """
            
        
        workbook = xlsxwriter.Workbook(self.output_file)
        worksheet_1 = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'fg_color': '#D7E4BC',
                                             'border': 1})

        main_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        title_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'valign': 'vcenter'})
                                             
        worksheet_1.set_column('A:A', 40)
        worksheet_1.set_column('B:B', 40)
        worksheet_1.set_column('C:C', 40)
        worksheet_1.set_column('D:D', 40)
        worksheet_1.set_column('E:E', 40)
        worksheet_1.set_column('F:F', 40)
        worksheet_1.set_column('G:G', 40)
        worksheet_1.set_column('H:H', 40)
        worksheet_1.set_column('I:I', 40)
        worksheet_1.set_column('J:J', 40)
        worksheet_1.set_column('K:K', 40)
        worksheet_1.set_column('L:L', 40)
        worksheet_1.set_column('M:M', 40)
        
        worksheet_1.write(0, 0, 'ID', header_format)
        worksheet_1.write(0, 1, 'Name', header_format)
        worksheet_1.write(0, 2, 'Type', header_format)
        worksheet_1.write(0, 3, 'Price', header_format)
        worksheet_1.write(0, 4, 'Small Image URL', header_format)
        worksheet_1.write(0, 5, 'Big Image URL', header_format)
        worksheet_1.write(0, 6, 'Width', header_format)
        worksheet_1.write(0, 7, 'Height', header_format)
        worksheet_1.write(0, 8, 'Depth', header_format)
        worksheet_1.write(0, 9, 'Width Seat', header_format)
        worksheet_1.write(0, 10, 'Height Seat', header_format)
        worksheet_1.write(0, 11, 'Depth Seat', header_format)
        worksheet_1.write(0, 12, 'Material', header_format)
        

        row = 1
        col = 0
        for obj in result:
            if (obj.get('count') != ''):
                worksheet_1.set_row(row, 40)
                worksheet_1.write(row, 0, obj.get('id'), main_format)
                worksheet_1.write(row, 1, obj.get('name'), main_format)
                worksheet_1.write(row, 2, obj.get('type'), main_format)
                worksheet_1.write(row, 3, obj.get('price'), main_format)
                worksheet_1.write(row, 4, obj.get('img_url'), main_format)
                worksheet_1.write(row, 5, obj.get('img_url_big'), main_format)
                worksheet_1.write(row, 6, obj.get('width'), main_format)
                worksheet_1.write(row, 7, obj.get('height'), main_format)
                worksheet_1.write(row, 8, obj.get('depth'), main_format)
                worksheet_1.write(row, 9, obj.get('width_seat'), main_format)
                worksheet_1.write(row, 10, obj.get('height_seat'), main_format)
                worksheet_1.write(row, 11, obj.get('depth_seat'), main_format)
                worksheet_1.write(row, 12, obj.get('material'), main_format)
                row += 1

        workbook.close()
        """"""
            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://loftdesigne.ru/catalog/', 'output_file': 'loftdesigne.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()