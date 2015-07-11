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
import tav.proxy
import tav.proxy.database
import sqlite3

pattern_main = "http://search.reteimprese.it"
pattern_url = "http://search.reteimprese.it/index_cerca_all.php?cosa="
#search_keywords = ['falegname', 'fabbro', 'idraulico', 'elettricista', 'impianto%20elettrico', 'infissi', 'serramenti', 'cancelli', 'imbiancatura', 'piastrellisti', 'restauratore']
search_keywords = ['falegname']
output_filename = 'test_tbl.xlsx'
#proxy_list = ['95.68.12.1:11202', '97.95.255.188:10513', '68.206.70.25:3720']

PROXY_DATABASE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'proxy.db')

all_items = []
paging_urls = []

"""
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
"""

#work_urls = ['http://search.reteimprese.it/index_cerca_all.php?s=&pg=0&k=falegname']
"""
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
"""

""""""
paging_urls = [{'falegname': 'http://www.reteimprese.it/48283'}, {'falegname': 'http://www.reteimprese.it/37274'}, {'falegname': 'http://www.reteimprese.it/3598'}, {'falegname': 'http://www.reteimprese.it/16495'}, {'falegname': 'http://www.reteimprese.it/22622'}, {'falegname': 'http://www.reteimprese.it/37875'}, {'falegname': 'http://www.reteimprese.it/55412'}, {'falegname': 'http://www.reteimprese.it/100366'}, {'falegname': 'http://www.reteimprese.it/606'}, {'falegname': 'http://www.reteimprese.it/118424'}, {'falegname': 'http://www.reteimprese.it/16276'}, {'falegname': 'http://www.reteimprese.it/2840'}, {'falegname': 'http://www.reteimprese.it/28555'}, {'falegname': 'http://www.reteimprese.it/44123'}, {'falegname': 'http://www.reteimprese.it/121544'}, {'falegname': 'http://www.reteimprese.it/81337'}, {'falegname': 'http://www.reteimprese.it/31101'}, {'falegname': 'http://www.reteimprese.it/90092'}, {'falegname': 'http://www.reteimprese.it/41200'}, {'falegname': 'http://www.reteimprese.it/22128'}, {'falegname': 'http://www.reteimprese.it/107663'}, {'falegname': 'http://www.reteimprese.it/26795'}, {'falegname': 'http://www.reteimprese.it/14001'}, {'falegname': 'http://www.reteimprese.it/42545'}, {'falegname': 'http://www.reteimprese.it/44702'}, {'falegname': 'http://www.reteimprese.it/19148'}, {'falegname': 'http://www.reteimprese.it/36562'}, {'falegname': 'http://www.reteimprese.it/20497'}, {'falegname': 'http://www.reteimprese.it/21368'}, {'falegname': 'http://www.reteimprese.it/27968'}, {'falegname': 'http://www.reteimprese.it/35242'}, {'falegname': 'http://www.reteimprese.it/105887'}, {'falegname': 'http://www.reteimprese.it/96462'}, {'falegname': 'http://www.reteimprese.it/74575'}, {'falegname': 'http://www.reteimprese.it/55156'}, {'falegname': 'http://www.reteimprese.it/33400'}, {'falegname': 'http://www.reteimprese.it/12375'}, {'falegname': 'http://www.reteimprese.it/3667'}, {'falegname': 'http://www.reteimprese.it/32120'}, {'falegname': 'http://www.reteimprese.it/48658'}, {'falegname': 'http://www.reteimprese.it/120946'}, {'falegname': 'http://www.reteimprese.it/427'}, {'falegname': 'http://www.reteimprese.it/45913'}, {'falegname': 'http://www.reteimprese.it/80098'}, {'falegname': 'http://www.reteimprese.it/11567'}, {'falegname': 'http://www.reteimprese.it/69537'}, {'falegname': 'http://www.reteimprese.it/41391'}, {'falegname': 'http://www.reteimprese.it/38925'}, {'falegname': 'http://www.reteimprese.it/24411'}, {'falegname': 'http://www.reteimprese.it/32905'}, {'falegname': 'http://www.reteimprese.it/33575'}, {'falegname': 'http://www.reteimprese.it/54275'}, {'falegname': 'http://www.reteimprese.it/57026'}, {'falegname': 'http://www.reteimprese.it/13323'}, {'falegname': 'http://www.reteimprese.it/8102'}, {'falegname': 'http://www.reteimprese.it/37388'}, {'falegname': 'http://www.reteimprese.it/7829'}, {'falegname': 'http://www.reteimprese.it/96794'}, {'falegname': 'http://www.reteimprese.it/46868'}, {'falegname': 'http://www.reteimprese.it/12389'}, {'falegname': 'http://www.reteimprese.it/41894'}, {'falegname': 'http://www.reteimprese.it/85243'}, {'falegname': 'http://www.reteimprese.it/84188'}, {'falegname': 'http://www.reteimprese.it/23114'}, {'falegname': 'http://www.reteimprese.it/33437'}, {'falegname': 'http://www.reteimprese.it/66405'}, {'falegname': 'http://www.reteimprese.it/14530'}, {'falegname': 'http://www.reteimprese.it/4470'}, {'falegname': 'http://www.reteimprese.it/23745'}, {'falegname': 'http://www.reteimprese.it/112244'}, {'falegname': 'http://www.reteimprese.it/26730'}, {'falegname': 'http://www.reteimprese.it/36108'}, {'falegname': 'http://www.reteimprese.it/106795'}, {'falegname': 'http://www.reteimprese.it/4626'}, {'falegname': 'http://www.reteimprese.it/26632'}, {'falegname': 'http://www.reteimprese.it/34389'}, {'falegname': 'http://www.reteimprese.it/76804'}, {'falegname': 'http://www.reteimprese.it/43060'}, {'falegname': 'http://www.reteimprese.it/28174'}, {'falegname': 'http://www.reteimprese.it/3862'}, {'falegname': 'http://www.reteimprese.it/11172'}, {'falegname': 'http://www.reteimprese.it/1157'}, {'falegname': 'http://www.reteimprese.it/33504'}, {'falegname': 'http://www.reteimprese.it/42710'}, {'falegname': 'http://www.reteimprese.it/12433'}, {'falegname': 'http://www.reteimprese.it/82006'}, {'falegname': 'http://www.reteimprese.it/25483'}, {'falegname': 'http://www.reteimprese.it/75321'}, {'falegname': 'http://www.reteimprese.it/72237'}, {'falegname': 'http://www.reteimprese.it/54133'}, {'falegname': 'http://www.reteimprese.it/12340'}, {'falegname': 'http://www.reteimprese.it/5330'}, {'falegname': 'http://www.reteimprese.it/61820'}, {'falegname': 'http://www.reteimprese.it/25162'}, {'falegname': 'http://www.reteimprese.it/87904'}, {'falegname': 'http://www.reteimprese.it/29711'}, {'falegname': 'http://www.reteimprese.it/38849'}, {'falegname': 'http://www.reteimprese.it/14581'}, {'falegname': 'http://www.reteimprese.it/87982'}, {'falegname': 'http://www.reteimprese.it/96436'}, {'falegname': 'http://www.reteimprese.it/5897'}, {'falegname': 'http://www.reteimprese.it/61821'}, {'falegname': 'http://www.reteimprese.it/18950'}, {'falegname': 'http://www.reteimprese.it/111904'}, {'falegname': 'http://www.reteimprese.it/64230'}, {'falegname': 'http://www.reteimprese.it/78379'}, {'falegname': 'http://www.reteimprese.it/78379'}, {'falegname': 'http://www.reteimprese.it/37321'}, {'falegname': 'http://www.reteimprese.it/90073'}, {'falegname': 'http://www.reteimprese.it/18542'}, {'falegname': 'http://www.reteimprese.it/68578'}, {'falegname': 'http://www.reteimprese.it/24752'}, {'falegname': 'http://www.reteimprese.it/1161'}, {'falegname': 'http://www.reteimprese.it/31718'}, {'falegname': 'http://www.reteimprese.it/79674'}, {'falegname': 'http://www.reteimprese.it/91268'}, {'falegname': 'http://www.reteimprese.it/39142'}, {'falegname': 'http://www.reteimprese.it/9395'}, {'falegname': 'http://www.reteimprese.it/48969'}, {'falegname': 'http://www.reteimprese.it/32543'}, {'falegname': 'http://www.reteimprese.it/108884'}, {'falegname': 'http://www.reteimprese.it/15092'}, {'falegname': 'http://www.reteimprese.it/12023'}, {'falegname': 'http://www.reteimprese.it/115402'}, {'falegname': 'http://www.reteimprese.it/11727'}, {'falegname': 'http://www.reteimprese.it/16867'}, {'falegname': 'http://www.reteimprese.it/23853'}, {'falegname': 'http://www.reteimprese.it/60151'}, {'falegname': 'http://www.reteimprese.it/97174'}, {'falegname': 'http://www.reteimprese.it/695'}, {'falegname': 'http://www.reteimprese.it/70032'}, {'falegname': 'http://www.reteimprese.it/57475'}, {'falegname': 'http://www.reteimprese.it/17755'}, {'falegname': 'http://www.reteimprese.it/81697'}, {'falegname': 'http://www.reteimprese.it/51231'}, {'falegname': 'http://www.reteimprese.it/104018'}, {'falegname': 'http://www.reteimprese.it/57797'}, {'falegname': 'http://www.reteimprese.it/20724'}, {'falegname': 'http://www.reteimprese.it/11628'}, {'falegname': 'http://www.reteimprese.it/11179'}, {'falegname': 'http://www.reteimprese.it/29283'}, {'falegname': 'http://www.reteimprese.it/18311'}, {'falegname': 'http://www.reteimprese.it/72682'}, {'falegname': 'http://www.reteimprese.it/15233'}, {'falegname': 'http://www.reteimprese.it/25426'}, {'falegname': 'http://www.reteimprese.it/48902'}, {'falegname': 'http://www.reteimprese.it/45662'}, {'falegname': 'http://www.reteimprese.it/96134'}, {'falegname': 'http://www.reteimprese.it/44833'}, {'falegname': 'http://www.reteimprese.it/6170'}, {'falegname': 'http://www.reteimprese.it/85552'}, {'falegname': 'http://www.reteimprese.it/8962'}, {'falegname': 'http://www.reteimprese.it/109296'}, {'falegname': 'http://www.reteimprese.it/18715'}, {'falegname': 'http://www.reteimprese.it/85956'}, {'falegname': 'http://www.reteimprese.it/36048'}, {'falegname': 'http://www.reteimprese.it/33611'}, {'falegname': 'http://www.reteimprese.it/81917'}, {'falegname': 'http://www.reteimprese.it/72291'}, {'falegname': 'http://www.reteimprese.it/41418'}, {'falegname': 'http://www.reteimprese.it/35992'}, {'falegname': 'http://www.reteimprese.it/65922'}, {'falegname': 'http://www.reteimprese.it/107379'}, {'falegname': 'http://www.reteimprese.it/38162'}, {'falegname': 'http://www.reteimprese.it/22794'}, {'falegname': 'http://www.reteimprese.it/26027'}, {'falegname': 'http://www.reteimprese.it/8698'}, {'falegname': 'http://www.reteimprese.it/72912'}, {'falegname': 'http://www.reteimprese.it/91386'}, {'falegname': 'http://www.reteimprese.it/55820'}, {'falegname': 'http://www.reteimprese.it/43768'}, {'falegname': 'http://www.reteimprese.it/105619'}, {'falegname': 'http://www.reteimprese.it/51046'}, {'falegname': 'http://www.reteimprese.it/31647'}, {'falegname': 'http://www.reteimprese.it/14157'}, {'falegname': 'http://www.reteimprese.it/10223'}, {'falegname': 'http://www.reteimprese.it/79427'}, {'falegname': 'http://www.reteimprese.it/4729'}, {'falegname': 'http://www.reteimprese.it/7775'}, {'falegname': 'http://www.reteimprese.it/43052'}, {'falegname': 'http://www.reteimprese.it/70504'}, {'falegname': 'http://www.reteimprese.it/49377'}, {'falegname': 'http://www.reteimprese.it/31360'}, {'falegname': 'http://www.reteimprese.it/8619'}, {'falegname': 'http://www.reteimprese.it/79831'}, {'falegname': 'http://www.reteimprese.it/3895'}, {'falegname': 'http://www.reteimprese.it/9738'}, {'falegname': 'http://www.reteimprese.it/9738'}, {'falegname': 'http://www.reteimprese.it/9738'}, {'falegname': 'http://www.reteimprese.it/9738'}, {'falegname': 'http://www.reteimprese.it/74773'}, {'falegname': 'http://www.reteimprese.it/69800'}, {'falegname': 'http://www.reteimprese.it/14611'}, {'falegname': 'http://www.reteimprese.it/7538'}, {'falegname': 'http://www.reteimprese.it/2480'}, {'falegname': 'http://www.reteimprese.it/59837'}, {'falegname': 'http://www.reteimprese.it/3119'}, {'falegname': 'http://www.reteimprese.it/117570'}, {'falegname': 'http://www.reteimprese.it/30634'}, {'falegname': 'http://www.reteimprese.it/28381'}, {'falegname': 'http://www.reteimprese.it/80748'}, {'falegname': 'http://www.reteimprese.it/2317'}, {'falegname': 'http://www.reteimprese.it/52906'}, {'falegname': 'http://www.reteimprese.it/33667'}, {'falegname': 'http://www.reteimprese.it/32898'}, {'falegname': 'http://www.reteimprese.it/21044'}, {'falegname': 'http://www.reteimprese.it/6902'}, {'falegname': 'http://www.reteimprese.it/50508'}, {'falegname': 'http://www.reteimprese.it/16052'}, {'falegname': 'http://www.reteimprese.it/29587'}, {'falegname': 'http://www.reteimprese.it/2542'}, {'falegname': 'http://www.reteimprese.it/5029'}, {'falegname': 'http://www.reteimprese.it/34565'}, {'falegname': 'http://www.reteimprese.it/101042'}, {'falegname': 'http://www.reteimprese.it/32720'}, {'falegname': 'http://www.reteimprese.it/30411'}, {'falegname': 'http://www.reteimprese.it/46199'}, {'falegname': 'http://www.reteimprese.it/8815'}, {'falegname': 'http://www.reteimprese.it/25640'}, {'falegname': 'http://www.reteimprese.it/119986'}, {'falegname': 'http://www.reteimprese.it/81476'}, {'falegname': 'http://www.reteimprese.it/63338'}, {'falegname': 'http://www.reteimprese.it/58392'}, {'falegname': 'http://www.reteimprese.it/20978'}, {'falegname': 'http://www.reteimprese.it/42726'}, {'falegname': 'http://www.reteimprese.it/5333'}, {'falegname': 'http://www.reteimprese.it/3190'}, {'falegname': 'http://www.reteimprese.it/9244'}, {'falegname': 'http://www.reteimprese.it/86568'}, {'falegname': 'http://www.reteimprese.it/16069'}, {'falegname': 'http://www.reteimprese.it/95136'}, {'falegname': 'http://www.reteimprese.it/10424'}, {'falegname': 'http://www.reteimprese.it/59861'}, {'falegname': 'http://www.reteimprese.it/22518'}, {'falegname': 'http://www.reteimprese.it/3511'}, {'falegname': 'http://www.reteimprese.it/92460'}, {'falegname': 'http://www.reteimprese.it/26535'}, {'falegname': 'http://www.reteimprese.it/9004'}, {'falegname': 'http://www.reteimprese.it/43377'}, {'falegname': 'http://www.reteimprese.it/23996'}, {'falegname': 'http://www.reteimprese.it/65520'}, {'falegname': 'http://www.reteimprese.it/14276'}, {'falegname': 'http://www.reteimprese.it/30104'}, {'falegname': 'http://www.reteimprese.it/2919'}, {'falegname': 'http://www.reteimprese.it/36221'}, {'falegname': 'http://www.reteimprese.it/117619'}, {'falegname': 'http://www.reteimprese.it/34768'}, {'falegname': 'http://www.reteimprese.it/58288'}, {'falegname': 'http://www.reteimprese.it/77787'}, {'falegname': 'http://www.reteimprese.it/20765'}, {'falegname': 'http://www.reteimprese.it/91216'}, {'falegname': 'http://www.reteimprese.it/24844'}, {'falegname': 'http://www.reteimprese.it/27578'}, {'falegname': 'http://www.reteimprese.it/42408'}, {'falegname': 'http://www.reteimprese.it/16883'}, {'falegname': 'http://www.reteimprese.it/48528'}, {'falegname': 'http://www.reteimprese.it/106950'}, {'falegname': 'http://www.reteimprese.it/88867'}, {'falegname': 'http://www.reteimprese.it/11735'}, {'falegname': 'http://www.reteimprese.it/55782'}, {'falegname': 'http://www.reteimprese.it/83528'}, {'falegname': 'http://www.reteimprese.it/101916'}, {'falegname': 'http://www.reteimprese.it/112342'}, {'falegname': 'http://www.reteimprese.it/32082'}, {'falegname': 'http://www.reteimprese.it/82742'}, {'falegname': 'http://www.reteimprese.it/96718'}, {'falegname': 'http://www.reteimprese.it/26901'}, {'falegname': 'http://www.reteimprese.it/7571'}, {'falegname': 'http://www.reteimprese.it/36750'}, {'falegname': 'http://www.reteimprese.it/7558'}, {'falegname': 'http://www.reteimprese.it/62296'}, {'falegname': 'http://www.reteimprese.it/66004'}, {'falegname': 'http://www.reteimprese.it/43892'}, {'falegname': 'http://www.reteimprese.it/15156'}, {'falegname': 'http://www.reteimprese.it/6974'}, {'falegname': 'http://www.reteimprese.it/17220'}, {'falegname': 'http://www.reteimprese.it/50184'}, {'falegname': 'http://www.reteimprese.it/41045'}, {'falegname': 'http://www.reteimprese.it/89035'}, {'falegname': 'http://www.reteimprese.it/57172'}, {'falegname': 'http://www.reteimprese.it/86230'}, {'falegname': 'http://www.reteimprese.it/5357'}, {'falegname': 'http://www.reteimprese.it/37621'}, {'falegname': 'http://www.reteimprese.it/81541'}, {'falegname': 'http://www.reteimprese.it/28220'}, {'falegname': 'http://www.reteimprese.it/102356'}, {'falegname': 'http://www.reteimprese.it/86314'}, {'falegname': 'http://www.reteimprese.it/16478'}, {'falegname': 'http://www.reteimprese.it/77384'}, {'falegname': 'http://www.reteimprese.it/13675'}, {'falegname': 'http://www.reteimprese.it/18254'}, {'falegname': 'http://www.reteimprese.it/2657'}, {'falegname': 'http://www.reteimprese.it/57742'}, {'falegname': 'http://www.reteimprese.it/14214'}, {'falegname': 'http://www.reteimprese.it/91638'}, {'falegname': 'http://www.reteimprese.it/33726'}, {'falegname': 'http://www.reteimprese.it/90525'}, {'falegname': 'http://www.reteimprese.it/2878'}, {'falegname': 'http://www.reteimprese.it/109832'}, {'falegname': 'http://www.reteimprese.it/23903'}, {'falegname': 'http://www.reteimprese.it/34995'}, {'falegname': 'http://www.reteimprese.it/4977'}, {'falegname': 'http://www.reteimprese.it/10620'}, {'falegname': 'http://www.reteimprese.it/61551'}, {'falegname': 'http://www.reteimprese.it/23497'}, {'falegname': 'http://www.reteimprese.it/7467'}, {'falegname': 'http://www.reteimprese.it/78980'}, {'falegname': 'http://www.reteimprese.it/98588'}, {'falegname': 'http://www.reteimprese.it/47366'}, {'falegname': 'http://www.reteimprese.it/7297'}, {'falegname': 'http://www.reteimprese.it/3603'}, {'falegname': 'http://www.reteimprese.it/13115'}, {'falegname': 'http://www.reteimprese.it/121088'}, {'falegname': 'http://www.reteimprese.it/61910'}, {'falegname': 'http://www.reteimprese.it/85739'}, {'falegname': 'http://www.reteimprese.it/4458'}, {'falegname': 'http://www.reteimprese.it/41764'}, {'falegname': 'http://www.reteimprese.it/3829'}, {'falegname': 'http://www.reteimprese.it/36029'}, {'falegname': 'http://www.reteimprese.it/17675'}, {'falegname': 'http://www.reteimprese.it/98308'}, {'falegname': 'http://www.reteimprese.it/59230'}, {'falegname': 'http://www.reteimprese.it/79007'}, {'falegname': 'http://www.reteimprese.it/1896'}, {'falegname': 'http://www.reteimprese.it/108458'}, {'falegname': 'http://www.reteimprese.it/33700'}, {'falegname': 'http://www.reteimprese.it/79114'}, {'falegname': 'http://www.reteimprese.it/8'}, {'falegname': 'http://www.reteimprese.it/8'}, {'falegname': 'http://www.reteimprese.it/8'}, {'falegname': 'http://www.reteimprese.it/8'}, {'falegname': 'http://www.reteimprese.it/8'}, {'falegname': 'http://www.reteimprese.it/3745'}, {'falegname': 'http://www.reteimprese.it/6822'}, {'falegname': 'http://www.reteimprese.it/23202'}, {'falegname': 'http://www.reteimprese.it/36936'}, {'falegname': 'http://www.reteimprese.it/11325'}, {'falegname': 'http://www.reteimprese.it/40616'}, {'falegname': 'http://www.reteimprese.it/30467'}, {'falegname': 'http://www.reteimprese.it/82371'}, {'falegname': 'http://www.reteimprese.it/98125'}, {'falegname': 'http://www.reteimprese.it/52960'}, {'falegname': 'http://www.reteimprese.it/60299'}, {'falegname': 'http://www.reteimprese.it/17817'}, {'falegname': 'http://www.reteimprese.it/64094'}, {'falegname': 'http://www.reteimprese.it/34418'}, {'falegname': 'http://www.reteimprese.it/17937'}, {'falegname': 'http://www.reteimprese.it/69068'}, {'falegname': 'http://www.reteimprese.it/18156'}, {'falegname': 'http://www.reteimprese.it/33883'}, {'falegname': 'http://www.reteimprese.it/55001'}, {'falegname': 'http://www.reteimprese.it/82291'}, {'falegname': 'http://www.reteimprese.it/27914'}, {'falegname': 'http://www.reteimprese.it/2101'}, {'falegname': 'http://www.reteimprese.it/76789'}, {'falegname': 'http://www.reteimprese.it/70776'}, {'falegname': 'http://www.reteimprese.it/46922'}, {'falegname': 'http://www.reteimprese.it/20399'}, {'falegname': 'http://www.reteimprese.it/43110'}, {'falegname': 'http://www.reteimprese.it/65664'}, {'falegname': 'http://www.reteimprese.it/24472'}, {'falegname': 'http://www.reteimprese.it/70112'}, {'falegname': 'http://www.reteimprese.it/101241'}, {'falegname': 'http://www.reteimprese.it/4816'}, {'falegname': 'http://www.reteimprese.it/115856'}, {'falegname': 'http://www.reteimprese.it/29984'}, {'falegname': 'http://www.reteimprese.it/118674'}, {'falegname': 'http://www.reteimprese.it/79514'}, {'falegname': 'http://www.reteimprese.it/39005'}, {'falegname': 'http://www.reteimprese.it/35503'}, {'falegname': 'http://www.reteimprese.it/54937'}, {'falegname': 'http://www.reteimprese.it/27506'}, {'falegname': 'http://www.reteimprese.it/19957'}, {'falegname': 'http://www.reteimprese.it/43193'}, {'falegname': 'http://www.reteimprese.it/37397'}, {'falegname': 'http://www.reteimprese.it/28464'}, {'falegname': 'http://www.reteimprese.it/42784'}, {'falegname': 'http://www.reteimprese.it/120190'}, {'falegname': 'http://www.reteimprese.it/69483'}, {'falegname': 'http://www.reteimprese.it/46469'}, {'falegname': 'http://www.reteimprese.it/38014'}, {'falegname': 'http://www.reteimprese.it/16752'}, {'falegname': 'http://www.reteimprese.it/118859'}, {'falegname': 'http://www.reteimprese.it/118859'}, {'falegname': 'http://www.reteimprese.it/58595'}, {'falegname': 'http://www.reteimprese.it/17604'}, {'falegname': 'http://www.reteimprese.it/57772'}, {'falegname': 'http://www.reteimprese.it/53664'}, {'falegname': 'http://www.reteimprese.it/19760'}, {'falegname': 'http://www.reteimprese.it/47523'}, {'falegname': 'http://www.reteimprese.it/65058'}, {'falegname': 'http://www.reteimprese.it/74010'}, {'falegname': 'http://www.reteimprese.it/57968'}, {'falegname': 'http://www.reteimprese.it/6738'}, {'falegname': 'http://www.reteimprese.it/7018'}, {'falegname': 'http://www.reteimprese.it/59035'}, {'falegname': 'http://www.reteimprese.it/59541'}, {'falegname': 'http://www.reteimprese.it/113163'}, {'falegname': 'http://www.reteimprese.it/3365'}, {'falegname': 'http://www.reteimprese.it/418'}, {'falegname': 'http://www.reteimprese.it/97113'}, {'falegname': 'http://www.reteimprese.it/41376'}, {'falegname': 'http://www.reteimprese.it/13067'}, {'falegname': 'http://www.reteimprese.it/24863'}, {'falegname': 'http://www.reteimprese.it/57321'}, {'falegname': 'http://www.reteimprese.it/29144'}, {'falegname': 'http://www.reteimprese.it/95885'}, {'falegname': 'http://www.reteimprese.it/81759'}, {'falegname': 'http://www.reteimprese.it/10565'}, {'falegname': 'http://www.reteimprese.it/11495'}, {'falegname': 'http://www.reteimprese.it/40669'}, {'falegname': 'http://www.reteimprese.it/50294'}, {'falegname': 'http://www.reteimprese.it/2218'}, {'falegname': 'http://www.reteimprese.it/14800'}, {'falegname': 'http://www.reteimprese.it/106892'}, {'falegname': 'http://www.reteimprese.it/30457'}, {'falegname': 'http://www.reteimprese.it/70826'}, {'falegname': 'http://www.reteimprese.it/75988'}, {'falegname': 'http://www.reteimprese.it/94372'}, {'falegname': 'http://www.reteimprese.it/37836'}, {'falegname': 'http://www.reteimprese.it/63150'}, {'falegname': 'http://www.reteimprese.it/86763'}, {'falegname': 'http://www.reteimprese.it/12303'}, {'falegname': 'http://www.reteimprese.it/60687'}, {'falegname': 'http://www.reteimprese.it/60687'}, {'falegname': 'http://www.reteimprese.it/68279'}, {'falegname': 'http://www.reteimprese.it/7350'}, {'falegname': 'http://www.reteimprese.it/32805'}, {'falegname': 'http://www.reteimprese.it/6008'}, {'falegname': 'http://www.reteimprese.it/18737'}, {'falegname': 'http://www.reteimprese.it/118312'}, {'falegname': 'http://www.reteimprese.it/17170'}, {'falegname': 'http://www.reteimprese.it/22557'}, {'falegname': 'http://www.reteimprese.it/26205'}, {'falegname': 'http://www.reteimprese.it/23682'}, {'falegname': 'http://www.reteimprese.it/29529'}, {'falegname': 'http://www.reteimprese.it/67031'}, {'falegname': 'http://www.reteimprese.it/2511'}, {'falegname': 'http://www.reteimprese.it/94848'}, {'falegname': 'http://www.reteimprese.it/3120'}, {'falegname': 'http://www.reteimprese.it/10004'}, {'falegname': 'http://www.reteimprese.it/35331'}, {'falegname': 'http://www.reteimprese.it/1838'}, {'falegname': 'http://www.reteimprese.it/3789'}, {'falegname': 'http://www.reteimprese.it/62179'}, {'falegname': 'http://www.reteimprese.it/16815'}, {'falegname': 'http://www.reteimprese.it/1623'}, {'falegname': 'http://www.reteimprese.it/3116'}, {'falegname': 'http://www.reteimprese.it/107991'}, {'falegname': 'http://www.reteimprese.it/812'}, {'falegname': 'http://www.reteimprese.it/86708'}, {'falegname': 'http://www.reteimprese.it/5954'}, {'falegname': 'http://www.reteimprese.it/2818'}, {'falegname': 'http://www.reteimprese.it/48871'}, {'falegname': 'http://www.reteimprese.it/2115'}, {'falegname': 'http://www.reteimprese.it/30981'}, {'falegname': 'http://www.reteimprese.it/102808'}, {'falegname': 'http://www.reteimprese.it/10559'}, {'falegname': 'http://www.reteimprese.it/46863'}, {'falegname': 'http://www.reteimprese.it/16536'}, {'falegname': 'http://www.reteimprese.it/10955'}, {'falegname': 'http://www.reteimprese.it/38080'}, {'falegname': 'http://www.reteimprese.it/499'}, {'falegname': 'http://www.reteimprese.it/51963'}, {'falegname': 'http://www.reteimprese.it/1105'}, {'falegname': 'http://www.reteimprese.it/93592'}, {'falegname': 'http://www.reteimprese.it/1679'}, {'falegname': 'http://www.reteimprese.it/16167'}, {'falegname': 'http://www.reteimprese.it/56850'}, {'falegname': 'http://www.reteimprese.it/3241'}, {'falegname': 'http://www.reteimprese.it/728'}, {'falegname': 'http://www.reteimprese.it/103611'}, {'falegname': 'http://www.reteimprese.it/45616'}, {'falegname': 'http://www.reteimprese.it/17617'}, {'falegname': 'http://www.reteimprese.it/20413'}, {'falegname': 'http://www.reteimprese.it/56746'}, {'falegname': 'http://www.reteimprese.it/8902'}, {'falegname': 'http://www.reteimprese.it/8971'}, {'falegname': 'http://www.reteimprese.it/75298'}, {'falegname': 'http://www.reteimprese.it/81900'}, {'falegname': 'http://www.reteimprese.it/42885'}, {'falegname': 'http://www.reteimprese.it/42162'}, {'falegname': 'http://www.reteimprese.it/27125'}, {'falegname': 'http://www.reteimprese.it/117591'}, {'falegname': 'http://www.reteimprese.it/108820'}, {'falegname': 'http://www.reteimprese.it/68228'}, {'falegname': 'http://www.reteimprese.it/24363'}, {'falegname': 'http://www.reteimprese.it/24785'}, {'falegname': 'http://www.reteimprese.it/36494'}, {'falegname': 'http://www.reteimprese.it/40989'}, {'falegname': 'http://www.reteimprese.it/13965'}, {'falegname': 'http://www.reteimprese.it/25546'}, {'falegname': 'http://www.reteimprese.it/13570'}, {'falegname': 'http://www.reteimprese.it/45935'}, {'falegname': 'http://www.reteimprese.it/27282'}, {'falegname': 'http://www.reteimprese.it/87493'}, {'falegname': 'http://www.reteimprese.it/16324'}, {'falegname': 'http://www.reteimprese.it/70962'}, {'falegname': 'http://www.reteimprese.it/9159'}, {'falegname': 'http://www.reteimprese.it/102035'}, {'falegname': 'http://www.reteimprese.it/11345'}, {'falegname': 'http://www.reteimprese.it/20732'}, {'falegname': 'http://www.reteimprese.it/34621'}, {'falegname': 'http://www.reteimprese.it/14498'}, {'falegname': 'http://www.reteimprese.it/15471'}, {'falegname': 'http://www.reteimprese.it/8401'}, {'falegname': 'http://www.reteimprese.it/114444'}, {'falegname': 'http://www.reteimprese.it/99890'}, {'falegname': 'http://www.reteimprese.it/74208'}, {'falegname': 'http://www.reteimprese.it/76816'}, {'falegname': 'http://www.reteimprese.it/96448'}, {'falegname': 'http://www.reteimprese.it/2121'}, {'falegname': 'http://www.reteimprese.it/86037'}, {'falegname': 'http://www.reteimprese.it/47655'}, {'falegname': 'http://www.reteimprese.it/9198'}, {'falegname': 'http://www.reteimprese.it/116564'}, {'falegname': 'http://www.reteimprese.it/13601'}, {'falegname': 'http://www.reteimprese.it/74901'}, {'falegname': 'http://www.reteimprese.it/101679'}, {'falegname': 'http://www.reteimprese.it/28227'}, {'falegname': 'http://www.reteimprese.it/2593'}, {'falegname': 'http://www.reteimprese.it/604'}, {'falegname': 'http://www.reteimprese.it/1498'}, {'falegname': 'http://www.reteimprese.it/43946'}, {'falegname': 'http://www.reteimprese.it/8886'}, {'falegname': 'http://www.reteimprese.it/25088'}, {'falegname': 'http://www.reteimprese.it/68071'}, {'falegname': 'http://www.reteimprese.it/42448'}, {'falegname': 'http://www.reteimprese.it/58498'}, {'falegname': 'http://www.reteimprese.it/55647'}, {'falegname': 'http://www.reteimprese.it/37772'}, {'falegname': 'http://www.reteimprese.it/102514'}, {'falegname': 'http://www.reteimprese.it/49228'}, {'falegname': 'http://www.reteimprese.it/39885'}, {'falegname': 'http://www.reteimprese.it/27293'}, {'falegname': 'http://www.reteimprese.it/31143'}, {'falegname': 'http://www.reteimprese.it/55833'}, {'falegname': 'http://www.reteimprese.it/7417'}, {'falegname': 'http://www.reteimprese.it/94970'}, {'falegname': 'http://www.reteimprese.it/63640'}, {'falegname': 'http://www.reteimprese.it/56525'}, {'falegname': 'http://www.reteimprese.it/12630'}, {'falegname': 'http://www.reteimprese.it/37519'}, {'falegname': 'http://www.reteimprese.it/46864'}, {'falegname': 'http://www.reteimprese.it/47648'}, {'falegname': 'http://www.reteimprese.it/59234'}, {'falegname': 'http://www.reteimprese.it/25969'}, {'falegname': 'http://www.reteimprese.it/34160'}, {'falegname': 'http://www.reteimprese.it/42707'}, {'falegname': 'http://www.reteimprese.it/34881'}, {'falegname': 'http://www.reteimprese.it/14129'}, {'falegname': 'http://www.reteimprese.it/395'}, {'falegname': 'http://www.reteimprese.it/108775'}, {'falegname': 'http://www.reteimprese.it/65957'}, {'falegname': 'http://www.reteimprese.it/34355'}, {'falegname': 'http://www.reteimprese.it/84196'}, {'falegname': 'http://www.reteimprese.it/50730'}, {'falegname': 'http://www.reteimprese.it/63086'}, {'falegname': 'http://www.reteimprese.it/36603'}, {'falegname': 'http://www.reteimprese.it/20260'}, {'falegname': 'http://www.reteimprese.it/103807'}, {'falegname': 'http://www.reteimprese.it/25781'}, {'falegname': 'http://www.reteimprese.it/19819'}, {'falegname': 'http://www.reteimprese.it/116527'}, {'falegname': 'http://www.reteimprese.it/54421'}, {'falegname': 'http://www.reteimprese.it/10881'}, {'falegname': 'http://www.reteimprese.it/93679'}, {'falegname': 'http://www.reteimprese.it/80754'}, {'falegname': 'http://www.reteimprese.it/65109'}, {'falegname': 'http://www.reteimprese.it/97577'}, {'falegname': 'http://www.reteimprese.it/67767'}, {'falegname': 'http://www.reteimprese.it/60287'}, {'falegname': 'http://www.reteimprese.it/19659'}, {'falegname': 'http://www.reteimprese.it/61995'}, {'falegname': 'http://www.reteimprese.it/39598'}, {'falegname': 'http://www.reteimprese.it/39420'}, {'falegname': 'http://www.reteimprese.it/62502'}, {'falegname': 'http://www.reteimprese.it/29773'}, {'falegname': 'http://www.reteimprese.it/16734'}, {'falegname': 'http://www.reteimprese.it/67174'}, {'falegname': 'http://www.reteimprese.it/66639'}, {'falegname': 'http://www.reteimprese.it/92098'}, {'falegname': 'http://www.reteimprese.it/69934'}, {'falegname': 'http://www.reteimprese.it/55121'}, {'falegname': 'http://www.reteimprese.it/6504'}, {'falegname': 'http://www.reteimprese.it/84101'}, {'falegname': 'http://www.reteimprese.it/10263'}, {'falegname': 'http://www.reteimprese.it/10145'}, {'falegname': 'http://www.reteimprese.it/31168'}, {'falegname': 'http://www.reteimprese.it/12520'}, {'falegname': 'http://www.reteimprese.it/50026'}, {'falegname': 'http://www.reteimprese.it/33196'}, {'falegname': 'http://www.reteimprese.it/19804'}, {'falegname': 'http://www.reteimprese.it/1304'}, {'falegname': 'http://www.reteimprese.it/13330'}, {'falegname': 'http://www.reteimprese.it/55804'}, {'falegname': 'http://www.reteimprese.it/11454'}, {'falegname': 'http://www.reteimprese.it/20117'}, {'falegname': 'http://www.reteimprese.it/16633'}, {'falegname': 'http://www.reteimprese.it/18180'}, {'falegname': 'http://www.reteimprese.it/93973'}, {'falegname': 'http://www.reteimprese.it/10030'}, {'falegname': 'http://www.reteimprese.it/51168'}, {'falegname': 'http://www.reteimprese.it/36049'}, {'falegname': 'http://www.reteimprese.it/22517'}, {'falegname': 'http://www.reteimprese.it/24817'}, {'falegname': 'http://www.reteimprese.it/26412'}, {'falegname': 'http://www.reteimprese.it/23077'}, {'falegname': 'http://www.reteimprese.it/55049'}, {'falegname': 'http://www.reteimprese.it/77375'}, {'falegname': 'http://www.reteimprese.it/17753'}, {'falegname': 'http://www.reteimprese.it/30866'}, {'falegname': 'http://www.reteimprese.it/46682'}, {'falegname': 'http://www.reteimprese.it/59118'}, {'falegname': 'http://www.reteimprese.it/33719'}, {'falegname': 'http://www.reteimprese.it/315'}, {'falegname': 'http://www.reteimprese.it/97575'}, {'falegname': 'http://www.reteimprese.it/19695'}, {'falegname': 'http://www.reteimprese.it/87377'}, {'falegname': 'http://www.reteimprese.it/69900'}, {'falegname': 'http://www.reteimprese.it/116629'}, {'falegname': 'http://www.reteimprese.it/103292'}, {'falegname': 'http://www.reteimprese.it/80340'}, {'falegname': 'http://www.reteimprese.it/1726'}, {'falegname': 'http://www.reteimprese.it/36421'}, {'falegname': 'http://www.reteimprese.it/36421'}, {'falegname': 'http://www.reteimprese.it/97434'}, {'falegname': 'http://www.reteimprese.it/1360'}, {'falegname': 'http://www.reteimprese.it/16470'}, {'falegname': 'http://www.reteimprese.it/5228'}, {'falegname': 'http://www.reteimprese.it/4164'}, {'falegname': 'http://www.reteimprese.it/73885'}, {'falegname': 'http://www.reteimprese.it/40482'}, {'falegname': 'http://www.reteimprese.it/60070'}, {'falegname': 'http://www.reteimprese.it/2830'}, {'falegname': 'http://www.reteimprese.it/86999'}, {'falegname': 'http://www.reteimprese.it/10672'}, {'falegname': 'http://www.reteimprese.it/117584'}, {'falegname': 'http://www.reteimprese.it/49018'}, {'falegname': 'http://www.reteimprese.it/85604'}, {'falegname': 'http://www.reteimprese.it/5787'}, {'falegname': 'http://www.reteimprese.it/5215'}, {'falegname': 'http://www.reteimprese.it/89163'}, {'falegname': 'http://www.reteimprese.it/13469'}, {'falegname': 'http://www.reteimprese.it/72108'}, {'falegname': 'http://www.reteimprese.it/19046'}, {'falegname': 'http://www.reteimprese.it/97508'}, {'falegname': 'http://www.reteimprese.it/49533'}, {'falegname': 'http://www.reteimprese.it/115875'}, {'falegname': 'http://www.reteimprese.it/31834'}, {'falegname': 'http://www.reteimprese.it/19291'}, {'falegname': 'http://www.reteimprese.it/72018'}, {'falegname': 'http://www.reteimprese.it/98635'}, {'falegname': 'http://www.reteimprese.it/127303'}, {'falegname': 'http://www.reteimprese.it/64899'}, {'falegname': 'http://www.reteimprese.it/72934'}, {'falegname': 'http://www.reteimprese.it/46925'}, {'falegname': 'http://www.reteimprese.it/9028'}, {'falegname': 'http://www.reteimprese.it/34015'}, {'falegname': 'http://www.reteimprese.it/17786'}, {'falegname': 'http://www.reteimprese.it/33466'}, {'falegname': 'http://www.reteimprese.it/63200'}, {'falegname': 'http://www.reteimprese.it/33286'}, {'falegname': 'http://www.reteimprese.it/25840'}, {'falegname': 'http://www.reteimprese.it/58231'}, {'falegname': 'http://www.reteimprese.it/82609'}, {'falegname': 'http://www.reteimprese.it/2210'}, {'falegname': 'http://www.reteimprese.it/8883'}, {'falegname': 'http://www.reteimprese.it/17341'}, {'falegname': 'http://www.reteimprese.it/114256'}, {'falegname': 'http://www.reteimprese.it/8240'}, {'falegname': 'http://www.reteimprese.it/31166'}, {'falegname': 'http://www.reteimprese.it/94419'}, {'falegname': 'http://www.reteimprese.it/42576'}, {'falegname': 'http://www.reteimprese.it/30266'}, {'falegname': 'http://www.reteimprese.it/26031'}, {'falegname': 'http://www.reteimprese.it/44215'}, {'falegname': 'http://www.reteimprese.it/118970'}, {'falegname': 'http://www.reteimprese.it/62433'}, {'falegname': 'http://www.reteimprese.it/67919'}, {'falegname': 'http://www.reteimprese.it/50506'}, {'falegname': 'http://www.reteimprese.it/19798'}, {'falegname': 'http://www.reteimprese.it/22481'}, {'falegname': 'http://www.reteimprese.it/75105'}, {'falegname': 'http://www.reteimprese.it/111911'}, {'falegname': 'http://www.reteimprese.it/12529'}, {'falegname': 'http://www.reteimprese.it/29132'}, {'falegname': 'http://www.reteimprese.it/78933'}, {'falegname': 'http://www.reteimprese.it/39765'}, {'falegname': 'http://www.reteimprese.it/4300'}, {'falegname': 'http://www.reteimprese.it/59068'}, {'falegname': 'http://www.reteimprese.it/34380'}, {'falegname': 'http://www.reteimprese.it/62629'}, {'falegname': 'http://www.reteimprese.it/35407'}, {'falegname': 'http://www.reteimprese.it/583'}, {'falegname': 'http://www.reteimprese.it/23397'}, {'falegname': 'http://www.reteimprese.it/52421'}, {'falegname': 'http://www.reteimprese.it/2894'}, {'falegname': 'http://www.reteimprese.it/10879'}, {'falegname': 'http://www.reteimprese.it/94856'}, {'falegname': 'http://www.reteimprese.it/46544'}, {'falegname': 'http://www.reteimprese.it/41283'}, {'falegname': 'http://www.reteimprese.it/38096'}, {'falegname': 'http://www.reteimprese.it/55152'}, {'falegname': 'http://www.reteimprese.it/11349'}, {'falegname': 'http://www.reteimprese.it/5437'}, {'falegname': 'http://www.reteimprese.it/34580'}, {'falegname': 'http://www.reteimprese.it/28034'}, {'falegname': 'http://www.reteimprese.it/44747'}, {'falegname': 'http://www.reteimprese.it/45887'}, {'falegname': 'http://www.reteimprese.it/92798'}, {'falegname': 'http://www.reteimprese.it/32585'}, {'falegname': 'http://www.reteimprese.it/28113'}, {'falegname': 'http://www.reteimprese.it/90074'}, {'falegname': 'http://www.reteimprese.it/55280'}, {'falegname': 'http://www.reteimprese.it/115501'}, {'falegname': 'http://www.reteimprese.it/37632'}, {'falegname': 'http://www.reteimprese.it/5692'}, {'falegname': 'http://www.reteimprese.it/16245'}, {'falegname': 'http://www.reteimprese.it/4094'}, {'falegname': 'http://www.reteimprese.it/67385'}, {'falegname': 'http://www.reteimprese.it/26226'}, {'falegname': 'http://www.reteimprese.it/89949'}, {'falegname': 'http://www.reteimprese.it/13932'}, {'falegname': 'http://www.reteimprese.it/17262'}, {'falegname': 'http://www.reteimprese.it/730'}, {'falegname': 'http://www.reteimprese.it/31717'}, {'falegname': 'http://www.reteimprese.it/34112'}, {'falegname': 'http://www.reteimprese.it/4329'}, {'falegname': 'http://www.reteimprese.it/40240'}, {'falegname': 'http://www.reteimprese.it/15806'}, {'falegname': 'http://www.reteimprese.it/26349'}, {'falegname': 'http://www.reteimprese.it/121470'}, {'falegname': 'http://www.reteimprese.it/71182'}, {'falegname': 'http://www.reteimprese.it/42960'}, {'falegname': 'http://www.reteimprese.it/65887'}, {'falegname': 'http://www.reteimprese.it/718'}, {'falegname': 'http://www.reteimprese.it/51372'}, {'falegname': 'http://www.reteimprese.it/50134'}, {'falegname': 'http://www.reteimprese.it/103154'}, {'falegname': 'http://www.reteimprese.it/19873'}, {'falegname': 'http://www.reteimprese.it/39378'}, {'falegname': 'http://www.reteimprese.it/14854'}, {'falegname': 'http://www.reteimprese.it/61708'}, {'falegname': 'http://www.reteimprese.it/16592'}, {'falegname': 'http://www.reteimprese.it/26800'}, {'falegname': 'http://www.reteimprese.it/65795'}, {'falegname': 'http://www.reteimprese.it/21820'}, {'falegname': 'http://www.reteimprese.it/30479'}, {'falegname': 'http://www.reteimprese.it/10071'}, {'falegname': 'http://www.reteimprese.it/34117'}, {'falegname': 'http://www.reteimprese.it/16330'}, {'falegname': 'http://www.reteimprese.it/452'}, {'falegname': 'http://www.reteimprese.it/66350'}, {'falegname': 'http://www.reteimprese.it/5946'}, {'falegname': 'http://www.reteimprese.it/13231'}, {'falegname': 'http://www.reteimprese.it/10985'}, {'falegname': 'http://www.reteimprese.it/5993'}, {'falegname': 'http://www.reteimprese.it/63252'}, {'falegname': 'http://www.reteimprese.it/89551'}, {'falegname': 'http://www.reteimprese.it/7303'}, {'falegname': 'http://www.reteimprese.it/906'}, {'falegname': 'http://www.reteimprese.it/28776'}, {'falegname': 'http://www.reteimprese.it/29567'}, {'falegname': 'http://www.reteimprese.it/21129'}, {'falegname': 'http://www.reteimprese.it/19453'}, {'falegname': 'http://www.reteimprese.it/11474'}, {'falegname': 'http://www.reteimprese.it/13481'}, {'falegname': 'http://www.reteimprese.it/17093'}, {'falegname': 'http://www.reteimprese.it/5844'}, {'falegname': 'http://www.reteimprese.it/38742'}, {'falegname': 'http://www.reteimprese.it/105283'}, {'falegname': 'http://www.reteimprese.it/59547'}, {'falegname': 'http://www.reteimprese.it/84460'}, {'falegname': 'http://www.reteimprese.it/22082'}, {'falegname': 'http://www.reteimprese.it/19262'}, {'falegname': 'http://www.reteimprese.it/10015'}, {'falegname': 'http://www.reteimprese.it/85159'}, {'falegname': 'http://www.reteimprese.it/93717'}, {'falegname': 'http://www.reteimprese.it/58952'}, {'falegname': 'http://www.reteimprese.it/23937'}, {'falegname': 'http://www.reteimprese.it/3367'}, {'falegname': 'http://www.reteimprese.it/29109'}, {'falegname': 'http://www.reteimprese.it/4224'}, {'falegname': 'http://www.reteimprese.it/397'}, {'falegname': 'http://www.reteimprese.it/55233'}, {'falegname': 'http://www.reteimprese.it/37125'}, {'falegname': 'http://www.reteimprese.it/91181'}, {'falegname': 'http://www.reteimprese.it/29047'}, {'falegname': 'http://www.reteimprese.it/37909'}, {'falegname': 'http://www.reteimprese.it/5723'}, {'falegname': 'http://www.reteimprese.it/13217'}, {'falegname': 'http://www.reteimprese.it/13243'}, {'falegname': 'http://www.reteimprese.it/43533'}, {'falegname': 'http://www.reteimprese.it/51128'}, {'falegname': 'http://www.reteimprese.it/35219'}, {'falegname': 'http://www.reteimprese.it/43984'}, {'falegname': 'http://www.reteimprese.it/115167'}, {'falegname': 'http://www.reteimprese.it/26328'}, {'falegname': 'http://www.reteimprese.it/19055'}, {'falegname': 'http://www.reteimprese.it/19414'}, {'falegname': 'http://www.reteimprese.it/1464'}, {'falegname': 'http://www.reteimprese.it/6058'}, {'falegname': 'http://www.reteimprese.it/68097'}, {'falegname': 'http://www.reteimprese.it/3517'}, {'falegname': 'http://www.reteimprese.it/14336'}, {'falegname': 'http://www.reteimprese.it/9328'}, {'falegname': 'http://www.reteimprese.it/11869'}, {'falegname': 'http://www.reteimprese.it/1895'}, {'falegname': 'http://www.reteimprese.it/21156'}, {'falegname': 'http://www.reteimprese.it/53808'}, {'falegname': 'http://www.reteimprese.it/35669'}, {'falegname': 'http://www.reteimprese.it/5576'}, {'falegname': 'http://www.reteimprese.it/20191'}, {'falegname': 'http://www.reteimprese.it/13127'}, {'falegname': 'http://www.reteimprese.it/16542'}, {'falegname': 'http://www.reteimprese.it/16542'}, {'falegname': 'http://www.reteimprese.it/7517'}, {'falegname': 'http://www.reteimprese.it/112998'}, {'falegname': 'http://www.reteimprese.it/9575'}, {'falegname': 'http://www.reteimprese.it/35225'}, {'falegname': 'http://www.reteimprese.it/19216'}, {'falegname': 'http://www.reteimprese.it/68697'}, {'falegname': 'http://www.reteimprese.it/16652'}, {'falegname': 'http://www.reteimprese.it/8127'}, {'falegname': 'http://www.reteimprese.it/21079'}, {'falegname': 'http://www.reteimprese.it/90153'}, {'falegname': 'http://www.reteimprese.it/48587'}, {'falegname': 'http://www.reteimprese.it/28936'}, {'falegname': 'http://www.reteimprese.it/110420'}, {'falegname': 'http://www.reteimprese.it/41163'}, {'falegname': 'http://www.reteimprese.it/50983'}, {'falegname': 'http://www.reteimprese.it/40415'}, {'falegname': 'http://www.reteimprese.it/54289'}, {'falegname': 'http://www.reteimprese.it/5883'}, {'falegname': 'http://www.reteimprese.it/1786'}, {'falegname': 'http://www.reteimprese.it/10117'}, {'falegname': 'http://www.reteimprese.it/80596'}, {'falegname': 'http://www.reteimprese.it/65828'}, {'falegname': 'http://www.reteimprese.it/36103'}, {'falegname': 'http://www.reteimprese.it/42359'}, {'falegname': 'http://www.reteimprese.it/17075'}, {'falegname': 'http://www.reteimprese.it/76361'}, {'falegname': 'http://www.reteimprese.it/5403'}, {'falegname': 'http://www.reteimprese.it/24536'}, {'falegname': 'http://www.reteimprese.it/48432'}, {'falegname': 'http://www.reteimprese.it/30967'}, {'falegname': 'http://www.reteimprese.it/9184'}, {'falegname': 'http://www.reteimprese.it/100029'}, {'falegname': 'http://www.reteimprese.it/15307'}, {'falegname': 'http://www.reteimprese.it/17527'}, {'falegname': 'http://www.reteimprese.it/45646'}, {'falegname': 'http://www.reteimprese.it/11892'}, {'falegname': 'http://www.reteimprese.it/12932'}, {'falegname': 'http://www.reteimprese.it/21059'}, {'falegname': 'http://www.reteimprese.it/19581'}, {'falegname': 'http://www.reteimprese.it/20741'}, {'falegname': 'http://www.reteimprese.it/16248'}, {'falegname': 'http://www.reteimprese.it/2178'}, {'falegname': 'http://www.reteimprese.it/55860'}, {'falegname': 'http://www.reteimprese.it/18039'}, {'falegname': 'http://www.reteimprese.it/89880'}, {'falegname': 'http://www.reteimprese.it/10318'}, {'falegname': 'http://www.reteimprese.it/82191'}, {'falegname': 'http://www.reteimprese.it/117804'}, {'falegname': 'http://www.reteimprese.it/7159'}, {'falegname': 'http://www.reteimprese.it/28028'}, {'falegname': 'http://www.reteimprese.it/47118'}, {'falegname': 'http://www.reteimprese.it/1583'}, {'falegname': 'http://www.reteimprese.it/16817'}, {'falegname': 'http://www.reteimprese.it/86634'}, {'falegname': 'http://www.reteimprese.it/74243'}, {'falegname': 'http://www.reteimprese.it/52478'}, {'falegname': 'http://www.reteimprese.it/111695'}, {'falegname': 'http://www.reteimprese.it/1858'}, {'falegname': 'http://www.reteimprese.it/110982'}, {'falegname': 'http://www.reteimprese.it/6075'}, {'falegname': 'http://www.reteimprese.it/45555'}, {'falegname': 'http://www.reteimprese.it/68762'}, {'falegname': 'http://www.reteimprese.it/15799'}, {'falegname': 'http://www.reteimprese.it/9677'}, {'falegname': 'http://www.reteimprese.it/35098'}, {'falegname': 'http://www.reteimprese.it/1172'}, {'falegname': 'http://www.reteimprese.it/21474'}, {'falegname': 'http://www.reteimprese.it/26975'}, {'falegname': 'http://www.reteimprese.it/21787'}, {'falegname': 'http://www.reteimprese.it/17660'}, {'falegname': 'http://www.reteimprese.it/73515'}, {'falegname': 'http://www.reteimprese.it/71717'}, {'falegname': 'http://www.reteimprese.it/575'}, {'falegname': 'http://www.reteimprese.it/77983'}, {'falegname': 'http://www.reteimprese.it/14911'}, {'falegname': 'http://www.reteimprese.it/21856'}, {'falegname': 'http://www.reteimprese.it/27912'}, {'falegname': 'http://www.reteimprese.it/34825'}, {'falegname': 'http://www.reteimprese.it/45700'}, {'falegname': 'http://www.reteimprese.it/61594'}, {'falegname': 'http://www.reteimprese.it/6297'}, {'falegname': 'http://www.reteimprese.it/21858'}, {'falegname': 'http://www.reteimprese.it/38600'}, {'falegname': 'http://www.reteimprese.it/2935'}, {'falegname': 'http://www.reteimprese.it/18834'}, {'falegname': 'http://www.reteimprese.it/35325'}, {'falegname': 'http://www.reteimprese.it/8613'}, {'falegname': 'http://www.reteimprese.it/36011'}, {'falegname': 'http://www.reteimprese.it/4051'}, {'falegname': 'http://www.reteimprese.it/29062'}, {'falegname': 'http://www.reteimprese.it/11512'}, {'falegname': 'http://www.reteimprese.it/16801'}, {'falegname': 'http://www.reteimprese.it/11034'}, {'falegname': 'http://www.reteimprese.it/60403'}, {'falegname': 'http://www.reteimprese.it/23699'}, {'falegname': 'http://www.reteimprese.it/20106'}, {'falegname': 'http://www.reteimprese.it/18795'}, {'falegname': 'http://www.reteimprese.it/9498'}, {'falegname': 'http://www.reteimprese.it/69065'}, {'falegname': 'http://www.reteimprese.it/34527'}, {'falegname': 'http://www.reteimprese.it/50280'}, {'falegname': 'http://www.reteimprese.it/21906'}, {'falegname': 'http://www.reteimprese.it/45668'}, {'falegname': 'http://www.reteimprese.it/79358'}, {'falegname': 'http://www.reteimprese.it/42544'}, {'falegname': 'http://www.reteimprese.it/28054'}, {'falegname': 'http://www.reteimprese.it/77573'}, {'falegname': 'http://www.reteimprese.it/49345'}, {'falegname': 'http://www.reteimprese.it/22433'}, {'falegname': 'http://www.reteimprese.it/13365'}, {'falegname': 'http://www.reteimprese.it/40263'}, {'falegname': 'http://www.reteimprese.it/65265'}, {'falegname': 'http://www.reteimprese.it/5651'}, {'falegname': 'http://www.reteimprese.it/63412'}, {'falegname': 'http://www.reteimprese.it/35398'}, {'falegname': 'http://www.reteimprese.it/3160'}, {'falegname': 'http://www.reteimprese.it/17259'}, {'falegname': 'http://www.reteimprese.it/2823'}, {'falegname': 'http://www.reteimprese.it/3274'}, {'falegname': 'http://www.reteimprese.it/42419'}, {'falegname': 'http://www.reteimprese.it/29521'}, {'falegname': 'http://www.reteimprese.it/56014'}, {'falegname': 'http://www.reteimprese.it/18650'}, {'falegname': 'http://www.reteimprese.it/66725'}, {'falegname': 'http://www.reteimprese.it/1019'}, {'falegname': 'http://www.reteimprese.it/18421'}, {'falegname': 'http://www.reteimprese.it/11850'}, {'falegname': 'http://www.reteimprese.it/39899'}, {'falegname': 'http://www.reteimprese.it/25416'}, {'falegname': 'http://www.reteimprese.it/4664'}, {'falegname': 'http://www.reteimprese.it/39272'}, {'falegname': 'http://www.reteimprese.it/82268'}, {'falegname': 'http://www.reteimprese.it/17407'}, {'falegname': 'http://www.reteimprese.it/31350'}, {'falegname': 'http://www.reteimprese.it/805'}, {'falegname': 'http://www.reteimprese.it/40112'}, {'falegname': 'http://www.reteimprese.it/34331'}, {'falegname': 'http://www.reteimprese.it/3135'}, {'falegname': 'http://www.reteimprese.it/5732'}, {'falegname': 'http://www.reteimprese.it/17987'}, {'falegname': 'http://www.reteimprese.it/6872'}, {'falegname': 'http://www.reteimprese.it/1024'}, {'falegname': 'http://www.reteimprese.it/31032'}, {'falegname': 'http://www.reteimprese.it/95655'}, {'falegname': 'http://www.reteimprese.it/24874'}, {'falegname': 'http://www.reteimprese.it/91053'}, {'falegname': 'http://www.reteimprese.it/11927'}, {'falegname': 'http://www.reteimprese.it/7872'}, {'falegname': 'http://www.reteimprese.it/38812'}, {'falegname': 'http://www.reteimprese.it/22285'}, {'falegname': 'http://www.reteimprese.it/40558'}, {'falegname': 'http://www.reteimprese.it/3835'}, {'falegname': 'http://www.reteimprese.it/2489'}, {'falegname': 'http://www.reteimprese.it/24653'}, {'falegname': 'http://www.reteimprese.it/33658'}, {'falegname': 'http://www.reteimprese.it/8088'}, {'falegname': 'http://www.reteimprese.it/10423'}, {'falegname': 'http://www.reteimprese.it/21442'}, {'falegname': 'http://www.reteimprese.it/96224'}, {'falegname': 'http://www.reteimprese.it/3102'}, {'falegname': 'http://www.reteimprese.it/18007'}, {'falegname': 'http://www.reteimprese.it/15264'}, {'falegname': 'http://www.reteimprese.it/84901'}, {'falegname': 'http://www.reteimprese.it/18364'}, {'falegname': 'http://www.reteimprese.it/110216'}, {'falegname': 'http://www.reteimprese.it/31470'}, {'falegname': 'http://www.reteimprese.it/26892'}, {'falegname': 'http://www.reteimprese.it/44868'}, {'falegname': 'http://www.reteimprese.it/34971'}, {'falegname': 'http://www.reteimprese.it/50731'}, {'falegname': 'http://www.reteimprese.it/56243'}, {'falegname': 'http://www.reteimprese.it/22373'}, {'falegname': 'http://www.reteimprese.it/21593'}, {'falegname': 'http://www.reteimprese.it/5797'}, {'falegname': 'http://www.reteimprese.it/2179'}, {'falegname': 'http://www.reteimprese.it/5559'}, {'falegname': 'http://www.reteimprese.it/27667'}, {'falegname': 'http://www.reteimprese.it/15304'}, {'falegname': 'http://www.reteimprese.it/6842'}, {'falegname': 'http://www.reteimprese.it/6842'}, {'falegname': 'http://www.reteimprese.it/3840'}, {'falegname': 'http://www.reteimprese.it/2798'}, {'falegname': 'http://www.reteimprese.it/44234'}, {'falegname': 'http://www.reteimprese.it/84650'}, {'falegname': 'http://www.reteimprese.it/7124'}, {'falegname': 'http://www.reteimprese.it/17167'}, {'falegname': 'http://www.reteimprese.it/4286'}, {'falegname': 'http://www.reteimprese.it/16615'}, {'falegname': 'http://www.reteimprese.it/3947'}, {'falegname': 'http://www.reteimprese.it/38128'}, {'falegname': 'http://www.reteimprese.it/27343'}, {'falegname': 'http://www.reteimprese.it/54974'}, {'falegname': 'http://www.reteimprese.it/126881'}, {'falegname': 'http://www.reteimprese.it/18119'}, {'falegname': 'http://www.reteimprese.it/1011'}, {'falegname': 'http://www.reteimprese.it/27126'}, {'falegname': 'http://www.reteimprese.it/5593'}, {'falegname': 'http://www.reteimprese.it/76212'}, {'falegname': 'http://www.reteimprese.it/29680'}, {'falegname': 'http://www.reteimprese.it/14065'}, {'falegname': 'http://www.reteimprese.it/103028'}, {'falegname': 'http://www.reteimprese.it/89936'}, {'falegname': 'http://www.reteimprese.it/23950'}, {'falegname': 'http://www.reteimprese.it/14323'}, {'falegname': 'http://www.reteimprese.it/699'}, {'falegname': 'http://www.reteimprese.it/3026'}, {'falegname': 'http://www.reteimprese.it/9856'}, {'falegname': 'http://www.reteimprese.it/2608'}, {'falegname': 'http://www.reteimprese.it/6862'}, {'falegname': 'http://www.reteimprese.it/3010'}, {'falegname': 'http://www.reteimprese.it/7373'}, {'falegname': 'http://www.reteimprese.it/39656'}, {'falegname': 'http://www.reteimprese.it/33677'}, {'falegname': 'http://www.reteimprese.it/108319'}, {'falegname': 'http://www.reteimprese.it/12102'}, {'falegname': 'http://www.reteimprese.it/40975'}, {'falegname': 'http://www.reteimprese.it/46487'}, {'falegname': 'http://www.reteimprese.it/20104'}, {'falegname': 'http://www.reteimprese.it/23181'}, {'falegname': 'http://www.reteimprese.it/32459'}, {'falegname': 'http://www.reteimprese.it/59767'}, {'falegname': 'http://www.reteimprese.it/36651'}, {'falegname': 'http://www.reteimprese.it/8103'}, {'falegname': 'http://www.reteimprese.it/18624'}, {'falegname': 'http://www.reteimprese.it/34441'}, {'falegname': 'http://www.reteimprese.it/5922'}, {'falegname': 'http://www.reteimprese.it/69087'}, {'falegname': 'http://www.reteimprese.it/39282'}, {'falegname': 'http://www.reteimprese.it/6126'}, {'falegname': 'http://www.reteimprese.it/74451'}, {'falegname': 'http://www.reteimprese.it/9522'}, {'falegname': 'http://www.reteimprese.it/25560'}, {'falegname': 'http://www.reteimprese.it/15400'}, {'falegname': 'http://www.reteimprese.it/5749'}, {'falegname': 'http://www.reteimprese.it/25269'}, {'falegname': 'http://www.reteimprese.it/2118'}, {'falegname': 'http://www.reteimprese.it/22142'}, {'falegname': 'http://www.reteimprese.it/3873'}, {'falegname': 'http://www.reteimprese.it/14797'}, {'falegname': 'http://www.reteimprese.it/81898'}, {'falegname': 'http://www.reteimprese.it/76044'}, {'falegname': 'http://www.reteimprese.it/21167'}, {'falegname': 'http://www.reteimprese.it/20777'}, {'falegname': 'http://www.reteimprese.it/34762'}, {'falegname': 'http://www.reteimprese.it/17853'}, {'falegname': 'http://www.reteimprese.it/48368'}, {'falegname': 'http://www.reteimprese.it/97228'}, {'falegname': 'http://www.reteimprese.it/84664'}, {'falegname': 'http://www.reteimprese.it/86517'}, {'falegname': 'http://www.reteimprese.it/13983'}, {'falegname': 'http://www.reteimprese.it/9934'}, {'falegname': 'http://www.reteimprese.it/8896'}, {'falegname': 'http://www.reteimprese.it/30877'}, {'falegname': 'http://www.reteimprese.it/105294'}, {'falegname': 'http://www.reteimprese.it/20735'}, {'falegname': 'http://www.reteimprese.it/44671'}, {'falegname': 'http://www.reteimprese.it/19011'}, {'falegname': 'http://www.reteimprese.it/10331'}, {'falegname': 'http://www.reteimprese.it/8206'}, {'falegname': 'http://www.reteimprese.it/107245'}, {'falegname': 'http://www.reteimprese.it/61451'}, {'falegname': 'http://www.reteimprese.it/32094'}, {'falegname': 'http://www.reteimprese.it/103523'}, {'falegname': 'http://www.reteimprese.it/84039'}, {'falegname': 'http://www.reteimprese.it/21162'}, {'falegname': 'http://www.reteimprese.it/104040'}, {'falegname': 'http://www.reteimprese.it/99287'}, {'falegname': 'http://www.reteimprese.it/103470'}, {'falegname': 'http://www.reteimprese.it/19807'}, {'falegname': 'http://www.reteimprese.it/13770'}, {'falegname': 'http://www.reteimprese.it/12149'}, {'falegname': 'http://www.reteimprese.it/377'}, {'falegname': 'http://www.reteimprese.it/4749'}, {'falegname': 'http://www.reteimprese.it/31811'}, {'falegname': 'http://www.reteimprese.it/8775'}, {'falegname': 'http://www.reteimprese.it/7347'}, {'falegname': 'http://www.reteimprese.it/16193'}, {'falegname': 'http://www.reteimprese.it/10953'}, {'falegname': 'http://www.reteimprese.it/7969'}, {'falegname': 'http://www.reteimprese.it/101139'}, {'falegname': 'http://www.reteimprese.it/61774'}, {'falegname': 'http://www.reteimprese.it/13907'}, {'falegname': 'http://www.reteimprese.it/5434'}, {'falegname': 'http://www.reteimprese.it/124741'}, {'falegname': 'http://www.reteimprese.it/52516'}, {'falegname': 'http://www.reteimprese.it/113333'}, {'falegname': 'http://www.reteimprese.it/8634'}, {'falegname': 'http://www.reteimprese.it/47886'}, {'falegname': 'http://www.reteimprese.it/13042'}, {'falegname': 'http://www.reteimprese.it/17040'}, {'falegname': 'http://www.reteimprese.it/45741'}, {'falegname': 'http://www.reteimprese.it/43944'}, {'falegname': 'http://www.reteimprese.it/45028'}, {'falegname': 'http://www.reteimprese.it/62448'}, {'falegname': 'http://www.reteimprese.it/30820'}, {'falegname': 'http://www.reteimprese.it/120222'}, {'falegname': 'http://www.reteimprese.it/8101'}, {'falegname': 'http://www.reteimprese.it/84052'}, {'falegname': 'http://www.reteimprese.it/69069'}, {'falegname': 'http://www.reteimprese.it/106444'}, {'falegname': 'http://www.reteimprese.it/97482'}, {'falegname': 'http://www.reteimprese.it/34953'}, {'falegname': 'http://www.reteimprese.it/21857'}, {'falegname': 'http://www.reteimprese.it/30762'}, {'falegname': 'http://www.reteimprese.it/7568'}, {'falegname': 'http://www.reteimprese.it/35551'}, {'falegname': 'http://www.reteimprese.it/89622'}, {'falegname': 'http://www.reteimprese.it/32966'}, {'falegname': 'http://www.reteimprese.it/23972'}, {'falegname': 'http://www.reteimprese.it/23396'}, {'falegname': 'http://www.reteimprese.it/510'}, {'falegname': 'http://www.reteimprese.it/95987'}, {'falegname': 'http://www.reteimprese.it/43731'}, {'falegname': 'http://www.reteimprese.it/55755'}, {'falegname': 'http://www.reteimprese.it/73116'}, {'falegname': 'http://www.reteimprese.it/36897'}, {'falegname': 'http://www.reteimprese.it/31354'}, {'falegname': 'http://www.reteimprese.it/36290'}, {'falegname': 'http://www.reteimprese.it/107116'}, {'falegname': 'http://www.reteimprese.it/34190'}, {'falegname': 'http://www.reteimprese.it/6453'}, {'falegname': 'http://www.reteimprese.it/39069'}, {'falegname': 'http://www.reteimprese.it/106724'}, {'falegname': 'http://www.reteimprese.it/41609'}, {'falegname': 'http://www.reteimprese.it/65367'}, {'falegname': 'http://www.reteimprese.it/46350'}, {'falegname': 'http://www.reteimprese.it/51149'}, {'falegname': 'http://www.reteimprese.it/209'}, {'falegname': 'http://www.reteimprese.it/32954'}, {'falegname': 'http://www.reteimprese.it/2387'}, {'falegname': 'http://www.reteimprese.it/25219'}, {'falegname': 'http://www.reteimprese.it/22449'}, {'falegname': 'http://www.reteimprese.it/82241'}, {'falegname': 'http://www.reteimprese.it/65889'}, {'falegname': 'http://www.reteimprese.it/33891'}, {'falegname': 'http://www.reteimprese.it/26784'}, {'falegname': 'http://www.reteimprese.it/62123'}, {'falegname': 'http://www.reteimprese.it/33592'}, {'falegname': 'http://www.reteimprese.it/39760'}, {'falegname': 'http://www.reteimprese.it/125324'}, {'falegname': 'http://www.reteimprese.it/4065'}, {'falegname': 'http://www.reteimprese.it/119922'}, {'falegname': 'http://www.reteimprese.it/113048'}, {'falegname': 'http://www.reteimprese.it/124711'}, {'falegname': 'http://www.reteimprese.it/335'}, {'falegname': 'http://www.reteimprese.it/24775'}, {'falegname': 'http://www.reteimprese.it/62340'}, {'falegname': 'http://www.reteimprese.it/110928'}, {'falegname': 'http://www.reteimprese.it/113059'}, {'falegname': 'http://www.reteimprese.it/76690'}, {'falegname': 'http://www.reteimprese.it/114439'}, {'falegname': 'http://www.reteimprese.it/34268'}, {'falegname': 'http://www.reteimprese.it/116726'}, {'falegname': 'http://www.reteimprese.it/81142'}, {'falegname': 'http://www.reteimprese.it/8879'}, {'falegname': 'http://www.reteimprese.it/123690'}, {'falegname': 'http://www.reteimprese.it/103672'}, {'falegname': 'http://www.reteimprese.it/107061'}, {'falegname': 'http://www.reteimprese.it/117536'}, {'falegname': 'http://www.reteimprese.it/122501'}, {'falegname': 'http://www.reteimprese.it/115312'}, {'falegname': 'http://www.reteimprese.it/108899'}, {'falegname': 'http://www.reteimprese.it/112953'}, {'falegname': 'http://www.reteimprese.it/16862'}, {'falegname': 'http://www.reteimprese.it/600'}, {'falegname': 'http://www.reteimprese.it/1246'}, {'falegname': 'http://www.reteimprese.it/122709'}, {'falegname': 'http://www.reteimprese.it/115752'}]

