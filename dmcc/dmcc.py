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
import os.path
from http.cookiejar import CookieJar
from time import sleep

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

        for inx in range(1,886):
            item_url = self.main_url + "&page_num="+str(inx)
            print(item_url)
            content = self.request_to_page(item_url)
            response = json.loads(content.decode('utf-8'))
            objects = response['sObjects']
            for obj in objects:
                if('License_Address__c' in obj.keys()):
                    adr = obj['License_Address__c'].replace('<br>',' ').replace('&amp;','&')
                else:
                    adr = ""
                if('Name' in obj['Account__r'].keys()):
                    name = obj['Account__r']['Name']
                else:
                    name = ""
                if('Phone_BD__c' in obj['Account__r'].keys()):
                    phone = obj['Account__r']['Phone_BD__c']
                else:
                    phone = ""
                if('Company_Official_Email_Address__c' in obj['Account__r'].keys()):
                    mail = obj['Account__r']['Company_Official_Email_Address__c']
                else:
                    mail = ""
                if('Company_Website_Address__c' in obj['Account__r'].keys()):
                    website = obj['Account__r']['Company_Website_Address__c']
                else:
                    website = ""
                output.writerow([name, adr, phone, mail, website])
            #print(response)
        
if __name__ == '__main__':
    settings = { 'main_url': 'https://dmcc.secure.force.com/services/apexrest/DMCC_BusinessDirectory_API_1/get/?authToken=1455459029231&query_type=activities', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
