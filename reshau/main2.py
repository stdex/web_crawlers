'''
Created on Oct 21, 2014
Modified on Dec 21, 2014
Version 0.03
@author: sergey@rostunov.com
A simple python script to parse the reshuege.ru website for content.
'''

from bs4 import BeautifulSoup
import urllib.request
from socket import timeout
import re
import sys

# pages = []
# surl = 'http://hist.reshuege.ru'
# stext = urllib.request.urlopen(surl).read()
# soup = BeautifulSoup(stext)
#
# data = soup.findAll('form', attrs={'id': 'catform'})
# for div in data:
#     links = div.findAll('a')
#     for a in links:
#         pages.append( surl + a['href'] )
# print(pages)

pages = []
pages = ['http://hist.reshuege.ru/test?theme=1', 'http://hist.reshuege.ru/test?theme=56', 'http://hist.reshuege.ru/test?theme=55', 'http://hist.reshuege.ru/test?theme=95', 'http://hist.reshuege.ru/test?theme=96', 'http://hist.reshuege.ru/test?theme=97', 'http://hist.reshuege.ru/test?theme=57', 'http://hist.reshuege.ru/test?theme=58', 'http://hist.reshuege.ru/test?theme=2', 'http://hist.reshuege.ru/test?theme=62', 'http://hist.reshuege.ru/test?theme=59', 'http://hist.reshuege.ru/test?theme=3', 'http://hist.reshuege.ru/test?theme=63', 'http://hist.reshuege.ru/test?theme=60', 'http://hist.reshuege.ru/test?theme=4', 'http://hist.reshuege.ru/test?theme=5', 'http://hist.reshuege.ru/test?theme=61', 'http://hist.reshuege.ru/test?theme=64', 'http://hist.reshuege.ru/test?theme=6', 'http://hist.reshuege.ru/test?theme=65', 'http://hist.reshuege.ru/test?theme=66', 'http://hist.reshuege.ru/test?theme=7', 'http://hist.reshuege.ru/test?theme=68', 'http://hist.reshuege.ru/test?theme=67', 'http://hist.reshuege.ru/test?theme=8', 'http://hist.reshuege.ru/test?theme=69', 'http://hist.reshuege.ru/test?theme=70', 'http://hist.reshuege.ru/test?theme=72', 'http://hist.reshuege.ru/test?theme=48', 'http://hist.reshuege.ru/test?theme=71', 'http://hist.reshuege.ru/test?theme=9', 'http://hist.reshuege.ru/test?theme=49', 'http://hist.reshuege.ru/test?theme=10', 'http://hist.reshuege.ru/test?theme=52', 'http://hist.reshuege.ru/test?theme=11', 'http://hist.reshuege.ru/test?theme=51', 'http://hist.reshuege.ru/test?theme=50', 'http://hist.reshuege.ru/test?theme=12', 'http://hist.reshuege.ru/test?theme=53', 'http://hist.reshuege.ru/test?theme=54', 'http://hist.reshuege.ru/test?theme=73', 'http://hist.reshuege.ru/test?theme=74', 'http://hist.reshuege.ru/test?theme=75', 'http://hist.reshuege.ru/test?theme=14', 'http://hist.reshuege.ru/test?theme=77', 'http://hist.reshuege.ru/test?theme=78', 'http://hist.reshuege.ru/test?theme=15', 'http://hist.reshuege.ru/test?theme=79', 'http://hist.reshuege.ru/test?theme=80', 'http://hist.reshuege.ru/test?theme=136', 'http://hist.reshuege.ru/test?theme=16', 'http://hist.reshuege.ru/test?theme=81', 'http://hist.reshuege.ru/test?theme=82', 'http://hist.reshuege.ru/test?theme=19', 'http://hist.reshuege.ru/test?theme=13', 'http://hist.reshuege.ru/test?theme=87', 'http://hist.reshuege.ru/test?theme=88', 'http://hist.reshuege.ru/test?theme=85', 'http://hist.reshuege.ru/test?theme=86', 'http://hist.reshuege.ru/test?theme=18', 'http://hist.reshuege.ru/test?theme=76', 'http://hist.reshuege.ru/test?theme=17', 'http://hist.reshuege.ru/test?theme=83', 'http://hist.reshuege.ru/test?theme=84', 'http://hist.reshuege.ru/test?theme=20', 'http://hist.reshuege.ru/test?theme=89', 'http://hist.reshuege.ru/test?theme=90', 'http://hist.reshuege.ru/test?theme=91', 'http://hist.reshuege.ru/test?theme=92', 'http://hist.reshuege.ru/test?theme=94', 'http://hist.reshuege.ru/test?theme=93', 'http://hist.reshuege.ru/test?theme=21']

