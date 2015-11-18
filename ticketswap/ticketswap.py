#!/usr/bin/env python

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from pyvirtualdisplay import Display

class TicketswapScraper(object):
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
        link, password, username = [config.get(k) for k in sorted(config.keys())]
        self.link = link
        self.username = username
        self.password = password

    def scrape_pdf(self):
        self.driver.get(self.link)
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_name('email').send_keys(self.username)
        self.driver.find_element_by_name('pass').send_keys(self.password)
        self.driver.find_element_by_name('pass').send_keys(Keys.RETURN)
        self.driver.implicitly_wait(10)

    def scrape(self):
        self.scrape_pdf()
        self.driver.quit()

if __name__ == '__main__':
    settings = { 'username': 'sergey7@e-kirov.ru', 'password': 'stdex11', 'link' : 'http://click.ticketswap.nl/track/click/30039336/www.ticketswap.nl?p=eyJzIjoiY0x6N3NXYThpZ0VGTGVsNVJzRC16R2hGVGFBIiwidiI6MSwicCI6IntcInVcIjozMDAzOTMzNixcInZcIjoxLFwidXJsXCI6XCJodHRwczpcXFwvXFxcL3d3dy50aWNrZXRzd2FwLm5sXFxcL2Rvd25sb2FkXFxcLzM2MTUyOFxcXC9jMTA5YmJjOWI4OGYzYTEyNTBjZDk3MTQyMmE2YWVkYVxcXC83NjQyNzFcIixcImlkXCI6XCIxNmE4NWI4Yzc5NmE0Y2UwOTk0Njc0M2RmM2MzODZkZlwiLFwidXJsX2lkc1wiOltcImQ4M2U3YmJmOTU3MTFkNDcyM2U4NjJlNTA1MWNjMWVhNTU5MDZlZjlcIl19In0' }
    scraper = TicketswapScraper(settings)
    scraper.scrape()
