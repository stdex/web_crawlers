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
search_keywords = ['fabbro']
output_filename = 'test_tbl.xlsx'

all_items = []
paging_urls = []

""""""
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

""""""
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



#paging_urls = [{'restauratore': 'http://www.reteimprese.it/84650'}, {'restauratore': 'http://www.reteimprese.it/7124'}, {'restauratore': 'http://www.reteimprese.it/17167'}, {'restauratore': 'http://www.reteimprese.it/4286'}, {'restauratore': 'http://www.reteimprese.it/16615'}, {'restauratore': 'http://www.reteimprese.it/3947'}, {'restauratore': 'http://www.reteimprese.it/38128'}, {'restauratore': 'http://www.reteimprese.it/27343'}, {'restauratore': 'http://www.reteimprese.it/54974'}, {'restauratore': 'http://www.reteimprese.it/126881'}, {'restauratore': 'http://www.reteimprese.it/18119'}, {'restauratore': 'http://www.reteimprese.it/1011'}, {'restauratore': 'http://www.reteimprese.it/27126'}, {'restauratore': 'http://www.reteimprese.it/5593'}, {'restauratore': 'http://www.reteimprese.it/76212'}, {'restauratore': 'http://www.reteimprese.it/29680'}, {'restauratore': 'http://www.reteimprese.it/14065'}, {'restauratore': 'http://www.reteimprese.it/103028'}, {'restauratore': 'http://www.reteimprese.it/89936'}, {'restauratore': 'http://www.reteimprese.it/23950'}, {'restauratore': 'http://www.reteimprese.it/14323'}, {'restauratore': 'http://www.reteimprese.it/699'}, {'restauratore': 'http://www.reteimprese.it/3026'}, {'restauratore': 'http://www.reteimprese.it/9856'}, {'restauratore': 'http://www.reteimprese.it/2608'}, {'restauratore': 'http://www.reteimprese.it/6862'}, {'restauratore': 'http://www.reteimprese.it/3010'}, {'restauratore': 'http://www.reteimprese.it/7373'}, {'restauratore': 'http://www.reteimprese.it/39656'}, {'restauratore': 'http://www.reteimprese.it/33677'}, {'restauratore': 'http://www.reteimprese.it/108319'}, {'restauratore': 'http://www.reteimprese.it/12102'}, {'restauratore': 'http://www.reteimprese.it/40975'}, {'restauratore': 'http://www.reteimprese.it/46487'}, {'restauratore': 'http://www.reteimprese.it/20104'}, {'restauratore': 'http://www.reteimprese.it/23181'}, {'restauratore': 'http://www.reteimprese.it/32459'}, {'restauratore': 'http://www.reteimprese.it/59767'}, {'restauratore': 'http://www.reteimprese.it/36651'}, {'restauratore': 'http://www.reteimprese.it/8103'}, {'restauratore': 'http://www.reteimprese.it/18624'}, {'restauratore': 'http://www.reteimprese.it/34441'}, {'restauratore': 'http://www.reteimprese.it/5922'}, {'restauratore': 'http://www.reteimprese.it/69087'}, {'restauratore': 'http://www.reteimprese.it/39282'}, {'restauratore': 'http://www.reteimprese.it/6126'}, {'restauratore': 'http://www.reteimprese.it/74451'}, {'restauratore': 'http://www.reteimprese.it/9522'}, {'restauratore': 'http://www.reteimprese.it/25560'}, {'restauratore': 'http://www.reteimprese.it/15400'}, {'restauratore': 'http://www.reteimprese.it/5749'}, {'restauratore': 'http://www.reteimprese.it/25269'}, {'restauratore': 'http://www.reteimprese.it/2118'}, {'restauratore': 'http://www.reteimprese.it/22142'}, {'restauratore': 'http://www.reteimprese.it/3873'}, {'restauratore': 'http://www.reteimprese.it/14797'}, {'restauratore': 'http://www.reteimprese.it/81898'}, {'restauratore': 'http://www.reteimprese.it/76044'}, {'restauratore': 'http://www.reteimprese.it/21167'}, {'restauratore': 'http://www.reteimprese.it/20777'}, {'restauratore': 'http://www.reteimprese.it/34762'}, {'restauratore': 'http://www.reteimprese.it/17853'}, {'restauratore': 'http://www.reteimprese.it/48368'}, {'restauratore': 'http://www.reteimprese.it/97228'}, {'restauratore': 'http://www.reteimprese.it/84664'}, {'restauratore': 'http://www.reteimprese.it/86517'}, {'restauratore': 'http://www.reteimprese.it/13983'}, {'restauratore': 'http://www.reteimprese.it/9934'}, {'restauratore': 'http://www.reteimprese.it/8896'}, {'restauratore': 'http://www.reteimprese.it/30877'}, {'restauratore': 'http://www.reteimprese.it/105294'}, {'restauratore': 'http://www.reteimprese.it/20735'}, {'restauratore': 'http://www.reteimprese.it/44671'}, {'restauratore': 'http://www.reteimprese.it/19011'}, {'restauratore': 'http://www.reteimprese.it/10331'}, {'restauratore': 'http://www.reteimprese.it/8206'}, {'restauratore': 'http://www.reteimprese.it/107245'}, {'restauratore': 'http://www.reteimprese.it/61451'}, {'restauratore': 'http://www.reteimprese.it/32094'}, {'restauratore': 'http://www.reteimprese.it/103523'}, {'restauratore': 'http://www.reteimprese.it/84039'}, {'restauratore': 'http://www.reteimprese.it/21162'}, {'restauratore': 'http://www.reteimprese.it/104040'}, {'restauratore': 'http://www.reteimprese.it/99287'}, {'restauratore': 'http://www.reteimprese.it/103470'}, {'restauratore': 'http://www.reteimprese.it/19807'}, {'restauratore': 'http://www.reteimprese.it/13770'}, {'restauratore': 'http://www.reteimprese.it/12149'}, {'restauratore': 'http://www.reteimprese.it/377'}, {'restauratore': 'http://www.reteimprese.it/4749'}, {'restauratore': 'http://www.reteimprese.it/31811'}, {'restauratore': 'http://www.reteimprese.it/8775'}, {'restauratore': 'http://www.reteimprese.it/7347'}, {'restauratore': 'http://www.reteimprese.it/16193'}, {'restauratore': 'http://www.reteimprese.it/10953'}, {'restauratore': 'http://www.reteimprese.it/7969'}, {'restauratore': 'http://www.reteimprese.it/101139'}, {'restauratore': 'http://www.reteimprese.it/61774'}, {'restauratore': 'http://www.reteimprese.it/13907'}, {'restauratore': 'http://www.reteimprese.it/5434'}, {'restauratore': 'http://www.reteimprese.it/124741'}, {'restauratore': 'http://www.reteimprese.it/52516'}, {'restauratore': 'http://www.reteimprese.it/113333'}, {'restauratore': 'http://www.reteimprese.it/8634'}, {'restauratore': 'http://www.reteimprese.it/47886'}, {'restauratore': 'http://www.reteimprese.it/13042'}, {'restauratore': 'http://www.reteimprese.it/17040'}, {'restauratore': 'http://www.reteimprese.it/45741'}, {'restauratore': 'http://www.reteimprese.it/43944'}, {'restauratore': 'http://www.reteimprese.it/45028'}, {'restauratore': 'http://www.reteimprese.it/62448'}, {'restauratore': 'http://www.reteimprese.it/30820'}, {'restauratore': 'http://www.reteimprese.it/120222'}, {'restauratore': 'http://www.reteimprese.it/8101'}, {'restauratore': 'http://www.reteimprese.it/84052'}, {'restauratore': 'http://www.reteimprese.it/69069'}, {'restauratore': 'http://www.reteimprese.it/106444'}, {'restauratore': 'http://www.reteimprese.it/97482'}, {'restauratore': 'http://www.reteimprese.it/34953'}, {'restauratore': 'http://www.reteimprese.it/21857'}, {'restauratore': 'http://www.reteimprese.it/30762'}, {'restauratore': 'http://www.reteimprese.it/7568'}, {'restauratore': 'http://www.reteimprese.it/35551'}, {'restauratore': 'http://www.reteimprese.it/89622'}, {'restauratore': 'http://www.reteimprese.it/32966'}, {'restauratore': 'http://www.reteimprese.it/23972'}, {'restauratore': 'http://www.reteimprese.it/23396'}, {'restauratore': 'http://www.reteimprese.it/510'}, {'restauratore': 'http://www.reteimprese.it/95987'}, {'restauratore': 'http://www.reteimprese.it/43731'}, {'restauratore': 'http://www.reteimprese.it/55755'}, {'restauratore': 'http://www.reteimprese.it/73116'}, {'restauratore': 'http://www.reteimprese.it/36897'}, {'restauratore': 'http://www.reteimprese.it/31354'}, {'restauratore': 'http://www.reteimprese.it/36290'}, {'restauratore': 'http://www.reteimprese.it/107116'}, {'restauratore': 'http://www.reteimprese.it/34190'}, {'restauratore': 'http://www.reteimprese.it/6453'}, {'restauratore': 'http://www.reteimprese.it/39069'}, {'restauratore': 'http://www.reteimprese.it/106724'}, {'restauratore': 'http://www.reteimprese.it/41609'}, {'restauratore': 'http://www.reteimprese.it/65367'}, {'restauratore': 'http://www.reteimprese.it/46350'}, {'restauratore': 'http://www.reteimprese.it/51149'}, {'restauratore': 'http://www.reteimprese.it/209'}, {'restauratore': 'http://www.reteimprese.it/32954'}, {'restauratore': 'http://www.reteimprese.it/2387'}, {'restauratore': 'http://www.reteimprese.it/25219'}, {'restauratore': 'http://www.reteimprese.it/22449'}, {'restauratore': 'http://www.reteimprese.it/82241'}, {'restauratore': 'http://www.reteimprese.it/65889'}, {'restauratore': 'http://www.reteimprese.it/33891'}, {'restauratore': 'http://www.reteimprese.it/26784'}, {'restauratore': 'http://www.reteimprese.it/62123'}, {'restauratore': 'http://www.reteimprese.it/33592'}, {'restauratore': 'http://www.reteimprese.it/39760'}, {'restauratore': 'http://www.reteimprese.it/125324'}, {'restauratore': 'http://www.reteimprese.it/4065'}, {'restauratore': 'http://www.reteimprese.it/119922'}, {'restauratore': 'http://www.reteimprese.it/113048'}, {'restauratore': 'http://www.reteimprese.it/124711'}, {'restauratore': 'http://www.reteimprese.it/335'}, {'restauratore': 'http://www.reteimprese.it/24775'}, {'restauratore': 'http://www.reteimprese.it/62340'}, {'restauratore': 'http://www.reteimprese.it/110928'}, {'restauratore': 'http://www.reteimprese.it/113059'}, {'restauratore': 'http://www.reteimprese.it/76690'}, {'restauratore': 'http://www.reteimprese.it/114439'}, {'restauratore': 'http://www.reteimprese.it/34268'}, {'restauratore': 'http://www.reteimprese.it/116726'}, {'restauratore': 'http://www.reteimprese.it/81142'}, {'restauratore': 'http://www.reteimprese.it/8879'}, {'restauratore': 'http://www.reteimprese.it/123690'}, {'restauratore': 'http://www.reteimprese.it/103672'}, {'restauratore': 'http://www.reteimprese.it/107061'}, {'restauratore': 'http://www.reteimprese.it/117536'}, {'restauratore': 'http://www.reteimprese.it/122501'}, {'restauratore': 'http://www.reteimprese.it/115312'}, {'restauratore': 'http://www.reteimprese.it/108899'}, {'restauratore': 'http://www.reteimprese.it/112953'}, {'restauratore': 'http://www.reteimprese.it/16862'}, {'restauratore': 'http://www.reteimprese.it/600'}, {'restauratore': 'http://www.reteimprese.it/1246'}, {'restauratore': 'http://www.reteimprese.it/122709'}, {'restauratore': 'http://www.reteimprese.it/115752'}]

#paging_urls = [{'falegname': 'http://www.reteimprese.it/90092'}]


for page_url in paging_urls:
    
    item_dict = {}
    search_keyword = list(page_url.keys())[0]
    page_url = list(page_url.values())[0]
    print(page_url)
    
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
        #sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', page_url)
        image_src = ""
        print(page_url)
        continue
    except:
        imgname = urlparse(page_url).path.replace('/','')
        image_src = ""
    
        
    DATABASE = os.path.join(os.path.abspath(os.path.split(__file__)[0]), 'proxy.db')

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    
    cursor.execute("""INSERT INTO Reteimprese (NOME, INDIRIZZO, CAP, COMUNE, PROVINCIA, TELEONO, PIVA, REA, URL, CATEGORIA, GEOCATEGORIA, URL_RETE_IMPRESA, URL_SEARCH, DESCRIZIONE, IMAGE_URL, SITE_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (title, adr1, adr2, adr3, adr4, phone, numbers1, numbers2, site_s, cat1_s, cat2_s, link_on_site_s, search_keyword, description, image_src, imgname))
    connection.commit()
    connection.close()