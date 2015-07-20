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
            request = urllib.request.Request(url)
            request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            request.add_header("Accept-Language","ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4")
            request.add_header("Cache-Control","max-age=0")
            request.add_header("Connection","keep-alive")
            request.add_header("User-Agent","Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36")
            request.add_header("X-Compress","null")
            request.add_header("Content-type","application/x-www-form-urlencoded")
            page = urllib.request.urlopen(request)
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

        code_list = ['Restaurants']
        on_page = 35
        result = []
        
        for state in code_list:
            
            print(self.main_url)
            content = self.request_to_page(self.main_url+'&clue='+state)
            soup = BeautifulSoup(content, "lxml")
            try:
                count_res = soup.find('span',  {"class": "emphasise"}).text
                cnt = re.findall('^(.*?)'+re.escape('Results'), count_res, re.DOTALL)[0].strip()
                if(not cnt.isdigit()):
                   cnt = 0 
            except:
                cnt = 0

            num_pages = math.ceil(int(cnt)/on_page)
            print(num_pages)
                
            num_pages = 29
            
            for page_index in range(1,num_pages+1):
                page_index = page_index.__str__()
                content = self.request_to_page(self.main_url+'&clue='+state+'&pageNumber='+page_index)
                soup = BeautifulSoup(content, "lxml")
                
                blocks = soup.findAll('div',  {"class": "cell in-area-cell middle-cell"})
                print(len(blocks))
                for block in blocks:
                    obj = {'title': '', 'adr': '', 'phone': '', 'email': ''} 
                    try:
                        title = block.find('a',  {"class": "listing-name"}).text.strip()
                        obj['title'] = title
                    except:
                        title = ''
                        
                    try:
                        adr = block.find('div',  {"class": "poi-and-body"}).text.strip()
                        obj['adr'] = adr
                    except:
                        adr = ''
                        
                    try:    
                        phone = block.find('a',  {"class": "click-to-call contact contact-preferred contact-phone "}).attrs['href'].replace('tel:','')
                        obj['phone'] = phone
                    except:
                        phone = ''

                    try:    
                        email = block.find('a',  {"class": "contact contact-main contact-email "}).attrs['data-email']
                        obj['email'] = email
                    except:
                        email = ''
                        
                    result.append(obj)
                
        
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


        worksheet_1.write(0, 0, 'Name', header_format)
        worksheet_1.write(0, 1, 'Address', header_format)
        worksheet_1.write(0, 2, 'Phone', header_format)
        worksheet_1.write(0, 3, 'Email', header_format)

        row = 1
        col = 0
        
        for obj in result:
            if(obj.get('email') != ''):
                worksheet_1.set_row(row, 40)
                worksheet_1.write(row, 0, obj.get('title'), main_format)
                worksheet_1.write(row, 1, obj.get('adr'), main_format)
                worksheet_1.write(row, 2, obj.get('phone'), title_format)
                worksheet_1.write(row, 3, obj.get('email'), main_format)
                row += 1


        workbook.close()
           
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.yellowpages.com.au/search/listings?&locationClue=&lat=&lon=&selectedViewMode=list', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()