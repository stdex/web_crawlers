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
            page = urllib.request.urlopen(url, timeout=1000)
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
        """
        content = self.request_to_page(self.main_url+'vote_ind.htm')
        soup = BeautifulSoup(content, "html.parser")
        table = soup.findAll('table',  {"class": "list"})
        trs_by_date = re.findall(re.escape('<!--START[')+'(.*?)'+re.escape('<!--END['), str(table), re.DOTALL)
        num_dates = len(trs_by_date) # TO LOOP (0,num,dates)
        object_list = []
        id = 1
        for x in range(0,num_dates):
            obj_soup = BeautifulSoup(trs_by_date[x], "html.parser")
            event_date = re.findall('^(.*?)'+re.escape(']-->'), trs_by_date[x], re.DOTALL)[0]
            tr_all = obj_soup.findAll('tr')
            for j in range(0,len(tr_all)):
                work_obj = tr_all[j].findAll('font')
                if j == 0:
                    event_title = work_obj[1].findAll('a')[0].text
                    event_link = self.main_url+work_obj[1].findAll('a')[0].attrs['href']
                else:
                    event_title = work_obj[0].findAll('a')[0].text
                    event_link = self.main_url+work_obj[0].findAll('a')[0].attrs['href']
                #event_date = work_obj[0].text
                
                object_list.append({'id' : id, 'date': event_date, 'title': event_title, 'url': event_link})
                id = id + 1

        #uprint(object_list)
        """
        
        object_list = [{'url': 'http://www.sangiin.go.jp/japanese/joho1/kousei/vote/189/189-0710-v001.htm', 'date': '2015/07/10', 'id': 1, 'title': '\u65e5\u7a0b\u7b2c\uff11\u3000\u5ec3\u68c4\u7269\u306e\u51e6\u7406\u53ca\u3073\u6e05\u6383\u306b\u95a2\u3059\u308b\u6cd5\u5f8b\u53ca\u3073\u707d\u5bb3\u5bfe\u7b56\u57fa\u672c\u6cd5\u306e\u4e00\u90e8\u3092\u6539\u6b63\u3059\u308b\u6cd5\u5f8b\u6848\uff08\u5185\u95a3\u63d0\u51fa\u3001\u8846\u8b70\u9662\u9001\u4ed8\uff09'}]
        legislators_dict = {}
        for obj_page in object_list:
            page_url = obj_page.get('url')
            bill_id = obj_page.get('id')
            print(page_url)
            content = self.request_to_page(page_url)
            obj_soup = BeautifulSoup(content, "html.parser")
            tables = obj_soup.findAll('div',  {"id": "ContentsBox"})[0].findAll('table')
            for k in range(4,len(tables)):
                work_all_legislators = tables[k].findAll('tr')
                party = tables[k].findAll('caption',  {"class": "party"})[0]
                party_name = re.findall(re.escape('>') + '(.*?)' + re.escape('('), str(party), re.DOTALL)[0]
                #uprint(party_name)
                for s in range(1,len(work_all_legislators)-1):
                    work_line = work_all_legislators[s].findAll('td')
                    
                    name_1 = work_line[2].text.strip()
                    name_2 = work_line[5].text.strip()
                    name_3 = work_line[8].text.strip()
                    
                    sansei_1 = work_line[0].find('img')
                    sansei_2 = work_line[3].find('img')
                    sansei_3 = work_line[6].find('img')
                    
                    hantai_1 = work_line[1].find('img')
                    hantai_2 = work_line[4].find('img')
                    hantai_3 = work_line[7].find('img')
                    
                    result_1 = ""
                    if(sansei_1 != None):
                        result_1 = "sansei"
                    elif (sansei_1 == None and hantai_1 == None):
                        result_1 = "spacer"
                    else:
                        result_1 = "hentai"
                        
                    result_2 = ""
                    if(sansei_2 != None):
                        result_2 = "sansei"
                    elif (sansei_2 == None and hantai_2 == None):
                        result_2 = "spacer"
                    else:
                        result_2 = "hentai"
                        
                    result_3 = ""
                    if(sansei_3 != None):
                        result_3 = "sansei"
                    elif (sansei_3 == None and hantai_3 == None):
                        result_3 = "spacer"
                    else:
                        result_3 = "hentai"
                        
                    if(name_1 != ''):
                        if( legislators_dict.get(str(hash(name_1))) == None ):
                            legislators_dict[str(hash(name_1))] = {}                    
                            legislators_dict.get(str(hash(name_1))).update({'name': name_1, 'party': party_name, 'bills': [] })
                            
                        legislators_dict.get(str(hash(name_1))).get('bills').append({bill_id: result_1})
                    
                    if(name_2 != ''):
                        if( legislators_dict.get(str(hash(name_2))) == None ):
                            legislators_dict[str(hash(name_2))] = {}                    
                            legislators_dict.get(str(hash(name_2))).update({'name': name_2, 'party': party_name, 'bills': [] })
                            
                        legislators_dict.get(str(hash(name_2))).get('bills').append({bill_id: result_2})
                    
                    if(name_3 != ''):
                        if( legislators_dict.get(str(hash(name_3))) == None ):
                            legislators_dict[str(hash(name_3))] = {}                    
                            legislators_dict.get(str(hash(name_3))).update({'name': name_3, 'party': party_name, 'bills': [] })
                            
                        legislators_dict.get(str(hash(name_3))).get('bills').append({bill_id: result_3})
                    
                    #uprint(s, result_1, result_2, result_3)
                        
            
        #uprint(len(legislators_dict))
        
        """"""
        workbook = xlsxwriter.Workbook(self.output_file)
        worksheet_1 = workbook.add_worksheet()

        header_format = workbook.add_format({'bold': True,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'fg_color': '#D7E4BC',
                                             'border': 1})

        main_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
        title_format = workbook.add_format({'bold': False, 'text_wrap': 1, 'border': 1, 'valign': 'vcenter'})
                                             
        worksheet_1.set_column('A:A', 8)
        worksheet_1.set_column('B:B', 15)
        worksheet_1.set_column('C:C', 220)

        worksheet_1.write(0, 0, 'Bill_ID', header_format)
        worksheet_1.write(0, 1, 'Date', header_format)
        worksheet_1.write(0, 2, 'Bill_name', header_format)

        row = 1
        col = 0
        
        for obj in object_list:
            worksheet_1.set_row(row, 50)
            worksheet_1.write(row, 0, obj.get('id'), main_format)
            worksheet_1.write(row, 1, obj.get('date'), main_format)
            worksheet_1.write(row, 2, obj.get('title'), title_format)
            row += 1
        
        
        worksheet_2 = workbook.add_worksheet()
                                             
        worksheet_2.set_column('A:A', 20)
        worksheet_2.set_column('B:B', 20)
        worksheet_2.set_column('C:ZZ', 20)

        worksheet_2.write(0, 0, 'Name', header_format)
        worksheet_2.write(0, 1, 'Party', header_format)

        for indx in range(0,len(object_list)):
            worksheet_2.write(0, indx+2, 'Bill_'+str(indx+1), header_format)

        row = 1
        col = 2
        
        for hash_id, legis in legislators_dict.items():
            worksheet_2.set_row(row, 30)
            worksheet_2.write(row, 0, legis.get('name'), main_format)
            worksheet_2.write(row, 1, legis.get('party'), main_format)
            for bill in legis.get('bills'):
                #uprint(bill)
                worksheet_2.write(row, col, list(bill.values())[0], title_format)
                col += 1
            
            row += 1
            col = 2
        
        workbook.close()
        
            
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.sangiin.go.jp/japanese/joho1/kousei/vote/189/', 'output_file': 'output.xlsx' }
    aggregator = Aggregator(settings)
    aggregator.start_process()