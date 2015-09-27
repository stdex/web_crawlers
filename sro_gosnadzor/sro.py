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

    def request_to_page(self, url, cnt_page):
        try:
            current_url = url
            cookie_jar = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)

            params = urllib.parse.urlencode({
                '_search': 'false',
                'nd': '1441114066092',
                'rows':  '20',
                'page':  cnt_page,
                'sidx':  '',
                'sord':  'asc',
            })
            
            data = params.encode('utf-8')
            request = urllib.request.Request(url)
            request.add_header("Accept","application/json, text/javascript, */*")
            request.add_header("Accept-Language","ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4")
            request.add_header("Connection","keep-alive")
            request.add_header("Accept-Encoding","gzip, deflate")
            request.add_header("Content-Length","60")
            request.add_header("Content-Type","application/x-www-form-urlencoded")
            request.add_header("Host","sro.gosnadzor.ru")
            request.add_header("Origin","http://sro.gosnadzor.ru")
            request.add_header("Referer","http://sro.gosnadzor.ru/")
            request.add_header("User-Agent","Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
            request.add_header("X-Compress","null")
            request.add_header("X-Requested-With","XMLHttpRequest")
            page = urllib.request.urlopen(request, data)

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

    def request_to_p(self, url):
        try:
            current_url = url
            cookie_jar = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)

            req = urllib.request.Request(url)
            page = urllib.request.urlopen(req)

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
        
        pages_url = '/Home/SroData'
        for cnt in range(1,15):
            content = self.request_to_page(self.main_url+pages_url, str(cnt))
            try:
                req_arr = json.loads(content.decode('utf8'))
                rows = req_arr['rows']
                for row in rows:
                    soup = BeautifulSoup(row['name'], "lxml")
                    link = soup.find('a').attrs['href']
                    print(self.main_url+link)
                    cc = self.request_to_p(self.main_url+link)
                    cc_soup = BeautifulSoup(cc, "lxml")
                    mailto = cc_soup.select('a[href^=mailto]')[0].attrs['href'].replace('mailto:','')
                    fo = open('sro_emails.txt', "a")
                    fo.write(mailto+'\n');
                    fo.close()
                    #print(mailto)
                    
                    #print(link)
                
                """
                pager = soup.findAll('span',  {"class": "item fleft"})
                last_page = pager[-1].find('span').text
                print(last_page)
                #int(last_page)
                for page in range(1,2):
                    content_page = self.request_to_page(self.main_url+cat+'?page='+str(page))
                    soup_page = BeautifulSoup(content_page, "lxml")
                    page_links = soup_page.findAll('a',  {"class": "marginright5 link linkWithHash detailsLink"})[0:-42]
                    print(len(page_links))

                    for item in page_links:
                        item_url = item.attrs['href']
                        content_item = self.request_to_page(item_url)
                        soup_item = BeautifulSoup(content_item, "lxml")
                        li_json = soup_item.find('li',  {"data-rel": "phone"}).attrs['class']
                        phone_id = li_json[5].replace("'id':'","").replace("',","")
                        print(phone_id)
                        parsed_uri = urlparse( item_url )
                        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                        phone_url = domain+'/ajax/misc/contact/phone/'+phone_id+'/'
                        print(phone_url)
                        phone_json = self.request_to_page(phone_url)
                        phone_arr = json.loads(phone_json.decode('utf8'))
                        phone_string = phone_arr['value']
                        if(phone_string.find("span")):
                            soup_phone = BeautifulSoup(phone_string, "lxml")
                            phone_string = soup_phone.find('span',  {"class": "block"}).text
                            
                        print(phone_string)
                        fo = open(cat.replace('/','')+'.txt', "a")
                        fo.write(phone_string.replace(' ','-')+'\n');
                        fo.close()
                    """
            except:
                links = ''
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://sro.gosnadzor.ru', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
