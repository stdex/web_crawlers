#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#from pyvirtualdisplay import Display

class YourticketproviderScraper(object):
    def __init__(self, config):
        
        # If need to work in background use pyvirtualdisplay
        # http://stackoverflow.com/a/23447450 
        #display = Display(visible=0, size=(800, 600))
        #display.start()
        
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.dir", os.getcwd())
        fp.set_preference("browser.download.useDownloadDir", True)
        fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
        fp.set_preference("browser.download.manager.focusWhenStarting", False)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.manager.closeWhenDone", True)
        fp.set_preference("browser.download.manager.showAlertOnComplete", False)
        fp.set_preference("browser.download.manager.useWindow", False)
        fp.set_preference("browser.download.manager.showAlertOnComplete", False)
        fp.set_preference("pdfjs.disabled", True)
        fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
        
        self.driver = webdriver.Firefox(firefox_profile=fp)
        #self.driver.set_window_size(1120, 550)
        link = [config.get(k) for k in sorted(config.keys())]
        self.link = link

    def scrape_pdf(self):
        self.driver.get(self.link)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_class_name('ticketLink').click()
        time.sleep(8)
        #self.driver.implicitly_wait(90)

    def scrape(self):
        self.scrape_pdf()
        self.driver.quit()

if __name__ == '__main__':
    settings = { 'link' : 'https://radionamsterdam.stager.nl/web/orders/347620/zTCjCwf2h149QXVmpHT1nV6YWzslI1' }
    scraper = YourticketproviderScraper(settings)
    scraper.scrape()
