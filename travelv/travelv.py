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

    def do_login(self, url, login, password):
        try:
            
            current_url = url
            cookie_jar = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
            urllib.request.install_opener(opener)
            
            request = urllib.request.Request(url)

            params = urllib.parse.urlencode({
                'meneger_user': login,
                'meneger_pass':  password,
                'url':  '',
            })

            request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
            request.add_header("Accept-Language","ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4")
            request.add_header("Cache-Control","max-age=0")
            request.add_header("Accept-Encoding","gzip, deflate")
            request.add_header("Connection","keep-alive")
            request.add_header("Content-Length","79")
            request.add_header("Content-Type","application/x-www-form-urlencoded")
            request.add_header("Host","www.travelv.ru")
            request.add_header("Origin","http://www.travelv.ru")
            request.add_header("Referer","http://www.travelv.ru/meneger/")
            request.add_header("User-Agent","Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36")
            request.add_header("X-Compress","null")
            
            
            data = params.encode('utf-8')
            
            page = opener.open(request, data)
            content = page.read()
            
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

    def start_process(self):
        """
        self.request_to_page(self.main_url)
        content = self.request_to_page(self.main_url+'/login')
        
        soup = BeautifulSoup(content, "lxml")
        try:
            csrf = soup.find('input',  {"name": "_csrf"}).attrs['value']
            print(csrf)
        except:
            csrf = ''
        """
        """
        login = 'ufa2'
        password = 'qYuEmZwifG'
        login = self.do_login(self.main_url+'/vhod.php', login, password)
        content = self.request_to_page(self.main_url+'/zayavki_podbor.php')
        uprint(login)
        """
        output = csv.writer(open(self.output_file, 'w', newline=''),  delimiter=';')
        result = []
        cur_path = os.path.dirname(os.path.abspath(__file__))
        for file_inx in range(1,66):
            print("src_"+str(file_inx)+".txt")
            with open (cur_path+"/html/src_"+str(file_inx)+".txt", "r") as myfile:
                content = myfile.read().replace('\n', '')
                soup = BeautifulSoup(content, "lxml")
                {"class": "div_zayavki"}
                div_s = soup.findAll('div',  {"class": re.compile('^div_zayavki')})
                for div in div_s:
                    obj = {'name': '', 'phone': '', 'email': '', 'country': '', 'adalt_cnt': '', 'children_cnt': '', 'price': ''}
                    name_r = re.search(re.escape('Имя клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(name_r != None):
                        name = name_r.group(1)
                    else:
                        name_s = div.find('font',  {"style": "font-size:18px; color:#008000"})
                        if(name_s != None):
                            name = name_s.text
                        else:
                            name = ""

                    phone_r = re.search(re.escape('Телефон клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(phone_r != None):
                        phone = phone_r.group(1)
                    else:
                        phone_s = div.find('input',  {"class": "telefon"})
                        if(phone_s != None):
                            phone = phone_s.attrs['value']
                        else:
                            phone = ""
                    
                    email_r = re.search(re.escape('E-mail клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(email_r != None):
                        email = email_r.group(1)
                    else:
                        email = ""
                        
                    country_r = re.search(re.escape('в страну <b>"')+'(.*?)'+re.escape('"</b>'), str(div))
                    if(country_r != None):
                        country = country_r.group(1)
                    else:
                        country = ""
                    
                    adalt_cnt_r = re.search(re.escape('Взрослых едет <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(adalt_cnt_r != None):
                        adalt_cnt = adalt_cnt_r.group(1)
                    else:
                        adalt_cnt = ""
                    
                    children_cnt_r = re.search(re.escape('Детей едет <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(children_cnt_r != None):
                        children_cnt = children_cnt_r.group(1)
                    else:
                        children_cnt = ""
                    
                    price_r = re.search(re.escape('Желаемая цена тура от <b>0</b> до <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(price_r != None):
                        price = price_r.group(1)
                    else:
                        price = ""
                        
                    obj['name'] = name
                    obj['phone'] = phone
                    obj['email'] = email
                    obj['country'] = country
                    obj['adalt_cnt'] = adalt_cnt
                    obj['children_cnt'] = children_cnt
                    obj['price'] = price
                    result.append(obj)
                
                
                """
                
                div_n = soup.findAll('div',  {"class": "div_zayavki_no"})
                for div in div_n:
                    obj = {'name': '', 'phone': '', 'email': '', 'country': '', 'adalt_cnt': '', 'children_cnt': '', 'price': ''}
                    name_r = re.search(re.escape('Имя клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(name_r != None):
                        name = name_r.group(1)
                    else:
                        name_s = div.find('font',  {"style": "font-size:18px; color:#008000"})
                        if(name_s != None):
                            name = name_s.text
                        else:
                            name = ""

                    phone_r = re.search(re.escape('Телефон клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(phone_r != None):
                        phone = phone_r.group(1)
                    else:
                        phone_s = div.find('input',  {"class": "telefon"})
                        if(phone_s != None):
                            phone = phone_s.attrs['value']
                        else:
                            phone = ""
                    
                    email_r = re.search(re.escape('E-mail клиента: <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(email_r != None):
                        email = email_r.group(1)
                    else:
                        email = ""
                        
                    country_r = re.search(re.escape('в страну <b>"')+'(.*?)'+re.escape('"</b>'), str(div))
                    if(country_r != None):
                        country = country_r.group(1)
                    else:
                        country = ""
                    
                    adalt_cnt_r = re.search(re.escape('Взрослых едет <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(adalt_cnt_r != None):
                        adalt_cnt = adalt_cnt_r.group(1)
                    else:
                        adalt_cnt = ""
                    
                    children_cnt_r = re.search(re.escape('Детей едет <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(children_cnt_r != None):
                        children_cnt = children_cnt_r.group(1)
                    else:
                        children_cnt = ""
                    
                    price_r = re.search(re.escape('Желаемая цена тура от <b>0</b> до <b>')+'(.*?)'+re.escape('</b>'), str(div))
                    if(price_r != None):
                        price = price_r.group(1)
                    else:
                        price = ""
                        
                    obj['name'] = name
                    obj['phone'] = phone
                    obj['email'] = email
                    obj['country'] = country
                    obj['adalt_cnt'] = adalt_cnt
                    obj['children_cnt'] = children_cnt
                    obj['price'] = price
                    result.append(obj)
                """    
                    
                print(len(result))
        
        for obj in result:
            output.writerow([obj.get('name'), obj.get('phone'), obj.get('email'), obj.get('country'), obj.get('adalt_cnt'), obj.get('children_cnt'), obj.get('price')])
                    
                
        
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.travelv.ru/meneger', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
