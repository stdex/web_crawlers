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

pattern_main = "http://search.reteimprese.it"
pattern_url = "http://search.reteimprese.it/index_cerca_all.php?cosa="
#search_keywords = ['falegname', 'fabbro', 'idraulico', 'elettricista', 'impianto%20elettrico', 'infissi', 'serramenti', 'cancelli', 'imbiancatura', 'piastrellisti', 'restauratore']
search_keywords = ['restauratore']
output_filename = 'test_tbl.xlsx'
proxy_list = ['95.68.12.1:11202', '97.95.255.188:10513', '68.206.70.25:3720']

all_items = []
paging_urls = []

work_urls = []
for i in search_keywords:
    current_url = pattern_url + i
    print(current_url)
    
    try:
        request = urllib.request.Request(current_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
        page = urllib.request.urlopen(request)
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

    content = page.read()
    soup = BeautifulSoup(content, "html.parser")
    links_on_pages_s = soup.findAll('div',  {"class": "RIpaginazione_tot_pag"})
    text_num_pages = links_on_pages_s[0].text
    num_pages = re.search(re.escape('di ')+'(.*?)'+re.escape(')'), text_num_pages).group(1)
    print(num_pages)
    for num in range(0,int(num_pages)):
        work_urls.append(pattern_main + '/index_cerca_all.php?s=&pg='+ str(num) + '&k=' + i)
        
    #links_on_pages_s = soup.findAll('div',  {"class": "RIpaginazione_int"})
    #links_on_pages = links_on_pages_s[0].findAll('a')
    #
    #for page_link in links_on_pages:
    #    work_urls.append(pattern_main + page_link.attrs['href'])
    

print(work_urls)

#work_urls = ['http://search.reteimprese.it/index_cerca_all.php?s=&pg=0&k=falegname']

for i in work_urls:
    
    current_url = i
    print(current_url)
    
    url_params = dict([kvpair.split('=') for kvpair in current_url.split('&')])
    search_word = url_params['k']
    
    try:
        request = urllib.request.Request(current_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
        page = urllib.request.urlopen(request)
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

    content = page.read()
    soup = BeautifulSoup(content, "html.parser")
    links_on_pages = soup.findAll('a',  {"class": "RIlink_listing3"})

    for page_link in links_on_pages:
        paging_urls.append({search_word : page_link.attrs['href']})
    
print(paging_urls)