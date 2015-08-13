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
            #sys.exit(1)
        except timeout:
            print('socket timed out - URL %s', current_url)
            
        return content

    def start_process(self):
    
        result = []
        content = self.request_to_page(self.main_url)
        soup = BeautifulSoup(content, "lxml")
        all_catalog_lists = soup.find('div', {'class': 'city-list'}).findAll('a')
        
        myfile = open(self.output_file, 'w')
        
        for cat_list in all_catalog_lists:
            url_pages = []
            firm_name_urls = []
            
            href = cat_list.attrs['href'].strip()
            url_pages.append(href)
            content = self.request_to_page(href)
            if(content == None):
                continue  
            soup = BeautifulSoup(content, "lxml")
            pagginations = soup.findAll('li', {'class': 'pager-item'})
            for page in pagginations:
                url = page.find('a').attrs['href'].strip()
                url_pages.append(href+url)
            
            
            for url in url_pages:
                content = self.request_to_page(url)
                if(content == None):
                    continue 
                soup = BeautifulSoup(content, "lxml")
                firm_blocks = soup.findAll('div', {'class': 'firm-name'})
                for bl in firm_blocks:
                    firm_url = bl.find('a').attrs['href'].strip()
                    firm_name_urls.append(href+firm_url)
                    
            print(url_pages)
            
            for url in firm_name_urls:
                content = self.request_to_page(url)
                if(content == None):
                    continue 
                soup = BeautifulSoup(content, "lxml")
                try:
                    email = soup.find('div', {'class': 'mail'}).find('a').attrs['href'].replace('mailto:','').strip()
                    myfile.write("%s\n" % email)
                    #result.append(email)
                except:
                    print(url)
            
            #print(result)
            myfile.close()
            
        print(len(result))

            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://potolochek.su/', 'output_file': 'potolochek.txt' }
    aggregator = Aggregator(settings)
    aggregator.start_process()