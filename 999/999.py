from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from urllib.parse import urlparse
from socket import timeout
import re
import sys
import os
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
            content = ''
            page = urllib.request.urlopen(url)
            content = page.read()
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('Failed to connect to server.')
                print('Reason: ', e.reason)
                print(url)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
            return (content, 1)
            #sys.exit(1)
        except timeout:
            print('socket timed out - URL %s', url)
            
        return (content, 0)

    def start_process(self):
        result = []
        for inx in range(1,20369773):
            content = ''
            (content, er) = self.request_to_page(self.main_url+inx.__str__())
            if( er != 1):
                soup = BeautifulSoup(content, "lxml")
                dl = soup.find('dl', {'class': 'adPage__content__phone grid_18'})
                if(len(dl) >0):
                    tel = dl.find('a').attrs['href'].replace('tel:','').strip()
                    myfile = open(self.output_file, 'a')
                    myfile.write("%s\n" % tel) 
                    myfile.close()
                    #print(tel)
            else:
                continue

        
if __name__ == '__main__':
    settings = { 'main_url': 'http://999.md/', 'output_file': 'output.txt' }
    aggregator = Aggregator(settings)
    aggregator.start_process()