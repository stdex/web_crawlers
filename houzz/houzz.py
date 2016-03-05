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
        
        links = ['http://www.houzz.ru/ideabooks/59837003/thumbs/idei-polyzovatelya-artemevlanov', 'http://www.houzz.ru/ideabooks/59837003/start=52/thumbs/idei-polyzovatelya-artemevlanov', 'http://www.houzz.ru/ideabooks/59837003/start=104/thumbs/idei-polyzovatelya-artemevlanov', 'http://www.houzz.ru/ideabooks/59837003/start=156/thumbs/idei-polyzovatelya-artemevlanov', 'http://www.houzz.ru/ideabooks/59837003/start=208/thumbs/idei-polyzovatelya-artemevlanov', 'http://www.houzz.ru/ideabooks/59837003/start=260/thumbs/idei-polyzovatelya-artemevlanov']
        
        #links = ['http://www.houzz.ru/ideabooks/59837003/start=260/thumbs/idei-polyzovatelya-artemevlanov']
        path = os.path.dirname(os.path.abspath(__file__))
        
        for lnk in links:
            content = self.request_to_page(lnk)
            soup = BeautifulSoup(content, "lxml")

            pages = soup.findAll('a',  {"class": "noHoverLink"})
            for pp in pages:
                pp_link = pp.attrs['href']
                content_inpage = self.request_to_page(pp_link)
                soup_inpage = BeautifulSoup(content_inpage, "lxml")
                img_og = soup_inpage.find('meta',  {"property": "og:image"}).attrs['content']
                try:
                    img_url = img_og[:43] + "8" + img_og[44:]
                    img_hash = img_url.split("/")[4]
                    img_name = img_url.split("/")[5]
                    img_path = os.path.join(path+'/images/'+img_hash+'__'+img_name)
                    img_source = urllib.request.urlopen(img_url).read()
                except urllib.error.HTTPError:
                    print(img_url, img_name, img_path)
                    img_url = img_og[:43] + "8" + img_og[44:]
                    img_hash = img_url.split("/")[4]
                    img_name = img_url.split("/")[5]
                    img_path = os.path.join(path+'/images/'+img_hash+'__'+img_name)
                    img_source = urllib.request.urlopen(img_url).read()
                
                s = open(img_path, "wb")
                s.write(img_source)
                s.close()
                print(img_url)
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://olx.ua', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