outputTxt = 'hist_res.txt'
open(outputTxt, 'w').close()

for page in pages:

    try:
        rWeb = urllib.request.urlopen(page, timeout=1000)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            print(page)
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
        sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', page)

    rSoup = BeautifulSoup(rWeb)

    divQ = rSoup.findAll('div', id=re.compile('^maindiv'))
    divT = rSoup.find("div", {"style": "padding-top:3px;vertical-align:middle;width:100%;height:25px; margin-bottom:2px"}).get_text(strip=True).replace('Каталог заданий.','')
    typeTask = rSoup.find("span", {"style": "text-indent:0;display:inline-block;font-weight:bold"}).get_text(strip=True)[0:4].replace(' ', '')

    with open(outputTxt, "a") as f:
        f.write(divT)

        out = {}
        cnt = 0
        for i in divQ:
            # typeTask = i.find("span", {"style": "text-indent:0;display:inline-block;font-weight:bold"}).get_text(strip=True)[0:3].replace(' ', '')
            quest = i.findAll('div', id=re.compile('^body'))
            clar = i.findAll('div', id=re.compile('^sol'))
            clarification = clar[0].findAll("p", {"class": "left_margin"})[1].get_text(strip=True).replace('­', '').replace('\xa0', ' ').strip()
            correct_answer = i.find("span", {"style": "letter-spacing: 2px;"}).get_text(strip=True)[7:8]
            source = i.findAll(text = re.compile('Источник'))
            if(len(source)>0):
                src = '<br/>'+source[0].replace('\xad','')
            else:
                src = ''

            #print(src)

            text = quest[0].findAll(text=True)
            x = len(text)
            z = 2
            question = text[1].replace('­', '').replace('\xad','').strip()
            while z < x:
                #.replace('\xa0','')
                result = text[z].replace('­', '').replace('\xad','').replace('\tВ.','').replace('\tР.','').replace('\tН.','').replace('\t',' ').replace('  ',' ').strip('')
                ans_regex = re.split('(?:^|, )\d{1,2}\) ', result)
                #print(ans_regex)
                if len(ans_regex)<=1 and result != "auto generated from answers" and result != "" and result != "\xa0" and result.find("№") == -1:
                    #print(result)
                    question = question + "<br/>" + result

                z += 1

            f.write('#'+ question)

            answers = {}
            cnt_ans = 0
            z = 0
            while z < x:
                result = text[z].replace('­', '').replace('\xad','').strip()
                ans_regex = re.split('(?:^|, )\d{1,2}\) ', result)
                #print( len(ans_regex))
                #print(result)
                if result != "auto generated from answers" and result != "" and result.find("№") == -1 and result.find("?") == -1 and len(ans_regex)>1:
                    if result[0].isdigit():
                        result = result[3:]
                        #print(result.strip())
                    # if any(char.isdigit() for char in result):
                    #     result = re.split("\d+", result)
                        if cnt_ans + 1 == int(correct_answer):
                            corr = 1
                        else:
                            corr = 0
                        #answer = result[1].replace(') ', '').strip()
                        answer = result.strip()
                        answers[cnt_ans] = {'answer': answer, 'accurate': corr}

                        if cnt_ans == 0:
                            d = '##'
                            p = '#' + clarification+src + '#' + typeTask
                        else:
                            d = '###'
                            p = '##'

                        if corr == 1:
                            c = '#*###'
                        else:
                            c = '####'
                        if answer == '':
                            print('empty-answer on page: ' + page + '\n' + 'question:' + question + '\n')
                            print(result)


                        if clarification == '':
                            print('empty-clarification on page: ' + page + '\n' + 'question:' + question + '\n')
                            print(result)

                        f.write(d + answer + c + p + '\n')
                        # print(result[1].replace(') ', '').strip())
                        # print(re.split(r'(\W+)', result))
                        # print(result[1])
                        cnt_ans += 1

                z += 1

            out[cnt] = {'type': typeTask, 'question': question, 'answers': answers}
            cnt += 1

        # print(out)

        f.close()