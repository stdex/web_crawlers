from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from socket import timeout
import re
import sys
import os
from os.path import basename, splitext
from urllib.parse import urlparse
import json, csv, sys
import unicodedata
import codecs
from unicodedata import normalize
import xlsxwriter
import random
import os.path
import sys
import threading

class Mythread(threading.Thread):
    '''Download pictures.'''
    def __init__(self, id_product, path):
        threading.Thread.__init__(self)
        self.id_product = id_product
        self.path = path
        print ('init thread.')

    def run(self):
        print ('thread running')
        print ('begin downloading %s' % self.id_product)
        pattern_main = "http://www.vseinstrumenti.ru"
        try:
            pdf_source = urllib.request.urlopen(pattern_main+'/instructions/'+self.id_product+'.pdf')
            pdfpath = self.path+'/img_3d/instructions/'+self.id_product+'.pdf'
            print(pattern_main+'/instructions/'+self.id_product+'.pdf')
            print(pdfpath)
            s = open(pdfpath, "wb")
            s.write(pdf_source.read())
            s.close()
        except timeout:
            print('socket timed out - URL %s', self.id_product)
        except urllib.error.HTTPError as e:
            print('error - URL %s', self.id_product)   
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to connect to server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
            #sys.exit(1)

def main():
    #for id_product in range(1,727194):
    path = os.path.dirname(os.path.abspath(__file__))
    #for i in range(0,72719):
    for i in range(9839,9840):
        for id_product in range(i*10,(i+1)*10):
            mythread = Mythread(str(id_product),path)
            mythread.start()
        print ('main thread continues.')
        # wait for mythread
        mythread.join()

if __name__ == '__main__':
    main()
