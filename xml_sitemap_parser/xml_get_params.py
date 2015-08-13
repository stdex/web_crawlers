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

        result = []
        content = self.request_to_page(self.main_url)
        soup = BeautifulSoup(content, "lxml")
        all_url = soup.findAll('url')
        print(len(all_url))
        
        all = len(all_url)

        for i in range(1,all):
            page_url = all_url[i].find('loc').text            
            content = self.request_to_page(page_url)
            soup = BeautifulSoup(content, "lxml")
            title = soup.find('title').text
            #print(page_url, title)
            obj = {'url': '', 'title': ''}
            obj['url'] = page_url
            obj['title'] = title
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

        worksheet_1.write(0, 0, 'URL', header_format)
        worksheet_1.write(0, 1, 'Title', header_format)

        row = 1
        col = 0
        
        for obj in result:
            if (obj.get('count') != ''):
                worksheet_1.set_row(row, 40)
                worksheet_1.write(row, 0, obj.get('url'), main_format)
                worksheet_1.write(row, 1, obj.get('title'), main_format)
                row += 1

        workbook.close()
            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://e-mebels.com/sitemap.xml', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()