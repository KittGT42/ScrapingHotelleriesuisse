import csv
import time
import undetected_chromedriver as uc
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

headers_csv = ['Apartment_names', 'Spezialisierung 1', 'Spezialisierung 2', 'Spezialisierung 3', 'Klassifikation', 'Adresse', 'PLZ', 'Ort', 'Telefon', 'Email',
               'Website', 'Source_Link']
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}
chrome_options = uc.ChromeOptions()

chrome_options.add_argument("--disable-extensions")

chrome_options.add_argument("--disable-popup-blocking")

chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_argument("--ignore-certificate-errors")

chrome_options.add_argument("--disable-plugins-discovery")

# chrome_options.add_argument("--incognito")
# with open('hotelleriesuisse_new.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(headers_csv)

chrome_options.add_argument("user_agent=DN")
driver = uc.Chrome(options=chrome_options)

driver.delete_all_cookies()
url = 'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-page-1?'
stock_url = 'https://www.hotelleriesuisse.ch'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'lxml')
last_page = soup.find('div', class_='Pagination--fraction-last').text.strip()
for page in range(115, int(last_page) + 1):
# for page in range(1, 2):
    print(f'{page} / {last_page}')
    url = f'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-page-{page}?'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    hotels = soup.find_all('li', class_='CardGrid--grid-item')
    len_hotels = len(hotels)
    counter = 0
    for hotel in hotels:
        counter += 1
        print(f'{counter}/{len_hotels}')
        link = stock_url + hotel.find('a')['href']
        response_hotel_profile = requests.get(link, headers=headers)
        soup_hotel_profile = BeautifulSoup(response_hotel_profile.content, 'lxml')
        time.sleep(1)
        try:
            name_hotel_profile = (soup_hotel_profile.find('h1', class_='HeaderSubpage--title').contents[0].text.strip()
                              + ' ' + soup_hotel_profile.find('h1', class_='HeaderSubpage--title').contents[
                                  2].text.strip())
        except:
            name_hotel_profile = 'NA'

        try:
            spezialisierungs = soup_hotel_profile.find_all('span',
                                                           class_='Button secondary sidebar image non-interactive')
            spezialisierung1 = ''
            spezialisierung2 = ''
            spezialisierung3 = ''
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
                telephones_hotel_profile = ''
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
        driver.get(link)
        driver.implicitly_wait(3)
        driver.execute_script("window.scrollBy(0,700)")
        time.sleep(2)
        try:
            driver.find_element(By.PARTIAL_LINK_TEXT, 'E-Mail').click()
            time.sleep(2)
            result = driver.current_url
            email = result.split('=')[4]
            with open('hotelleriesuisse_new.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(
                    [name_hotel_profile, spezialisierung1, spezialisierung2, spezialisierung3, klassifikation, address_hotel_profile, PLZ, Ort,
                     telephones_hotel_profile, email,url_hotel_profile, link])
        except:
            email = 'N/A'
            with open('hotelleriesuisse_new.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(
                    [name_hotel_profile, spezialisierung1, spezialisierung2, spezialisierung3, klassifikation,
                     address_hotel_profile, PLZ, Ort,
                     telephones_hotel_profile, email, url_hotel_profile, link])
            print('Нету почты')
