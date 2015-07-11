'''
Created on Oct 21, 2014
Modified on May 28, 2015
Version 0.04
@author: sergey@rostunov.com
A simple python script to parse the reshuege.ru website for content.
'''

from bs4 import BeautifulSoup
import urllib.request
from socket import timeout
import re
import sys
import os
from os.path import basename, splitext
from urllib.parse import urlparse

# pages = []
# surl = 'http://soc.reshuege.ru/'
# stext = urllib.request.urlopen(surl).read()
# soup = BeautifulSoup(stext)
#
# data = soup.findAll('form', attrs={'id': 'catform'})
# for div in data:
#     links = div.findAll('a')
#     for a in links:
#         pages.append( surl + a['href'] )
# print(pages)

url_img = "http://soc.reshuege.ru/"

pages = []

pages = ['http://soc.reshuege.ru//test?theme=3', 'http://soc.reshuege.ru//test?theme=44', 'http://soc.reshuege.ru//test?theme=1', 'http://soc.reshuege.ru//test?theme=38', 'http://soc.reshuege.ru//test?theme=39', 'http://soc.reshuege.ru//test?theme=40', 'http://soc.reshuege.ru//test?theme=45', 'http://soc.reshuege.ru//test?theme=2', 'http://soc.reshuege.ru//test?theme=41', 'http://soc.reshuege.ru//test?theme=42', 'http://soc.reshuege.ru//test?theme=43', 'http://soc.reshuege.ru//test?theme=4', 'http://soc.reshuege.ru//test?theme=155', 'http://soc.reshuege.ru//test?theme=154', 'http://soc.reshuege.ru//test?theme=5', 'http://soc.reshuege.ru//test?theme=47', 'http://soc.reshuege.ru//test?theme=46', 'http://soc.reshuege.ru//test?theme=48', 'http://soc.reshuege.ru//test?theme=52', 'http://soc.reshuege.ru//test?theme=54', 'http://soc.reshuege.ru//test?theme=53', 'http://soc.reshuege.ru//test?theme=49', 'http://soc.reshuege.ru//test?theme=51', 'http://soc.reshuege.ru//test?theme=50', 'http://soc.reshuege.ru//test?theme=6', 'http://soc.reshuege.ru//test?theme=7', 'http://soc.reshuege.ru//test?theme=56', 'http://soc.reshuege.ru//test?theme=55', 'http://soc.reshuege.ru//test?theme=8', 'http://soc.reshuege.ru//test?theme=60', 'http://soc.reshuege.ru//test?theme=9', 'http://soc.reshuege.ru//test?theme=57', 'http://soc.reshuege.ru//test?theme=61', 'http://soc.reshuege.ru//test?theme=59', 'http://soc.reshuege.ru//test?theme=58', 'http://soc.reshuege.ru//test?theme=64', 'http://soc.reshuege.ru//test?theme=65', 'http://soc.reshuege.ru//test?theme=66', 'http://soc.reshuege.ru//test?theme=11', 'http://soc.reshuege.ru//test?theme=62', 'http://soc.reshuege.ru//test?theme=10', 'http://soc.reshuege.ru//test?theme=63', 'http://soc.reshuege.ru//test?theme=68', 'http://soc.reshuege.ru//test?theme=12', 'http://soc.reshuege.ru//test?theme=67', 'http://soc.reshuege.ru//test?theme=69', 'http://soc.reshuege.ru//test?theme=13', 'http://soc.reshuege.ru//test?theme=85', 'http://soc.reshuege.ru//test?theme=71', 'http://soc.reshuege.ru//test?theme=70', 'http://soc.reshuege.ru//test?theme=15', 'http://soc.reshuege.ru//test?theme=88', 'http://soc.reshuege.ru//test?theme=90', 'http://soc.reshuege.ru//test?theme=89', 'http://soc.reshuege.ru//test?theme=87', 'http://soc.reshuege.ru//test?theme=86', 'http://soc.reshuege.ru//test?theme=84', 'http://soc.reshuege.ru//test?theme=14', 'http://soc.reshuege.ru//test?theme=16', 'http://soc.reshuege.ru//test?theme=92', 'http://soc.reshuege.ru//test?theme=17', 'http://soc.reshuege.ru//test?theme=94', 'http://soc.reshuege.ru//test?theme=18', 'http://soc.reshuege.ru//test?theme=96', 'http://soc.reshuege.ru//test?theme=97', 'http://soc.reshuege.ru//test?theme=20',  'http://soc.reshuege.ru//test?theme=95', 'http://soc.reshuege.ru//test?theme=98', 'http://soc.reshuege.ru//test?theme=19', 'http://soc.reshuege.ru//test?theme=91', 'http://soc.reshuege.ru//test?theme=93']




