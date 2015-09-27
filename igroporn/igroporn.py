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
from os.path import splitext, basename

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
        
        path = os.path.dirname(os.path.abspath(__file__))
        
        for inx in range(2,40):
            print(str(inx))
            content = self.request_to_page(self.main_url+'/page/'+str(inx)+'/')
            soup = BeautifulSoup(content, "lxml")
            page_links = soup.findAll('a',  {"class": "game"})
            print(len(page_links))
            for internal in page_links:
                link_to_internal = internal.attrs['href']
                content_internal = self.request_to_page(link_to_internal)
                soup_page = BeautifulSoup(content_internal, "lxml")
                iframe_obj = soup_page.find('iframe')
                if(iframe_obj != None):
                    iframe = iframe_obj.attrs['src']
                    disassembled = urlparse(iframe)
                    swf_filename, swf_ext = splitext(basename(disassembled.path))
                    swf_source = urllib.request.urlopen(iframe)
                    swfpath = path+'/swf/'+swf_filename+'.swf'
                    s = open(swfpath, "wb")
                    s.write(swf_source.read())
                    s.close()
                    print(iframe)
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://igroporn.com', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
