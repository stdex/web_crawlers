# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from socket import timeout
import re
import sys
import os
import json, csv, sys
import os.path
from http.cookiejar import CookieJar
from time import sleep
import unicodedata

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

        
class Aggregator(object):
    
    def __init__(self, config):
        main_url, output_file = [config.get(k) for k in sorted(config.keys())]
        self.main_url = main_url
        self.output_file = output_file

    def request_to_page(self, url):
        try:
            current_url = url
            cookie_jar = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)

            req = urllib.request.Request(url)
            page = urllib.request.urlopen(req)

            content = page.read()
            #print(content)
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
        output.writerow(['Номер заказа', 'Полное название', 'Название', 'Преимущества продукта', 'Области применения', 'Характеристики продукта', 'Длина', 'Диаметр', 'Вес продукта', 'Мощность на входе', 'Номинальный напряжение', 'Номинальная мощность', 'Допустимое отклонение входной мощности', 'Тестовое напряжение', 'Мощность системы [AGGR]', 'Цоколь', 'ECE-категория', 'Сертификация/Соответствие стандартам', 'Цветовая температура', 'Световой поток', 'Допуск по отклонению светового потока', 'Продолжительность жизни В3', 'Срок службы Тс'])
        
        page_list = ['http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/headlights-for-cars/index.jsp', 'http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/led-exterior-lighting/index.jsp', 'http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/gas-discharge-headlight-lamps-for-cars/index.jsp', 'http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/halogen-headlight-lamps-for-cars/index.jsp', 'http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/led-interior-lighting/index.jsp', 'http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/signal-lamps-for-cars/index.jsp']
        #page_list = page_list[:-5]
        for ppage in page_list:
            content = self.request_to_page(ppage)
            soup_inpage = BeautifulSoup(content, "lxml")
            product_links = soup_inpage.findAll('a',  {"class": "cat_heading"})
            for prd in product_links:
                prd_link = self.main_url + prd.attrs['href']
                print(prd_link)
                
                #prd_link = "http://www.osram.ru/osram_ru/products/lamps/vehicle-and-bicycle-lighting/cars/headlights-for-cars/ledriving-xenarc/index.jsp"
                content_prd = self.request_to_page(prd_link)
                soup_prd = BeautifulSoup(content_prd, "lxml")
                title = soup_prd.find('h1',  {"class": "hl_content"}).getText().strip()
                descr = soup_prd.findAll('ul',  {"class": "simplelist"})
                orig_pd_copy = soup_prd.find('div',  {"class": "pd_copy"})
                obj_titles = [ x.getText().strip() for x in orig_pd_copy.findAll('b') ]
                descr_plus = ''
                descr_area = ''
                descr_charact = ''
                descr_standart = ''
                descr_equpm = ''
                descr_sec = ''
                descr_0 = ''
                descr_1 = ''
                descr_2 = ''
                for ds in descr:
                    try:
                        descr_plus = [ x.getText().replace('&#150;','-') for x in descr[0].findAll('li') ]
                    except IndexError:
                        pass
                    try:
                        descr_area = [ x.getText() for x in descr[1].findAll('li') ]
                    except IndexError:
                        pass
                    try:
                        descr_charact = [ x.getText() for x in descr[2].findAll('li') ]
                    except IndexError:
                        pass
                    
                    """
                    if 'Соответствие стандартам' in obj_titles:
                        try:
                            descr_standart = [ x.getText() for x in descr[3].findAll('li') ]
                        except IndexError:
                            pass
                    
                    if 'Оборудование/аксессуары' in obj_titles:
                        try:
                            descr_equpm = [ x.getText() for x in descr[3].findAll('li') ]
                        except IndexError:
                            pass
                            
                    if 'Советы по безопасности' in obj_titles:
                        try:
                            descr_sec = [ x.getText() for x in descr[3].findAll('li') ]
                        except IndexError:
                            pass
                    """

                descr_0 = '\n'.join(descr_plus).strip()
                descr_1 = '\n'.join(descr_area).strip()
                descr_2 = '\n'.join(descr_charact).strip()
                
                series_prd = [ self.main_url + x.attrs['href'] for x in soup_prd.findAll('a',  {"class": "arr_right"}) ]
                for srs_rd in series_prd:
                    print(srs_rd)
                    content_srs = self.request_to_page(srs_rd)
                    soup_srs = BeautifulSoup(content_srs, "lxml")
                    srs_title = soup_srs.find('h2',  {"class": "hl_tab_content"}).getText().strip()
                    srs_characters = ([ x.findAll('tr') for x in soup_srs.findAll('div',  {"class": "producttable"}) ])
                    lenq = ''
                    diam = ''
                    weight = ''
                    input_power = ''
                    nominal_voltage = ''
                    nominal_power = ''
                    dop_input_power = ''
                    test_voltage = ''
                    aggr_power = ''
                    cocol = ''
                    ECE = ''
                    sertificy = ''
                    color_t = ''
                    color_flow = ''
                    dop_color_flow = ''
                    hours_work_b3 = ''
                    hours_work = ''
                    for character in srs_characters:
                        char_title = character[0].find('th').getText().strip()
                        char_value = character[0].find('td').getText().strip().replace('&#133;', '...').replace('&#133;', '...')
                        
                        #
                        
                        if char_title == 'Номер заказа':
                            classify = char_value
                            
                        #
                        
                        if char_title == 'Длина':
                            lenq = char_value
                            
                        if char_title == 'Диаметр':
                            diam = char_value
                        
                        if char_title == 'Вес продукта':
                            weight = char_value
                            
                        #
                        
                        if char_title == 'Мощность на входе':
                            input_power = char_value
                            
                        if char_title == 'Номинальный напряжение':
                            nominal_voltage = char_value
                        
                        if char_title == 'Номинальная мощность':
                            nominal_power = char_value
                            
                        if char_title == 'Допустимое отклонение входной мощности':
                            dop_input_power = char_value
                            
                        if char_title == 'Тестовое напряжение':
                            test_voltage = char_value
                            
                        if char_title == 'Мощность системы [AGGR]':
                            aggr_power = char_value
                            
                        #
                        
                        if char_title == 'Цоколь':
                            cocol = char_value
                        
                        #
                            
                        if char_title == 'ECE-категория':
                            ECE = char_value
                            
                        if char_title == 'Сертификация/Соответствие стандартам':
                            sertificy = char_value
                            
                        #
                            
                        if char_title == 'Цветовая температура':
                            color_t = char_value
                            
                        if char_title == 'Световой поток':
                            color_flow = char_value
                            
                        if char_title == 'Допуск по отклонению светового потока':
                            dop_color_flow = char_value
                            
                        #
                        
                        if char_title == 'Продолжительность жизни В3':
                            hours_work_b3 = char_value
                            
                        if char_title == 'Срок службы Тс':
                            hours_work = char_value

                    img_product_line_list = [ self.main_url + x.find('a').attrs['href'] for x in soup_srs.findAll('div',  {"class": "cat_copy arr_left"}) ]
                    img_product = (soup_srs.find('a',  {"id": "lightbox_zoom"}).attrs['rel'])[0].split(';')
                    img_product_large = self.main_url + img_product[1]
                    img_product_line_list.insert(0, img_product_large)
                    #print(img_product_line_list)
                    img_hash = classify.replace(' ', '_')
                    img_index = 0
                    path = os.path.dirname(os.path.abspath(__file__))
                    for img_url in img_product_line_list:
                        img_path = os.path.join(path+'/images/'+img_hash+'/'+str(img_index)+'.jpg')
                        directory = os.path.dirname(img_path)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        img_source = urllib.request.urlopen(img_url).read()
                        s = open(img_path, "wb")
                        s.write(img_source)
                        s.close()
                        img_index = img_index + 1
                        
                    output.writerow([classify, srs_title, title, descr_0, descr_1, descr_2, lenq, diam, weight, input_power, nominal_voltage, nominal_power, dop_input_power, test_voltage, aggr_power, cocol, ECE, sertificy, color_t, color_flow, dop_color_flow, hours_work_b3, hours_work])
            
            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.osram.ru', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
