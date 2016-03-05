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
        
        output = csv.writer(open(self.output_file, 'w', newline=''),  delimiter=';')
        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("network.cookie.lifetimePolicy", 0)
        fp.set_preference("network.cookie.alwaysAcceptSessionCookies", True)
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("profile.default_content_settings.cookies", 0)
        self.driver = webdriver.Firefox(firefox_profile=fp)

        #self.driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')
        
        self.driver.set_window_size(1120, 550)
        for inx in range(1,29):
            self.driver.get(self.main_url + "/top/p" + str(inx) + "-0-0.htm")
            self.driver.implicitly_wait(10)
            topl = (self.driver.find_elements_by_xpath("//td[@class='topl']"))[1:]
            print(len(topl))
            for top in topl:
                sitename = top.find_element_by_tag_name("span").text
                output.writerow(["http://"+sitename])
                #print("http://"+sitename)

        
if __name__ == '__main__':
    settings = { 'main_url': 'http://agroserver.ru', 'output_file': 'output.csv' }
    aggregator = Aggregator(settings)
    aggregator.start_process()
