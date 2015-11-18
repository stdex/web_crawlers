#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        self.driver.find_element_by_id('downloadBottom').click()
        self.driver.implicitly_wait(60)

    def scrape(self):
        self.scrape_pdf()
        self.driver.quit()

if __name__ == '__main__':
    settings = { 'link' : 'https://www.yourticketprovider.nl/LiveContent/tickets.aspx?x=492449&y=8687&px=92AD8EAA22C9223FBCA3102EE0AE2899510C03E398A8A08A222AFDACEBFF8BA95D656F01FB04A1437669EC46E93AB5776A33951830BBA97DD94DB1729BF42D76&rand=a17cafc7-26fe-42d9-a61a-894b43a28046&utm_source=PurchaseSuccess&utm_medium=Email&utm_campaign=SystemMails' }
    scraper = YourticketproviderScraper(settings)
    scraper.scrape()
