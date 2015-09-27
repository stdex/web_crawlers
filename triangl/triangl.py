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
        content = self.request_to_page(self.main_url+'/collections/swimwear')
        soup = BeautifulSoup(content, "lxml")
        try:
            links = soup.findAll('a',  {"class": "product"})
            for link in links:
                cont = self.request_to_page(self.main_url+link.attrs['href'])
                soup_cont = BeautifulSoup(cont, "lxml")
                name = soup_cont.find('h1',  {"itemprop": "name"}).text.strip().replace(' ','_')
                path = os.path.dirname(os.path.abspath(__file__))
                imgpath = os.path.join(path+'/triangl_images/'+name+'/')
                if not os.path.exists(imgpath):
                    os.makedirs(imgpath)
                images = soup_cont.findAll('a',  {"class": "fancybox"})
                for img in images:
                    imgpath = os.path.join(path+'/triangl_images/'+name+'/')
                    img_url = ('http:'+img.attrs['href'])[:-13]
                    img_source = urllib.request.urlopen(img_url).read()
                    imgpath = os.path.join(imgpath, img_url.split("/")[-1])
                    print(imgpath)
                    s = open(imgpath, "wb")
                    s.write(img_source)
                    s.close()
                    print(img_url)
                #print(name)
                #print(link.attrs['href'])
        except:
            links = ''
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://international.triangl.com', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