#paging_urls = [{'falegname': 'http://www.reteimprese.it/429'}]

def process_update(page_url):
    import socket
    item_dict = {}
    current_page_url = page_url
    search_keyword = list(page_url.keys())[0]
    page_url = list(page_url.values())[0]
    print(page_url)
    
    #with tav.proxy.database.SqliteProxyDatabase(PROXY_DATABASE) as db:
    #    proxies = db.get_random()
    #    current_proxy = proxies[0]
    #    print(current_proxy)
    
    #current_proxy = random.choice(proxy_list)
    
    #proxy = urllib.request.ProxyHandler({'http': "http://"+str(current_proxy)})
    #opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    #urllib.request.install_opener(opener)
    
    #proxy_support = urllib.request.ProxyHandler({'http' : current_proxy})
    #opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler(debuglevel=1))
    #urllib.request.install_opener(opener)
    
    global page
    global content
    global title
    global adr1
    global adr2
    global adr3
    global adr4
    global phone
    global numbers1
    global numbers2
    global site_s
    global cat1_s
    global cat2_s
    global link_on_site_s
    global search_keyword
    global description
    page = ""

    
    try:
        request = urllib.request.Request(page_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
        #page = urllib.request.FancyURLopener({"http":current_proxy}).open(request)
        page = urllib.request.urlopen(request, timeout=5)
        if(page == ""):
            process_update(current_page_url)
        content = page.read()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            print(page_url)
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
        process_update(current_page_url)
    except timeout:
        print('socket timed out - URL %s', page_url)
        process_update(current_page_url)
    except socket.error as socketerror:
        print("Error: ", socketerror)
        process_update(current_page_url)
    except:
        process_update(current_page_url)    
    
    ssss = ''.join(map(chr, content.decode('iso-8859-1').encode('utf8')))
    soup = BeautifulSoup(ssss, "html.parser")
    
    title = soup.findAll('div',  {"class": "header_azienda_right"})
    title = str(title[0]).replace('<div class="header_azienda_right">','').replace('</div>','').replace('&amp;','&').strip()
    #print(title)
    
    description = soup.findAll('div',  {"class": "Mright"})
    description = normalize('NFKD', str(description[0])).encode('ASCII', 'ignore')
    soap2 = BeautifulSoup(description, "html.parser")
    description = ''.join(soap2.findAll(text=True)).replace('\n','')
    description = re.sub(r'^https?:\/\/.*[\r\n]*', '', description, flags=re.MULTILINE)
    #print(description)
    
    footer = soup.findAll('div',  {"class": "footer_info"})
    footer = str(footer[0])
    footer_list = footer.split('<br/>')
    
    footer_str = ''.join(footer_list)
    footer_str = normalize('NFKD', str(footer_str)).encode('ASCII', 'ignore')
    soap3 = BeautifulSoup(footer_str, "html.parser")
    footer_adr = ''.join(soap3.findAll(text=True)).strip().replace('\n\n','').split('	')
    
    footer = ''.join(soap3.findAll(text=True)).replace('\n','').replace('\t','').replace('   ','').strip()
    #print(footer)
    
    phone_s = re.search(re.escape('Telefono:')+'(.*?)'+re.escape('|Fax:'), footer).group(1)
    phone = phone_s.replace('|','').strip()
    #print(phone)
    
    numbers_s1 = re.search(re.escape('Partita IVA: ')+'(.*?)'+re.escape(' '), footer).group(1)
    numbers1 = numbers_s1.replace('|','').strip()
    #print(numbers1)
    
    numbers_s2 = re.search(re.escape('REA: ')+'(.*?)'+re.escape(' '), footer).group(1)
    numbers2 = numbers_s2.replace('|','').replace('Indirizzo','').strip()
    if(numbers2 == 'Indirizzo'):
        numbers2 = ''
    
    try:
        if(re.search('(\d+)', numbers2) == None):
            numbers2 = re.search(re.escape('REA:')+'(.*?)'+re.escape('Indirizzo'), footer).group(1)
            numbers2 = re.search('(\d+)', numbers2).group(1)
    except:
        numbers2 = numbers2
        
    if(re.search('Categoria', numbers2)  != None):
        numbers2 = ""
        
    #print(numbers2)
    
    try:
        cat1_s = re.search(re.escape('Categoria: ')+'(.*?)'+re.escape(';'), footer).group(1)
    except:
        cat1_s = ""
        print(page_url)
    #print(cat1_s)
    
    try:
        cat2_s = re.search(re.escape('GeoCategoria: ')+'(.*?)'+re.escape('Indirizzo Reteimprese:'), footer).group(1)
    except:
        cat2_s = ""
        print(page_url)
    #print(cat2_s)
    
    try:
        link_on_site_s = re.search(re.escape('Reteimprese: ')+'(.*?)$', footer).group(1)
    except:
        link_on_site_s = ""
        print(page_url)
    #print(link_on_site_s)
    
    try:
        address = re.search('^(.*?)'+re.escape('Telefono:'), footer).group(1)
        adr_list = address.split(',')
        #print(adr_list)
        if(len(adr_list) == 3):
            #adr1 = str(adr_list[0])+','+str(adr_list[1])
            adr1 = str(footer_adr[1].replace('\n','').strip()) + ' ' + str(footer_adr[2].replace(',','').strip())
            adr2 = re.search('(\d+)', adr_list[2]).group(1)
            adr_dd = adr_list[2].replace(adr2, '').split('-')
            adr3 = adr_dd[0].strip()
            adr4 = adr_dd[1].strip()
        #print(adr1)
        #print(adr2)
        #print(adr3)
        #print(adr4)
        if(title == ''):
            title = footer_adr[0]
    except:
        adr1 = ""
        adr2 = ""
        adr3 = ""
        adr4 = ""
        
    
    
    site_obj = re.search(re.escape('Indirizzo Ufficiale: ')+'(.*?)'+re.escape(' '), footer)
    if(site_obj):
        site_s = site_obj.group(1)
    else:
        site_s = ""
    #print(site_s)
    
    soup_image_src = soup.findAll('div',  {"class": "header_azienda_left"})
    

    try:
        image_src = soup_image_src[0].findAll('img')[0].attrs['src']
        imgname = urlparse(page_url).path.replace('/','')
        #print(imgname)
        img_data = urllib.request.urlopen(image_src, timeout=10)
        img_source = img_data.read()
        imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__))+'/img/', imgname+'.png')
        s = open(imgpath, "wb")
        s.write(img_source)
        s.close()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            image_src = ""
            print(page_url)
            process_update(current_page_url)
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
            image_src = ""
            print(page_url)
            process_update(current_page_url)
        sys.exit(1)
    except socket.error as socketerror:
        print("Error: ", socketerror)
        process_update(current_page_url)
    except timeout:
        print('socket timed out - URL %s', page_url)
        image_src = ""
        print(page_url)
        process_update(current_page_url)
    except:
        process_update(current_page_url)
    
    #print(image_src)
    
    DATABASE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'proxy.db')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("""INSERT INTO Reteimprese (NOME, INDIRIZZO, CAP, COMUNE, PROVINCIA, TELEONO, PIVA, REA, URL, CATEGORIA, GEOCATEGORIA, URL_RETE_IMPRESA, URL_SEARCH, DESCRIZIONE, IMAGE_URL, SITE_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (title, adr1, adr2, adr3, adr4, phone, numbers1, numbers2, site_s, cat1_s, cat2_s, link_on_site_s, search_keyword, description, image_src, imgname))
    connection.commit()
    connection.close()

for page_url in paging_urls: 
    process_update(page_url)

 
"""
workbook = xlsxwriter.Workbook(output_filename)
worksheet = workbook.add_worksheet()

header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})

