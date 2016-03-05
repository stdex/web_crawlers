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
        
        output = csv.writer(open(self.output_file, 'w', newline=''),  delimiter=';')
        
        current_link = self.main_url + '/models?brand_id=5'
        content = self.request_to_page(current_link)
        soup = BeautifulSoup(content, "lxml")
        
        items_all = soup.findAll('div',  {"class": "item"})
        #items = items_all[:-1]
        items = items_all[:-16]
        print(len(items))
        
        for itm in items:
            model_url = self.main_url + itm.find('a').attrs['href']
            #print(model_url)
            content_model = self.request_to_page(model_url)
            soup_model = BeautifulSoup(content_model, "lxml")
            
            brend_name = soup_model.find('div',  {"id": "breadcrumbs"}).find('span',  {"class": "text"}).getText()
            #print(model_name)
            
            vehicle_table = soup_model.find('table',  {"class": "table-mod"})
            trs_all = vehicle_table.findAll('tr',  {"class": ""})
            #trs = trs_all[1:-1]
            trs = trs_all[1:-4]
            #print(trs)
            for tr in trs:
                tds = tr.findAll('td')
                if len(tds) == 6:
                    litr = tds[0].getText().replace(' л.','')
                    model_name = tds[1].getText()
                    years_str = tds[2].getText().replace(' ','')
                    years_pieces = years_str.split('/')
                    start_year = years_pieces[0].strip()
                    end_year = ((years_pieces[1].split('—'))[1]).strip()
                    years = start_year + "-" + end_year
                    vehicle_type = ""
                    if vehicle_type == "":
                        vehicle_type = "бензин" 
                    kpp = ""
                    if kpp == "":
                        kpp = "МКПП/АКПП"
                    privod = ""
                    if privod == "":
                        privod = "Передний"
                    genarts_link = self.main_url + tds[1].find('a').attrs['href']
                elif len(tds) == 5:
                    litr = litr
                    model_name = tds[0].getText()
                    years_str = tds[1].getText().replace(' ','')
                    years_pieces = years_str.split('/')
                    start_year = years_pieces[0].strip()
                    end_year = ((years_pieces[1].split('—'))[1]).strip()
                    years = start_year + "-" + end_year
                    vehicle_type = ""
                    if vehicle_type == "":
                        vehicle_type = "бензин" 
                    kpp = ""
                    if kpp == "":
                        kpp = "МКПП/АКПП"
                    privod = ""
                    if privod == "":
                        privod = "Передний"
                    genarts_link = self.main_url + tds[0].find('a').attrs['href']
                
                content_genarts = self.request_to_page(genarts_link)
                soup_genarts = BeautifulSoup(content_genarts, "lxml")
                all_genarts = (soup_genarts.find('div', {"class": "set-list"}).findAll('div',  {"class": "item"}))[1:]
                for genar in all_genarts:
                    name_0 = "Комплект"
                    name_1 = genar.find('a').getText()
                    name_2 = ((genar.find('p').getText().split('или'))[0]).replace(' ', '')
                    genar_name = name_0 + " " + name_1 + " (" + name_2 + ")"
                    genar_url = self.main_url + genar.find('a').attrs['href']
                    content_genar = self.request_to_page(genar_url)
                    soup_genar = BeautifulSoup(content_genar, "lxml")
                    all_genar = (soup_genar.find('div', {"class": "contains-over over1"}).findAll('p'))
                    for gnr in all_genar:
                        split_name_gnr = gnr.getText().split(brend_name.upper())
                        name_gnr1 = split_name_gnr[0].strip()
                        name_gnr2 = split_name_gnr[1].strip()
                        name_gnr = name_gnr1 + " " + name_gnr2
                        print(name_gnr1)
                        """
                        li_cnts = soup_genar.find('div', {"class": "set-inner"}).findAll('li')
                        for li in li_cnts:
                            l = li.getText()
                            if name_gnr1 == 'Масло моторное' and l.find('Замена моторного масла'):
                                cnt_need_parts = name_gnr2.split(' ')
                                for cntnd in cnt_need_parts:
                                    if cntnd.isdigit():
                                        cnt_need = cntnd
                                cnt_to = l.replace('Замена моторного масла (объем ','').replace(' л.)','')
                        print(name_gnr, cnt_need, cnt_to)
                        """
                        output.writerow([genar_name, years, litr + " " + vehicle_type, kpp, privod, name_gnr, brend_name.upper(), '', '1'])
                #print(model_name, years, litr + " " + vehicle_type, kpp, privod, genarts_link)
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://toexpert.ru', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
