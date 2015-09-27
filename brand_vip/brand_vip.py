from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from socket import timeout
import re
import sys
import os
from os.path import basename, splitext
from urllib.parse import urlparse
import json, csv, sys
import unicodedata
import codecs
from unicodedata import normalize
import xlsxwriter
import random
import os.path
import sys
import sqlite3
from io import BytesIO

pattern_main = "http://brand-vip.ru"
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
worksheet.set_column('B:B', 35)
worksheet.set_column('C:C', 35)
worksheet.set_column('D:D', 35)
worksheet.set_column('E:E', 50)

workbook.add_format({'text_wrap': 1, 'valign': 'top'})

worksheet.write(0, 0, 'Наименование', header_format)
worksheet.write(0, 1, 'Категория', header_format)
worksheet.write(0, 2, 'Модель', header_format)
worksheet.write(0, 3, 'Производитель', header_format)
worksheet.write(0, 4, 'Изображение', header_format)

row = 1
col = 0

"""
try:
    request = urllib.request.Request(pattern_main, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
    page = urllib.request.urlopen(request, timeout=10)
except urllib.error.URLError as e:
    if hasattr(e, 'reason'):
        print('Failed to connect to server.')
        print('Reason: ', e.reason)
        print(page_url)
    elif hasattr(e, 'code'):
        print('Error code: ', e.code)
    sys.exit(1)
except timeout:
    print('socket timed out - URL %s', page_url)

content = page.read()
#ssss = ''.join(map(chr, content.decode('iso-8859-1').encode('utf8')))
soup = BeautifulSoup(content, "lxml")
catz_div = soup.findAll('div',  {"class": "catmenu"})
catz = catz_div[0].findAll('a')

for cat in catz:
    #print(cat.attrs['href'])
"""

catz_links = ['http://brand-vip.ru/aksessuary/klatchi/',
'http://brand-vip.ru/aksessuary/kosmetichki/',
'http://brand-vip.ru/aksessuary/koshelki/',
'http://brand-vip.ru/aksessuary/oblozhki-dlya-dokumentov-klyuchnicy/',
'http://brand-vip.ru/aksessuary/ochki/',
'http://brand-vip.ru/aksessuary/perchatki/',
'http://brand-vip.ru/aksessuary/pledy-polotenca/',
'http://brand-vip.ru/aksessuary/postelnoe-bele/',
'http://brand-vip.ru/aksessuary/remni/',
'http://brand-vip.ru/aksessuary/ruchki-swarovski/',
'http://brand-vip.ru/aksessuary/chehly-dlya-ipad-iphone/',
'http://brand-vip.ru/aksessuary/shapki/',
'http://brand-vip.ru/aksessuary/sharfy-platki-palantiny/',

'http://brand-vip.ru/bizhuteriya/braslety/',
'http://brand-vip.ru/bizhuteriya/broshi-chanel/',
'http://brand-vip.ru/bizhuteriya/kolca/',
'http://brand-vip.ru/bizhuteriya/komplekty/',
'http://brand-vip.ru/bizhuteriya/sergi-podveski/',

'http://brand-vip.ru/muzhskoe/kurtki-puhoviki/',
'http://brand-vip.ru/muzhskoe/muzhskie-koshelki/',
'http://brand-vip.ru/muzhskoe/muzhskie-rubashki/',
'http://brand-vip.ru/muzhskoe/muzhskie-sumki/',
'http://brand-vip.ru/muzhskoe/muzhskie-futbolki-polo/',
'http://brand-vip.ru/muzhskoe/nizhnee-bele/',
'http://brand-vip.ru/muzhskoe/obuv-1/',
'http://brand-vip.ru/muzhskoe/puhoviki-1/',
'http://brand-vip.ru/muzhskoe/remni-1/',
'http://brand-vip.ru/muzhskoe/svitera-kofty/',
'http://brand-vip.ru/muzhskoe/sportivnye-kostyumy-1/',
'http://brand-vip.ru/muzhskoe/sharfy/',

'http://brand-vip.ru/obuv/baletki/',
'http://brand-vip.ru/obuv/bosonozhki/',
'http://brand-vip.ru/obuv/botinki/',
'http://brand-vip.ru/obuv/zimnyaya-obuv/',
'http://brand-vip.ru/obuv/krossovki/',
'http://brand-vip.ru/obuv/mokasiny/',
'http://brand-vip.ru/obuv/tufli/',
'http://brand-vip.ru/obuv/shlepkislancy/',

'http://brand-vip.ru/odezhda/bryuki-shtany/',
'http://brand-vip.ru/odezhda/zhenskie-dzhinsy/',
'http://brand-vip.ru/odezhda/kofty-sviterki/',
'http://brand-vip.ru/odezhda/kupalniki/',
'http://brand-vip.ru/odezhda/kurtki/',
'http://brand-vip.ru/odezhda/pidzhaki/',
'http://brand-vip.ru/odezhda/platya-yubki/',
'http://brand-vip.ru/odezhda/puhoviki/',
'http://brand-vip.ru/odezhda/sportivnye-kostyumy/',
'http://brand-vip.ru/odezhda/trusy/',
'http://brand-vip.ru/odezhda/futbolki-mayki/',
'http://brand-vip.ru/pufy-so-strazami/',

'http://brand-vip.ru/sumki/burberry/',
'http://brand-vip.ru/sumki/chanel-1/',
'http://brand-vip.ru/sumki/chanel/',
'http://brand-vip.ru/sumki/dolcegabbana/',
'http://brand-vip.ru/sumki/etro/',
'http://brand-vip.ru/sumki/furla/',
'http://brand-vip.ru/sumki/sumki-giorgio-armani/',
'http://brand-vip.ru/sumki/gucci/',
'http://brand-vip.ru/sumki/louis-vuitton/',
'http://brand-vip.ru/sumki/zhenskie-sumki/',
'http://brand-vip.ru/sumki/zhenskie-sumki-miks/',

'http://brand-vip.ru/chasy/hublot/',

'http://brand-vip.ru/kurtki-po-proizvoditelyam/kurtki-bosco/',
'http://brand-vip.ru/kurtki-po-proizvoditelyam/kurtki-zilli/',
'http://brand-vip.ru/aksessuary-dlya-vannoy-komnaty-so-strazami-swarovski/',

'http://brand-vip.ru/koshelki-po-proizvoditelyam/koshelki-brioni/',
'http://brand-vip.ru/koshelki-po-proizvoditelyam/koshelki-montblanc/',
'http://brand-vip.ru/koshelki-po-proizvoditelyam/koshelki-zilli/',

'http://brand-vip.ru/remni-po-proizvoditelyam/remni-hermes/',
'http://brand-vip.ru/remni-po-proizvoditelyam/remni-montblanc/',
'http://brand-vip.ru/remni-po-proizvoditelyam/remni-zilli/',
'http://brand-vip.ru/ployki/',

'http://brand-vip.ru/sharfy-po-proizvoditelyam/sharfy-etro/',
'http://brand-vip.ru/sharfy-po-proizvoditelyam/sharfy-hermes/',
'http://brand-vip.ru/sharfy-po-proizvoditelyam/palantiny-louis-vuitton/',

'http://brand-vip.ru/postelnoe-belye/postelnoe-belye-etro/',

'http://brand-vip.ru/krossovki-po-proizvoditelyam/krossovki-bikkembergs/',
'http://brand-vip.ru/krossovki-po-proizvoditelyam/krossovki-dolce-gabbana/',

'http://brand-vip.ru/oblojki-po-proizvoditelyam/oblojki-hermes/',
'http://brand-vip.ru/oblojki-po-proizvoditelyam/oblojki-montblanc/',
]