main_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'valign': 'top', 'border': 1})
                                     
worksheet.set_column('A:A', 35)
worksheet.set_column('B:B', 24)
worksheet.set_column('C:C', 5)
worksheet.set_column('D:D', 8)
worksheet.set_column('E:E', 15)
worksheet.set_column('F:F', 10)
worksheet.set_column('G:G', 11)
worksheet.set_column('H:H', 7)
worksheet.set_column('I:I', 30)
worksheet.set_column('J:J', 32)
worksheet.set_column('K:K', 37)
worksheet.set_column('L:L', 36)
worksheet.set_column('M:M', 11)
worksheet.set_column('N:N', 35)
worksheet.set_column('O:O', 19)

workbook.add_format({'text_wrap': 1, 'valign': 'top'})

worksheet.write(0, 0, 'NOME', header_format)
worksheet.write(0, 1, 'INDIRIZZO', header_format)
worksheet.write(0, 2, 'CAP', header_format)
worksheet.write(0, 3, 'COMUNE', header_format)
worksheet.write(0, 4, 'PROVINCIA', header_format)
worksheet.write(0, 5, 'TELEONO', header_format)
worksheet.write(0, 6, 'PIVA', header_format)
worksheet.write(0, 7, 'REA', header_format)
worksheet.write(0, 8, 'URL', header_format)
worksheet.write(0, 9, 'CATEGORIA', header_format)
worksheet.write(0, 10, 'GEOCATEGORIA', header_format)
worksheet.write(0, 11, 'URL RETE IMPRESA', header_format)
worksheet.write(0, 12, 'URL SEARCH', header_format)
worksheet.write(0, 13, 'DESCRIZIONE', header_format)
worksheet.write(0, 14, 'IMAGE', header_format)

