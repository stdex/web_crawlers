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


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

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
        output.writerow(['Название продукта', 'Категория', 'Подкатегория', 'Пищевая Ценность', 'Енергетическая ценность', 'Белки', 'Углеводы', 'Сахар', 'Жиры', 'Насыщенные Жиры', 'Мононенасыщенные Жиры', 'Полиненасыщенные Жиры', 'Холестерин', 'Клетчатка', 'Натрий', 'Калий', 'РСК', 'Классификация калорий (Углеводы)', 'Классификация калорий (Жиры)', 'Классификация калорий (Белки)', 'Обычные размеры порций', 'Изображения'])
        
        check_list = []
        
        fpage = "http://fatsecret.ru/%D0%BA%D0%B0%D0%BB%D0%BE%D1%80%D0%B8%D0%B8-%D0%BF%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D0%B5/%D0%B3%D1%80%D1%83%D0%BF%D0%BF%D0%B0/%D0%91%D0%BE%D0%B1%D1%8B-%D0%B8-%D0%91%D0%BE%D0%B1%D0%BE%D0%B2%D1%8B%D0%B5"
        fcontent = self.request_to_page(fpage)
        soup_fpage = BeautifulSoup(fcontent, "lxml")
        main_cat_list = soup_fpage.find('table',  {"class": "common"}).findAll('a')
        #main_cat_list = main_cat_list[:-17]

        for main_cat in main_cat_list:
            
            main_cat_url = self.main_url + main_cat.attrs['href'].strip()
            main_cat_title = main_cat.getText().strip()
            fcontent = self.request_to_page(main_cat_url)
            soup_fpage = BeautifulSoup(fcontent, "lxml")
            main_cat_list = soup_fpage.find('table',  {"class": "common"}).findAll('a')
            
            secHolder_list = str(soup_fpage.find('div',  {"class": "secHolder"})).split('<hr/>')
            secHolder_list = secHolder_list[:-1]
            #secHolder_list = secHolder_list[:-4]
            for sub_cat in secHolder_list:
                soup_sub_cat = BeautifulSoup(sub_cat, "lxml")
                sub_cat_title = soup_sub_cat.find('h2').getText().strip()
                items_obj = soup_sub_cat.find('div',  {"class": "food_links"})
                if items_obj == None:
                    continue
                items_urls = [ self.main_url + x.attrs['href'].strip() for x in items_obj.findAll('a') ]
                #items_urls = items_urls[:-4]
                for item_url in items_urls:
                    if item_url in check_list:
                        continue
                    
                    item_content = self.request_to_page(item_url)
                    soup_item_page = BeautifulSoup(item_content, "lxml")
                    
                    check_an_unexpected_error_has_occured = soup_item_page.find('table',  {"class": "lightbordercurvedbox"})
                    
                    if check_an_unexpected_error_has_occured != None:
                        continue
                    
                    item_title = soup_item_page.find('h1').getText().strip()
                    item_translit = translit(item_title).replace(' ', '_').replace('/', '').replace(',', '').replace('(', '').replace(')', '').replace("'", "").lower().strip()
                    specifications_table = soup_item_page.find('div',  {"class": "nutpanel"}).findAll('tr')
                    specify = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:'', 10:'', 11:'', 12:''}
                    for spec_tr in specifications_table:
                        spec_item = spec_tr.findAll('td')
                        #print(spec_item)
                        spec_title = spec_item[0].getText().strip()
                        spec_value = spec_item[1].getText().replace('<br />','').replace('\n','').strip()
                        if spec_title == 'Пищевая Ценность':
                            specify[0] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Енергетическая ценность':
                            specify[1] = spec_value.split('кДж')[1].replace(' ккал','').strip()
                        if spec_title == 'Белки':
                            specify[2] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Углеводы':
                            specify[3] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Сахар':
                            specify[4] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Жиры':
                            specify[5] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Насыщенные Жиры':
                            specify[6] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Мононенасыщенные Жиры':
                            specify[7] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Полиненасыщенные Жиры':
                            specify[8] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Холестерин':
                            specify[9] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Клетчатка':
                            specify[10] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Натрий':
                            specify[11] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        if spec_title == 'Калий':
                            specify[12] = spec_value.replace('в ','').replace(' г','').replace(' мг','').strip()
                        
                    #print(specify)
                    rdi_value = soup_item_page.find('div',  {"class": "rdi_perc_container"}).find('div',  {"class": "big"}).getText().replace('%','').strip()
                    cfp_values = soup_item_page.find('div',  {"class": "cfp_breakdown_container"}).find('div',  {"class": "small"})
                    cfp_values = str(soup_item_page.find('div',  {"class": "cfp_breakdown_container"}).find('div',  {"class": "small"})).split('<br/>')
                    carbs_dot = BeautifulSoup(cfp_values[0], "lxml").getText().replace('Углеводы (','').replace('%)','').strip()
                    fat_dot = BeautifulSoup(cfp_values[1], "lxml").getText().replace('Жиры (','').replace('%)','').strip()
                    protein_dot = BeautifulSoup(cfp_values[2], "lxml").getText().replace('Белки (','').replace('%)','').strip()
                    #print(carbs_dot, fat_dot, protein_dot)
                    
                    common_serving_sizes = soup_item_page.find('table',  {"style": "margin:0px;margin-top:5px;"}).findAll('tr',  {"valign": "middle"})
                    common_serving_sizes_str = ""
                    for css in common_serving_sizes:
                        css_tds = css.findAll('td')
                        css_title = css_tds[0].getText().strip()
                        css_value = css_tds[1].getText().strip()
                        common_serving_sizes_str += css_title + ": " + css_value + "\n"
                    
                    css_out = common_serving_sizes_str.strip()
                    
                    image_extra = soup_item_page.find('a',  {"style": "color:#028CC4;"})
                    images_urls = []
                    if image_extra != None:
                        image_extra_url = self.main_url + image_extra.attrs['href'].strip()
                        image_extra_content = self.request_to_page(image_extra_url)
                        soup_image_extra = BeautifulSoup(image_extra_content, "lxml")
                        images_urls = [ x.attrs['src'].replace('_sq','') for x in soup_image_extra.find('table',  {"class": "generic searchResult"}).findAll('img') ]
                    else:
                        images_urls = [ x.attrs['src'].replace('_sq','') for x in soup_item_page.findAll('table',  {"class": "generic"})[4].findAll('img') ]
                    
                    #print(images_urls)
                    
                    for img_url in images_urls:
                        path = os.path.dirname(os.path.abspath(__file__))
                        disassembled = urlparse(img_url)
                        img_filename, img_file_ext = splitext(basename(disassembled.path))
                        img_index = img_filename + img_file_ext
                        img_path = os.path.join(path+'/images/'+item_translit+'/'+str(img_index))
                        
                        directory = os.path.dirname(img_path)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        img_source = urllib.request.urlopen(img_url).read()
                        s = open(img_path, "wb")
                        s.write(img_source)
                        s.close()
                        
                    if len(images_urls) == 0:
                        item_translit = ''
                    
                    output.writerow([item_title, main_cat_title, sub_cat_title, specify.get(0), specify.get(1), specify.get(2), specify.get(3), specify.get(4), specify.get(5), specify.get(6), specify.get(7), specify.get(8), specify.get(9), specify.get(10), specify.get(11), specify.get(12), rdi_value, carbs_dot, fat_dot, protein_dot, css_out, item_translit])
                    check_list.append(item_url)
                    
if __name__ == '__main__':
    settings = { 'main_url': 'http://fatsecret.ru', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
