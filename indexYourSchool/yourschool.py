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

all_items = []
for i in range(0, 9):
    offset = str(100*i+1)

    main_url = "http://api.news.com.au/mm/dataset/TAUS_yourschool_index_v13/select?callback=jsonp1436096207145&format=json&args%5Bcount%5D=100" \
    +"&args%5Bwhere%5D%5B0%5D%5Bfield%5D=type&args%5Bwhere%5D%5B0%5D%5Bop%5D=!%3D&args%5Bwhere%5D%5B0%5D%5Bvalue%5D=primary" \
    +"&args%5Bwhere%5D%5B1%5D%5Bfield%5D=sector&args%5Bwhere%5D%5B1%5D%5Bvalue%5D=non-government&args%5Bwhere%5D%5B2%5D%5Bfield%5D=location" \
    +"&args%5Bwhere%5D%5B2%5D%5Bvalue%5D=metropolitan&args%5Border%5D%5B0%5D%5Bfield%5D=average_total" \
    +"&args%5Border%5D%5B0%5D%5Bdir%5D=desc&args%5Boffset%5D="+offset
    
    print(main_url)
    
    try:
        page = urllib.request.urlopen(main_url, timeout=1000)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            print(main_url)
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
        sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', main_url)

    content = page.read()
    soup = BeautifulSoup(content, "html.parser")
    json_string = str(soup).replace(")","")
    json_string = re.sub(r'\jsonp.*?\(', '', json_string)
    data_dictionary=json.loads(json_string.replace('\r\n', ''), strict=False)
    #print(data_dictionary['items'])
    for ditem in data_dictionary['items']:
        all_items.append(ditem)


output = csv.writer(open('test.csv', 'w', newline=''),  delimiter=';')
output.writerow(list(all_items[0].keys()))

for row in all_items:
    output.writerow(list(row.values()))