for page in pages:

    theme_inx = dict([kvpair.split('=') for kvpair in page.split('&')]).popitem()[1]

    outputTxt = 'soc_res_theme_'+theme_inx+'.txt'
    open(outputTxt, 'w').close()

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
    typeTask = rSoup.find("span", {"style": "text-indent:0;display:inline-block;font-weight:bold"}).get_text(strip=True)[0:11].replace(' ', '')
    # print(typeTask)

    with open(outputTxt, "a") as f:
        f.write(divT)

        out = {}
        cnt = 0
        for i in divQ:
            # typeTask = i.find("span", {"style": "text-indent:0;display:inline-block;font-weight:bold"}).get_text(strip=True)[0:3].replace(' ', '')
            quest = i.findAll('div', id=re.compile('^body'))
            clar = i.findAll('div', id=re.compile('^sol'))
            # clarification = clar[0].findAll("p", {"class": "left_margin"})[1].get_text(strip=True).replace('­', '').replace('\xa0', ' ').strip()
            correct_answer = i.find("span", {"style": "letter-spacing: 2px;"}).get_text(strip=True)[7:8]
            source = i.findAll(text = re.compile('Источник'))
            if(len(source)>0):
                src = '<br/>'+source[0].replace('\xad','').replace('\n', '')
            else:
                src = ''

            # print(source)

            clarification = ""
            for index, w in enumerate(clar[0].findAll("p")):
                if(index != len(clar[0].findAll("p"))-1 and w.get_text(strip=True).replace('­', '').replace('\xa0', ' ').strip() != ""):
                    clarification = clarification + w.get_text(strip=True).replace('­', '').replace('\xa0', ' ').strip() + "<br/>"
                    # print(w.get_text(strip=True).replace('­', '').replace('\xa0', ' ').strip())


            text = quest[0].findAll(text=True)

            text_new = ""
            if(re.search("<!--auto generated from answers-->", str(quest[0])) != None):

                text_new = (re.compile(r'<(div|TAGX).*?>|</div>').sub('', re.sub(r'<(span|TAGX).*?>.*?</\1>', '', BeautifulSoup(str(quest[0]).split('<!--auto generated from answers-->')[0]).prettify().replace('­', '').replace('\xad','').strip().replace('\n', '').replace('   <p class="left_margin">   </p>   <div style="width:20px;height:5px;display:inline">   </div>   ', '').replace('<html> <body>  ', '').replace(' </body></html>', '').replace('     ', '') )).replace('   ', '').replace('<p></p>',''))

                soup = BeautifulSoup(text_new)
                for img in soup.findAll('img'):
                    print(img['src'])
                    if 'reshuege.ru:89' in img['src']:
                        img['src'] = url_img + 'get_file?id=' + splitext(basename(img['src']))[0]
                        imgname = str(splitext(basename(img['src']))[0])[12:]
                    elif 'reshuege.ru/formula/' in img['src']:
                        img['src'] = img['src']
                        imgname = splitext(basename(img['src']))[0]
                    else:
                        img['src'] = url_img + splitext(basename(img['src']))[0]
                        imgname = str(splitext(basename(img['src']))[0])[12:]

                    print(img['src'])
                    img['style'] = ''
                    img_source = urllib.request.urlopen(img['src']).read()
                    imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__))+'/img/', imgname+'.png')
                    # if not os.path.exists(os.path.abspath(__file__)+'/img/'+theme_inx+'/'):
                    #     os.makedirs(os.path.abspath(__file__)+'/img/'+theme_inx+'/')
                    s = open(imgpath, "wb")
                    s.write(img_source)
                    s.close()

                text_new = str(soup)
                text_new = text_new.replace('<html><body>', '').replace('</body></html>','').replace('  ','')
                # print(BeautifulSoup(re.sub(r'<(span|TAGX).*?>.*?</\1>', '', BeautifulSoup(str(quest[0]).split('<!--auto generated from answers-->')[0]).prettify().replace('­', '').replace('\xad','').strip().replace('\n', '').replace('   <p class="left_margin">   </p>   <div style="width:20px;height:5px;display:inline">   </div>   ', '').replace('<html> <body>  ', '').replace(' </body></html>', '').replace('     ', '') )).find_all("div", class_="nobreak pbody"))


                # print(BeautifulSoup(BeautifulSoup(str(quest[0]).split('<!--auto generated from answers-->')[0]).prettify().replace('­', '').replace('\xad','').strip()).find_all("p", class_="left_margin"))
            else:
                text_new = '<p>'+str(BeautifulSoup(str(quest[0]).split('<p> </p>')[0]).findAll(text=True)[1].replace('­', '').replace('\xad','').strip())+'</p>'
            # print(str(quest[0]).split('<p> </p>')[0])
            # print(BeautifulSoup(str(quest[0]).split('<!--auto generated from answers-->')[0]).prettify().replace('­', '').replace('\xad','').strip())

            # print(text_new)

            question = text_new
            f.write('#'+ question)

            # img = ""
            # for tag in quest[0].findAll("img"):
            #     img = "<br/><img src='"+url_img+""+tag['src']+"' /><br/>"

            x = len(text)
            z = 2
            # question = text[1].replace('­', '').replace('\xad','').strip() + img
            #
            # while z < x:
            #     #.replace('\xa0','')
            #     result = text[z].replace('­', '').replace('\xad','').replace('\tВ.','').replace('\tР.','').replace('\tН.','').replace('\t',' ').replace('  ',' ').strip('')
            #     # print(result)
            #     ans_regex = re.split('(?:^|, )\d{1,2}\) ', result)
            #     # print(ans_regex)
            #     if len(ans_regex)<=1 and result != "auto generated from answers" and result != "" and result != "\xa0" and result.find("№") == -1:
            #         # print(result)
            #         question = question + "<br/>" + result
            #
            #     z += 1
            #
            # f.write('#'+ question)

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


                        # if clarification == '':
                        #     print('empty-clarification on page: ' + page + '\n' + 'question:' + question + '\n')
                        #     print(result)

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