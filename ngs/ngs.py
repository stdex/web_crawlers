#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import uuid
import re
#from pyvirtualdisplay import Display

class YourticketproviderScraper(object):
    def __init__(self, config):
        
        # If need to work in background use pyvirtualdisplay
        # http://stackoverflow.com/a/23447450 
        #display = Display(visible=0, size=(800, 600))
        #display.start()

        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("network.cookie.lifetimePolicy", 0)
        fp.set_preference("network.cookie.alwaysAcceptSessionCookies", True)
        fp.set_preference("network.cookie.cookieBehavior", 0)
        fp.set_preference("profile.default_content_settings.cookies", 0)
        self.driver = webdriver.Firefox(firefox_profile=fp)

        #self.driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')
        self.driver.set_window_size(1120, 550)
        link = [config.get(k) for k in sorted(config.keys())]
        self.link = link
    
    def scrape_mail(self):
        print(self.link[0])
        self.driver.get('https://ngs.ru/')
        for inx in range(0,101):
            self.driver.get(self.link[0])
            self.driver.implicitly_wait(10)
            self.driver.find_element_by_name('registration-variant').click()
            randname = str(uuid.uuid4().hex[0:8])
            with open("test.txt", "a") as myfile:
                myfile.write(randname+"@ngs.ru:"+randname+"\n")
            self.driver.find_element_by_name('name').send_keys("test test")
            self.driver.find_element_by_name('name-before-at').send_keys(randname)
            self.driver.find_element_by_name('password').send_keys(randname)
            self.driver.find_element_by_name('one-more-password').send_keys(randname)
            wait = WebDriverWait(self.driver, 300).until(EC.element_to_be_clickable((By.ID,'td_header_right1')))
            self.driver.find_element_by_partial_link_text('Выход').click();
    
    def scrape(self):
        self.scrape_mail()
        #self.driver.quit()

if __name__ == '__main__':
    settings = { 'link' : 'https://passport.ngs.ru/register/?return=https://mail.ngs.ru/' }
    scraper = YourticketproviderScraper(settings)
    scraper.scrape()
