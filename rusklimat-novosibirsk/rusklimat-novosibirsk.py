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
from os.path import splitext, basename

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


def translit(locallangstring):
    conversion = {
        u'\u0410' : 'A',    u'\u0430' : 'a',
        u'\u0411' : 'B',    u'\u0431' : 'b',
        u'\u0412' : 'V',    u'\u0432' : 'v',
        u'\u0413' : 'G',    u'\u0433' : 'g',
        u'\u0414' : 'D',    u'\u0434' : 'd',
        u'\u0415' : 'E',    u'\u0435' : 'e',
        u'\u0401' : 'Yo',   u'\u0451' : 'yo',
        u'\u0416' : 'Zh',   u'\u0436' : 'zh',
        u'\u0417' : 'Z',    u'\u0437' : 'z',
        u'\u0418' : 'I',    u'\u0438' : 'i',
        u'\u0419' : 'Y',    u'\u0439' : 'y',
        u'\u041a' : 'K',    u'\u043a' : 'k',
        u'\u041b' : 'L',    u'\u043b' : 'l',
        u'\u041c' : 'M',    u'\u043c' : 'm',
        u'\u041d' : 'N',    u'\u043d' : 'n',
        u'\u041e' : 'O',    u'\u043e' : 'o',
        u'\u041f' : 'P',    u'\u043f' : 'p',
        u'\u0420' : 'R',    u'\u0440' : 'r',
        u'\u0421' : 'S',    u'\u0441' : 's',
        u'\u0422' : 'T',    u'\u0442' : 't',
        u'\u0423' : 'U',    u'\u0443' : 'u',
        u'\u0424' : 'F',    u'\u0444' : 'f',
        u'\u0425' : 'H',    u'\u0445' : 'h',
        u'\u0426' : 'Ts',   u'\u0446' : 'ts',
        u'\u0427' : 'Ch',   u'\u0447' : 'ch',
        u'\u0428' : 'Sh',   u'\u0448' : 'sh',
        u'\u0429' : 'Sch',  u'\u0449' : 'sch',
        u'\u042a' : '"',    u'\u044a' : '"',
        u'\u042b' : 'Y',    u'\u044b' : 'y',
        u'\u042c' : '\'',   u'\u044c' : '\'',
        u'\u042d' : 'E',    u'\u044d' : 'e',
        u'\u042e' : 'Yu',   u'\u044e' : 'yu',
        u'\u042f' : 'Ya',   u'\u044f' : 'ya',
    }
    translitstring = []
    for c in locallangstring:
        translitstring.append(conversion.setdefault(c, c))
    return ''.join(translitstring)

        
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
        
        output.writerow(['Категория', 'URL категории', 'Товар', 'Вариант', 'Описание', 'Цена', 'URL', 'Изображение', 'Артикул', 'Количество', 'Активность', 'Заголовок [SEO]', 'Ключевые слова [SEO]', 'Описание [SEO]', 'Старая цена', 'Рекомендуемый', 'Новый', 'Сортировка', 'Вес', 'Связанные артикулы', 'Смежные категории', 'Ссылка на товар', 'Валюта', 'Свойства', 'id'])
        
        page_list = ['http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/split-type-systems/', 'http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/inverter-split-type-systems/','http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/cassette-type-split-systems/', 'http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/floor-standing-split-systems/',
'http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/floor-ceiling-split-systems/', 'http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/mobile-type-air-conditioners/', 'http://www.rusklimat-novosibirsk.ru/catalog/air-dryings/air-dryings/', 'http://www.rusklimat-novosibirsk.ru/catalog/air-dryings/air-dryings-complex/']
        #page_list = page_list[:-7]
        for ppage in page_list:
            content = self.request_to_page(ppage)
            soup_inpage = BeautifulSoup(content, "lxml")
            product_links = [ self.main_url + x.find('a').attrs['href'] for x in soup_inpage.findAll('td',  {"class": "first goodLink"}) ]
            #print(product_links)
            """"""
            for prd_link in product_links:
                print(prd_link)
                #prd_link = "http://www.rusklimat-novosibirsk.ru/catalog/air-conditioner/split-type-systems/zanussi/24312.html"
                content_prd = self.request_to_page(prd_link)
                soup_prd = BeautifulSoup(content_prd, "lxml")
                title = soup_prd.find('h1',  {"class": "card-ttl"}).getText().strip()
                url_title = translit(title).replace(' ', '-').replace('/', '').replace(',', '').replace('(', '').replace(')', '').replace("'", "").lower().strip()
                code = soup_prd.find('div',  {"class": "article"}).getText().replace('код товара: ','').strip()
                price = soup_prd.find('p',  {"class": "sp"}).getText().strip().replace(' ', '')
                category = soup_prd.find('div',  {"class": "breadcrumbs"}).findAll('li')[4].getText().strip()
                url_category = translit(category).lower().replace("'", "").replace(' ', '-').strip()
                descr = soup_prd.find('div',  {"class": "content"}).find('ul')
                brend = soup_prd.find('div',  {"class": "brand dot"}).find('a').attrs['href'].replace('/partners/','').replace('.html','').replace('-',' ')
                keywords = ', '.join(title.split(' ')).replace('  ',' ') + ', ' + title + ' купить'
                
                print(url_title)
                tech_trs = soup_prd.find('div',  {"class": "tech"}).findAll('tr')
                tech_data = []
                tech_data.append({'Бренд': brend})
                for tr in tech_trs:
                    tech_title = tr.find('td',  {"class": "first"}).getText().strip()
                    tech_value = tr.findAll('td')[1].getText().strip()
                    tech_data.append({tech_title: tech_value})
                
                param_out = ''
                for param in tech_data:
                    tech_key = ''
                    tech_value = ''
                    tech_key, tech_value = param.popitem()
                    param_out += tech_key+'='+tech_value+'&'
                
                param_out = param_out[:-1]
                
                image_url_obj =  soup_prd.find('img',  {"id": "bigImg"})
                if image_url_obj != None:
                    image_url = image_url_obj.attrs['src'].strip()
                    img_hash = code.replace(' ', '_')
                    path = os.path.dirname(os.path.abspath(__file__))
                    disassembled = urlparse(image_url)
                    img_filename, img_file_ext = splitext(basename(disassembled.path))
                    img_index = img_filename + img_file_ext
                    img_path = os.path.join(path+'/images/'+str(img_index))
                    """
                    directory = os.path.dirname(img_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    
                    img_path = os.path.join(path+'/images/'+img_hash+'/'+str(img_index))
                    directory = os.path.dirname(img_path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    """
                    img_source = urllib.request.urlopen(image_url).read()
                    s = open(img_path, "wb")
                    s.write(img_source)
                    s.close()
                    img_file_path = str(img_index)
                else:
                    img_file_path = ''
                
                output.writerow([category, url_category, title, '', descr, price, url_title, img_file_path, code, '-1', '1', title, keywords, title, '0', '0', '0', '0', '0', '', '', '', 'RUR', param_out, ''])
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.rusklimat-novosibirsk.ru', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