catz_links = ['http://brand-vip.ru/sumki/louis-vuitton/']

for cat_link in catz_links:
    try:
        request = urllib.request.Request(cat_link, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
        #page = urllib.request.FancyURLopener({"http":current_proxy}).open(request)
        page = urllib.request.urlopen(request, timeout=10)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            print(page_url)
            continue
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
            continue
        sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', page_url)
        continue
    
    content = page.read()
    soup = BeautifulSoup(content, "lxml")
    catz_div = soup.find('div',  {"class": "links"})
    curr_links = []
    if(catz_div != None):
        curr_links.append(cat_link)
        pagination = catz_div.findAll('a')
        for pp in pagination:
            curr_links.append(pp.attrs['href'])
    
    for product_link in curr_links:
        try:
            request = urllib.request.Request(product_link, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
            #page = urllib.request.FancyURLopener({"http":current_proxy}).open(request)
            page = urllib.request.urlopen(request, timeout=1000)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to connect to server.')
                print('Reason: ', e.reason)
                print(page_url)
                continue
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
                continue
            sys.exit(1)
        except timeout:
            print('socket timed out - URL %s', page_url)
            continue
        content = page.read()
        soup = BeautifulSoup(content, "lxml")
        prd_links = soup.findAll('div',  {"class": "image"})
        for prd in prd_links:
            pr = prd.find('a')
            pr_link = pr.attrs['href']
            try:
                request_tt = urllib.request.Request(pr_link, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
                page_tt = urllib.request.urlopen(request_tt, timeout=1000)
            except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                    print('Failed to connect to server.')
                    print('Reason: ', e.reason)
                    print(page_url)
                    continue
                elif hasattr(e, 'code'):
                    print('Error code: ', e.code)
                    continue
                sys.exit(1)
            except timeout:
                print('socket timed out - URL %s', page_url)
                continue
            content_tt = page_tt.read()
            soup_tt = BeautifulSoup(content_tt, "lxml")
            breadcrumb = soup_tt.find('div',  {"class": "breadcrumb"})
            breadcrumb_links = breadcrumb.findAll('a')
            category = breadcrumb_links[2].text
            title = breadcrumb_links[3].text
            
            description = soup_tt.find('div',  {"class": "description"})
            factory = description.find('a').text
            spans = description.findAll('span')
            model = spans[1].text.replace('Модель: ','')
            
            worksheet.set_row(row, 250)
            worksheet.write(row, 0, str(title), main_format)
            worksheet.write(row, 1, str(category), main_format)
            worksheet.write(row, 2, str(model), main_format)
            worksheet.write(row, 3, str(factory), main_format)
            
            img_div = soup_tt.find('div',  {"class": "image"})
            print(pr_link)
            image_link = img_div.find('img').attrs['src'].replace(" ", "%20")
            
            try:
                img_data = urllib.request.urlopen(image_link, timeout=1000)
                img_source = img_data.read()
                image_data = BytesIO(img_source)
                worksheet.insert_image(row, 4, str(image_link), {'image_data': image_data})
            except urllib.error.URLError as e:
                if hasattr(e, 'reason'):
                    print('Failed to connect to server.')
                    print('Reason: ', e.reason)
                elif hasattr(e, 'code'):
                    print('Error code: ', e.code)
                #sys.exit(1)
            except timeout:
                print('socket timed out - URL %s', image_link)
            except:
                print('problems - URL %s', image_link)
                s = open('bad_urls.txt', "a")
                s.write("%s::%s\n" % (pr_link,image_link))
                s.close()
                
            
            row += 1
            
workbook.close()
