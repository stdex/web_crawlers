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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def start_process(self):
        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("network.cookie.lifetimePolicy", 0)
        fp.set_preference("network.cookie.alwaysAcceptSessionCookies", True)
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("profile.default_content_settings.cookies", 0)
        self.driver = webdriver.Firefox(firefox_profile=fp)

        #self.driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')
        self.driver.set_window_size(1120, 550)
        self.driver.get(self.main_url)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_class_name('h2').click()
        date_menu = self.driver.find_element_by_id('ifmenu-calendar-content')
        date_items = date_menu.find_elements_by_tag_name("li")
        for idate in date_items:
            print (idate.text)
            
        date_items[8].click()
        self.driver.implicitly_wait(10)
        sleep(1)
        #pageElement = self.driver.find_element_by_id("fs")
        #wait = WebDriverWait(self.driver, 10).until(EC.staleness_of(pageElement))
        matches_list = self.driver.find_elements_by_xpath("//table[@class='soccer']")
        matches_list = matches_list[:-49]
        print(len(matches_list))
        #print(len(matches_list))
        # loop by country
        for imatch in matches_list:
            itbody = imatch.find_element_by_tag_name("tbody")
            #print(imatch.text)
            mtrs = itbody.find_elements_by_tag_name("tr")
            #mtrs = imatch.find_elements_by_xpath("//tr[@class='stage-scheduled']")
            mtrs[0].click()
            # loop by matches
            #for mtr in mtrs:
            #    print(mtr.text)
            
            #prepare handlers
            matches_title = str(self.driver.title)
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                if(self.driver.title != matches_title):
                    statistic_title = str(self.driver.title)
                    statistic_handle = handle
                else:
                    matches_handle = handle
            
            #switch to statistic page
            self.driver.switch_to.window(statistic_handle)
            sleep(3)
            print(self.driver.title)
            #print(self.driver.window_handles)
            team_titles = self.driver.find_elements_by_xpath("//span[@class='tname']")
            print(team_titles[0].text.strip(), '-', team_titles[1].text.strip())
            bets_coef_table = self.driver.find_element_by_id('default-odds')
            bets_coef_tds = bets_coef_table.find_element_by_tag_name("tbody").find_element_by_xpath("//tr[@class='odd']").find_elements_by_tag_name("td")
            #for td in bets_coef_tds:
            #    print(td.text)
            """
            bets_p1 = bets_coef_tds[1].find_element_by_tag_name("span").text.strip()
            bets_p2 = bets_coef_tds[3].find_element_by_tag_name("span").text.strip()
            bets_n = bets_coef_tds[2].find_element_by_tag_name("span").text.strip()
            """
            bets_p1 = bets_coef_table.find_elements_by_xpath("//td[@class='kx o_1']")[1].text.strip()
            #for p1 in bets_p1:
            #    print(p1.text)
            bets_p2 = bets_coef_table.find_elements_by_xpath("//td[@class='kx o_2']")[1].text.strip()
            #for p2 in bets_p2:
            #    print(p2.text)
            bets_n = bets_coef_table.find_elements_by_xpath("//td[@class='kx o_0']")[1].text.strip()
            #for n in bets_n:
            #    print(n.text)
            print(bets_p1, bets_n, bets_p2)
            
            
        """
        items_all = soup.findAll('a',  {"class": "categoryLink"})
        items = [ x.attrs['href'] for x in items_all ]
        items = items[:-47]
        print(items)
        #out = []
        for itm in items:
            cat_url = self.main_url + "/" + itm
            print(cat_url)
            content_cat = self.request_to_page(cat_url)
            soup_cat = BeautifulSoup(content_cat, "lxml")
            last_page_inx = soup_cat.find('a',  {"class": "addax-cs_hl_lastpage"}).attrs['href'].split(',')[1].replace('.html','')
            #last_page_inx = 2
            for inx in range(1,int(last_page_inx)+1):
                page_url = self.main_url + "/" + itm + "/firmy," + str(inx) + ".html"
                print(page_url)
                content_page = self.request_to_page(page_url)
                soup_page = BeautifulSoup(content_page, "lxml")
                mails = soup_page.findAll('a',  {"class": "icon-mail"})
                mails_list = [ m.attrs['href'].replace('mailto:','') for m in mails ]
                #out += mails_list
                for ml in mails_list:
                    output.writerow([ml])
                sleep(0.1)
        """
        
if __name__ == '__main__':
    settings = { 'main_url': 'http://www.myscore.ru/', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
