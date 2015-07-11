from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from socket import timeout
import re
import sys
import os
from os.path import basename, splitext
from urllib.parse import urlparse
import json

"""
Prepare main url with params
"""
main_url = "http://www.bac-lac.gc.ca/eng/discover/immigration/immigration-records/passenger-lists/passenger-lists-1865-1922/Pages/"
#search_params = {'ShipName':'OTTAWA', 'Year':'1908', 'ArrivalPort':'', 'ShippingLine':'', 'DeparturePort':'', 'DepartureDate':'', 'ArrivalDate':''}
#search_params = {'ShipName':'MARINA', 'Year':'1909', 'ArrivalPort':'', 'ShippingLine':'', 'DeparturePort':'', 'DepartureDate':'', 'ArrivalDate':''}
search_params = {'ShipName':'MARINA', 'Year':'', 'ArrivalPort':'', 'ShippingLine':'', 'DeparturePort':'', 'DepartureDate':'', 'ArrivalDate':''}
for x in list(search_params.keys()):
    if search_params[x] == '':
        del search_params[x]
        
search_result_url = main_url + 'list.aspx?' + urllib.parse.urlencode(search_params)
print(search_result_url)

"""
Do request for main url
"""
try:
    search_result_page = urllib.request.urlopen(search_result_url, timeout=1000)
except urllib.error.URLError as e:
    if hasattr(e, 'reason'):
        print('Failed to connect to server.')
        print('Reason: ', e.reason)
        print(search_result_url)
    elif hasattr(e, 'code'):
        print('Error code: ', e.code)
    sys.exit(1)
except timeout:
    print('socket timed out - URL %s', search_result_url)

dom_search_result_page = BeautifulSoup(search_result_page, "html.parser")

"""
Parse pagination urls
"""
search_paging = dom_search_result_page.findAll('div',  {"class": "search_paging"})
paging_links = search_paging[0].findAll('a')

paging_urls = []
for page_link in paging_links:
    if (page_link.text.strip() != 'Next >'):
        paging_urls.append(page_link.attrs['href'])

print(paging_urls)

def parse_one_page(url):
    print(url)
    try:
        one_page = urllib.request.urlopen(url, timeout=1000)
    except urllib.error.URLError as e:
        if hasattr(e, 'reason'):
            print('Failed to connect to server.')
            print('Reason: ', e.reason)
            print(url)
        elif hasattr(e, 'code'):
            print('Error code: ', e.code)
        sys.exit(1)
    except timeout:
        print('socket timed out - URL %s', url)

    dom_page = BeautifulSoup(one_page, "html.parser")

    """
    Parse items urls
    """
    items_dom = dom_page.findAll('table',  {"class": "result_table table table-striped table-bordered"})
    items_links = items_dom[0].findAll('a')

    items_urls = []
    for item_link in items_links:
        items_urls.append(main_url + item_link.attrs['href'])

    print(items_urls)

    """
    Parse item parameters
    """
    dict_items = {}
    for page in items_urls:

        try:
            item_page = urllib.request.urlopen(page, timeout=1000)
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
            
        dom_item_page = BeautifulSoup(item_page, "html.parser")
        
        items_dom = dom_item_page.findAll('div',  {"id": "GenappContent"})
        item_divs = items_dom[0].findAll('div', {"class": "genapp_item_display_container"})
        
        item_dict = {}
        current_item_id = ""
        for item in item_divs:
            label = item.findAll('div',  {"class": "genapp_item_display_label"})[0].text.strip()
            data = item.findAll('div',  {"class": "genapp_item_display_data"})[0].text.strip()
            if(label == 'Ship:'):
                item_dict.update({'ShipName': data})
            elif(label == 'Port of Departure:'):
                item_dict.update({'DeparturePort': data})
            elif(label == 'Date of Departure:'):
                item_dict.update({'DepartureDate': data})
            elif(label == 'Port of Arrival:'):
                item_dict.update({'ArrivalPort': data})
            elif(label == 'Date of Arrival:'):
                item_dict.update({'ArrivalDate': data})
            elif(label == 'Year:'):
                item_dict.update({'Year': data})
            elif(label == 'Microfilm Reel Number:'):
                item_dict.update({'Microfilm': data})
            elif(label == 'Reference:'):
                item_dict.update({'Reference': data})
            elif(label == 'Item Number:'):
                item_dict.update({'ItemNumber': data})
                current_item_id = data

        images_dom = dom_item_page.findAll('div',  {"id": "bl-slideshow-inner"})
        images_links = images_dom[0].findAll('a')
        #print(images_links)

        images_item = {}
        img_id = 0
        for img_link in images_links:
            img_id = img_id + 1
            imgpage_url = main_url + img_link.attrs['href']
            try:
                image_page = urllib.request.urlopen(imgpage_url, timeout=1000)
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
                

            dom_image_page = BeautifulSoup(image_page, "html.parser")
            image_dom = dom_image_page.findAll('div',  {"id": "imageDiv"})
            image_url = image_dom[0].findAll('img')[0].get('src')
            images_item.update({img_id: image_url})


        item_dict.update({'Images': images_item})
        dict_items.update({current_item_id:item_dict})

    return (dict_items)
    

result_dict = {}
result_dict.update(parse_one_page(search_result_url))

for page_url in paging_urls:
    result_dict.update(parse_one_page(page_url))

print(result_dict)

"""
Generete JSON
"""
#print(simplejson.dumps(dict_items))
#print(json.dumps(dict_items))