row = 1
col = 0

for page_url in paging_urls:
    
    item_dict = {}
    search_keyword = list(page_url.keys())[0]
    page_url = list(page_url.values())[0]
    print(page_url)
    
    with tav.proxy.database.SqliteProxyDatabase(PROXY_DATABASE) as db:
        proxies = db.get_random()
        current_proxy = proxies[0]
        print(current_proxy)
    
    #current_proxy = random.choice(proxy_list)
    
    proxy = urllib.request.ProxyHandler({'http': "http://"+str(current_proxy)})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    
    #proxy_support = urllib.request.ProxyHandler({'http' : current_proxy})
    #opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler(debuglevel=1))
    #urllib.request.install_opener(opener)
    
    try:
        request = urllib.request.Request(page_url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', 'X-Compress': 'null'})
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
    ssss = ''.join(map(chr, content.decode('iso-8859-1').encode('utf8')))
    soup = BeautifulSoup(ssss, "html.parser")
    
    title = soup.findAll('div',  {"class": "header_azienda_right"})
    title = str(title[0]).replace('<div class="header_azienda_right">','').replace('</div>','').replace('&amp;','&').strip()
    #print(title)
    
    description = soup.findAll('div',  {"class": "Mright"})
    description = normalize('NFKD', str(description[0])).encode('ASCII', 'ignore')
    soap2 = BeautifulSoup(description, "html.parser")
    description = ''.join(soap2.findAll(text=True)).replace('\n','')
    description = re.sub(r'^https?:\/\/.*[\r\n]*', '', description, flags=re.MULTILINE)
    #print(description)
    
    footer = soup.findAll('div',  {"class": "footer_info"})
    footer = str(footer[0])
    footer_list = footer.split('<br/>')
    
    footer_str = ''.join(footer_list)
    footer_str = normalize('NFKD', str(footer_str)).encode('ASCII', 'ignore')
    soap3 = BeautifulSoup(footer_str, "html.parser")
    footer_adr = ''.join(soap3.findAll(text=True)).strip().replace('\n\n','').split('	')
    
    footer = ''.join(soap3.findAll(text=True)).replace('\n','').replace('\t','').replace('   ','').strip()
    #print(footer)
    
    phone_s = re.search(re.escape('Telefono:')+'(.*?)'+re.escape('|Fax:'), footer).group(1)
    phone = phone_s.replace('|','').strip()
    #print(phone)
    
    numbers_s1 = re.search(re.escape('Partita IVA: ')+'(.*?)'+re.escape(' '), footer).group(1)
    numbers1 = numbers_s1.replace('|','').strip()
    #print(numbers1)
    
    numbers_s2 = re.search(re.escape('REA: ')+'(.*?)'+re.escape(' '), footer).group(1)
    numbers2 = numbers_s2.replace('|','').replace('Indirizzo','').strip()
    if(numbers2 == 'Indirizzo'):
        numbers2 = ''
    
    try:
        if(re.search('(\d+)', numbers2) == None):
            numbers2 = re.search(re.escape('REA:')+'(.*?)'+re.escape('Indirizzo'), footer).group(1)
            numbers2 = re.search('(\d+)', numbers2).group(1)
    except:
        numbers2 = numbers2
        
    if(re.search('Categoria', numbers2)  != None):
        numbers2 = ""
        
    #print(numbers2)
    
    try:
        cat1_s = re.search(re.escape('Categoria: ')+'(.*?)'+re.escape(';'), footer).group(1)
    except:
        cat1_s = ""
        print(page_url)
    #print(cat1_s)
    
    try:
        cat2_s = re.search(re.escape('GeoCategoria: ')+'(.*?)'+re.escape('Indirizzo Reteimprese:'), footer).group(1)
    except:
        cat2_s = ""
        print(page_url)
    #print(cat2_s)
    
    try:
        link_on_site_s = re.search(re.escape('Reteimprese: ')+'(.*?)$', footer).group(1)
    except:
        link_on_site_s = ""
        print(page_url)
    #print(link_on_site_s)
    
    try:
        address = re.search('^(.*?)'+re.escape('Telefono:'), footer).group(1)
        adr_list = address.split(',')
        #print(adr_list)
        if(len(adr_list) == 3):
            #adr1 = str(adr_list[0])+','+str(adr_list[1])
            adr1 = str(footer_adr[1].replace('\n','').strip()) + ' ' + str(footer_adr[2].replace(',','').strip())
            adr2 = re.search('(\d+)', adr_list[2]).group(1)
            adr_dd = adr_list[2].replace(adr2, '').split('-')
            adr3 = adr_dd[0].strip()
            adr4 = adr_dd[1].strip()
        #print(adr1)
        #print(adr2)
        #print(adr3)
        #print(adr4)
        if(title == ''):
            title = footer_adr[0]
    except:
        adr1 = ""
        adr2 = ""
        adr3 = ""
        adr4 = ""
        
    
    
    site_obj = re.search(re.escape('Indirizzo Ufficiale: ')+'(.*?)'+re.escape(' '), footer)
    if(site_obj):
        site_s = site_obj.group(1)
    else:
        site_s = ""
    #print(site_s)
    
    soup_image_src = soup.findAll('div',  {"class": "header_azienda_left"})
    

    try:
        image_src = soup_image_src[0].findAll('img')[0].attrs['src']
        imgname = urlparse(page_url).path.replace('/','')
        #print(imgname)
        img_data = urllib.request.urlopen(image_src, timeout=10)
        img_source = img_data.read()
        imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__))+'/img/', imgname+'.png')
        s = open(imgpath, "wb")
        s.write(img_source)
        s.close()
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            image_src = ""
            print(page_url)
            continue
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
            image_src = ""
            print(page_url)
            continue
        sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', page_url)
        image_src = ""
        print(page_url)
        continue

    
    #print(image_src)
    
    worksheet.set_row(row, 80)
    worksheet.write(row, 0, title, main_format)
    worksheet.write(row, 1, adr1, main_format)
    worksheet.write(row, 2, adr2, main_format)
    worksheet.write(row, 3, adr3, main_format)
    worksheet.write(row, 4, adr4, main_format)
    worksheet.write(row, 5, phone, main_format)
    worksheet.write(row, 6, numbers1, main_format)
    worksheet.write(row, 7, numbers2, main_format)
    worksheet.write(row, 8, site_s, main_format)
    worksheet.write(row, 9, cat1_s, main_format)
    worksheet.write(row, 10, cat2_s, main_format)
    worksheet.write(row, 11, link_on_site_s, main_format)
    worksheet.write(row, 12, search_keyword, main_format)
    worksheet.write(row, 13, description, main_format)
    
    if(image_src != ''):
        worksheet.write(row, 14, "", main_format)
        worksheet.insert_image(row, 14, imgpath, {'positioning': 2, 'x_offset': 15, 'y_offset': 2})
    else:
        worksheet.write(row, 14, image_src, main_format)
    row += 1
    
workbook.close()
"""
