import csv
import re
import time
import undetected_chromedriver as uc
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from seleniumbase import SB
from selenium.webdriver.common.by import By


headers_csv = ['Apartment_names', 'Adresse', 'PLZ', 'Ort', 'Telefon', 'Email', 'Website', 'Source_Link']
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}

# chrome_options.add_argument("--incognito")
with open('hotelleriesuisse_old.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers_csv)


link = 'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-hotel-bad-muntelier-am-see'
# link = 'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-22-summits-boutique-hotel'
# link = 'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-apparthotel-casa-vanessa'
response_hotel_profile = requests.get(link, headers=headers)
soup_hotel_profile = BeautifulSoup(response_hotel_profile.content, 'lxml')
name_hotel_profile = (soup_hotel_profile.find('h1', class_='HeaderSubpage--title').contents[0].text.strip()
                      + ' ' + soup_hotel_profile.find('h1', class_='HeaderSubpage--title').contents[
                          2].text.strip())
try:
    spezialisierungs = soup_hotel_profile.find_all('span', class_='Button secondary sidebar image non-interactive')
    spezialisierung1= ''
    spezialisierung2= ''
    spezialisierung3= ''
    counter_of_spezialisierung = 0
    for i in spezialisierungs:
        counter_of_spezialisierung += 1
        if counter_of_spezialisierung == 1:
            spezialisierung1 = i.text.strip()
        elif counter_of_spezialisierung == 2:
            spezialisierung2 = i.text.strip()
        elif counter_of_spezialisierung == 3:
            spezialisierung3 = i.text.strip()
except:
    spezialisierung = 'N/A'
try:
    klassifikation = soup_hotel_profile.find('div', class_='SidebarSection--text').text.strip()
except:
    klassifikation = 'N/A'

block_info_hotel_profile = soup_hotel_profile.find('div', class_='SidebarSection')
res = block_info_hotel_profile.find('p').contents
if len(block_info_hotel_profile.find('p').contents) < 3:
    address_hotel_profile = ''
    PLZ = block_info_hotel_profile.find('p').contents[0].split(' ')[0].strip()
    Ort = block_info_hotel_profile.find('p').contents[0].split(' ')[1].strip()
else:
    if len(block_info_hotel_profile.find('p').text.strip().split(' ')) <= 2:
        address_hotel_profile = ''
        PLZ = block_info_hotel_profile.find('p').contents[2].split(' ')[0].strip()
        Ort = ' '.join(block_info_hotel_profile.find('p').contents[2].split(' ')[1:])
    else:
        address_hotel_profile = block_info_hotel_profile.find('p').contents[0].strip()
        PLZ = block_info_hotel_profile.find('p').contents[2].split(' ')[0].strip()
        Ort = block_info_hotel_profile.find('p').contents[2].split(' ')[1].strip()
all_links_in_info_block = block_info_hotel_profile.find_all('a', class_='Button secondary sidebar')
for link_block_info in all_links_in_info_block:
    if 'tel:' in link_block_info['href']:
        try:
            telephones_hotel_profile = link_block_info['href'].split(':')[1]
        except KeyError:
            telephones_hotel_profile = ''
    elif 'www' or '.ch' in link_block_info['href']:
        try:
            url_hotel_profile = link_block_info['href']
            if url_hotel_profile == '#':
                url_hotel_profile = ''
        except KeyError:
            url_hotel_profile = ''






