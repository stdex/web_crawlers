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
        
        # second - parse phones
        with open('emls_links.txt') as f:
            emls_links = f.readlines()
            
        phone_list = []
        for link in emls_links:
            try:
                print(link.strip())
                content = self.request_to_page(link.strip())
                soup = BeautifulSoup(content, "lxml")
                tr_s = soup.find('table', {"class": "html_table_1"}).findAll('tr')[1:-1]
                for tr in tr_s:
                    td_s = tr.findAll('td')
                    if(len(td_s) == 1):
                        continue
                    td = str(td_s[5]).split('<br/>')
                    #print(len(td))
                    if(len(td) == 4):
                        phone_list.append(td[1].strip())
                        phone_list.append(td[2].strip())
                    elif(len(td) == 3):
                        phone_list.append(td[1].strip())
            except Exception as e:
                print(str(e))
                print(link.strip())
        
        phones = list(set(phone_list))
        
        s = open('emls_phones.txt', "a")

        for item in phones:
            s.write("%s\n" % item)

        s.close()
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://emls.ru', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
