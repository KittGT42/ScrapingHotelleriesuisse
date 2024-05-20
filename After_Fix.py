import csv

from bs4 import BeautifulSoup
import requests


headers_csv = [ 'Branche', 'Company_Name', 'Adresse', 'PLZ', 'Ort', 'Land', 'Telefon', 'Email', 'Website',
               'Anrede', 'Vorname', 'Name', 'Title','Mitglied',
               'Facebook', 'Twitter', 'Youtube', 'Linkedin', 'Instagram', 'Company Description']
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
}
with open('persoenlich_after_fix.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers_csv)

default_url = 'https://www.persoenlich.com'
response = requests.get('https://www.persoenlich.com/marktplatz', headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
last_page_number = soup.find('span', class_='last').find('a').get('href').split('=')[-1]
counter = 1
for i in range(1, int(last_page_number) + 1):
    print(f'Dowloand {i}/{last_page_number}')
    response = requests.get(f'https://www.persoenlich.com/marktplatz?page={i}', headers=headers)
    soup_company = BeautifulSoup(response.text, 'lxml')
    all_companies_name = soup_company.find_all('li', class_='col-xs-12 pl0 pr0 mb20')
    for company in all_companies_name:
        Branche = company.find('div', class_='firmasubareatext').text.strip()
        try:
            Mitglied = company.find('div', style='margin-bottom:22px').find('a').get('href').split('www')[-1].split('/')[0][1:]
        except Exception:
            Mitglied = ''
        try:
            Company_Description = company.find('div', class_='col-md-12 pl5 mb10').find('p').text.strip()
        except Exception:
            Company_Description = ''
        try:
            url_company = default_url + company.find('a').get('href')
        except Exception:
            url_company = default_url + company.find('a').get('href')

        response_company = requests.get(url_company, headers=headers)
        soup_company = BeautifulSoup(response_company.text, 'lxml')
        try:
            Company_Name = soup_company.find('div', class_='companynamebold').text.strip()
        except Exception:
            try:
                Company_Name = soup_company.find('h2', class_='company').find('a').text.strip()
            except Exception:
                Company_Name = ''
        try:
            Adresse = str(soup_company.find_all('div', class_='pull-left')[3].find('a').contents[0])
            if Adresse == '<br/>':
                Adresse = ''
        except Exception:
            Adresse = ''
        try:
            if Adresse == '':
                try:
                    PLZ = soup_company.find_all('div', class_='pull-left')[3].find('a').contents[1].split(' ')[0]
                except Exception:
                    PLZ = ''
            else:
                PLZ = soup_company.find_all('div', class_='pull-left')[3].find('a').contents[2].split(' ')[0]
        except Exception:
            PLZ = ''
        try:
            if Adresse == '':
                try:
                    Ort = soup_company.find_all('div', class_='pull-left')[3].find('a').contents[1].split(' ')[1]
                except Exception:
                    Ort = ''
            else:
                Ort = str(soup_company.find_all('div', class_='pull-left')[3].find('a').contents[2].split(' ')[1])
                if Ort == 'St.':
                    Ort = ''.join(
                        soup_company.find_all('div', class_='pull-left')[3].find('a').contents[2].split(' ')[1:3])
        except Exception:
            Ort = ''
        try:
            if Adresse == '':
                try:
                    Land = soup_company.find_all('div', class_='pull-left')[3].find('a').contents[3]
                except Exception:
                    Land = ''
            else:
                Land = soup_company.find_all('div', class_='pull-left')[3].find('a').contents[4]
        except Exception:
            Land = ''
        try:
            Telefon = soup_company.find('i', class_='fa fa-phone fa-fw').parent.text.strip()
        except Exception:
            Telefon = ''
        try:
            Email = soup_company.find('i', class_='fa fa-envelope fa-fw').parent.text.strip()
            if Email == 'Kontaktformular Website':
                Email = ''
        except Exception:
            Email = ''
        try:
            Website = soup_company.find('i', class_='fa fa-globe fa-fw').parent.find('a').text.strip()
            if Email != '' and '@' in Email:
                Website = Email.split('@')[1]
        except Exception:
            if Email != '' and '@' in Email:
                Website = Email.split('@')[1]
            else:
                Website = ''
        try:
            Anrede = str(soup_company.find('div', style='margin-top: 8px;').contents[2].text.strip().split(' ')[0])
            if Anrede == 'Herr':
                Anrede = 'Mr.'
            elif Anrede == 'Frau':
                Anrede = 'Ms.'
            else:
                Anrede = ''
        except Exception:
            Anrede = ''
        try:
            Vorname = soup_company.find('div', style='margin-top: 8px;').contents[2].text.strip().split(' ')[-2]
        except Exception:
            Vorname = ''
        try:
            if ',' in soup_company.find('div', style='margin-top: 8px;').contents[2].text.strip():
                Name = \
                soup_company.find('div', style='margin-top: 8px;').contents[2].text.strip().split(',')[0].split(' ')[1]
            else:
                Name = soup_company.find('div', style='margin-top: 8px;').contents[2].text.strip().split(' ')[-1]
        except Exception:
            Name = ''
        try:
            if soup_company.find('div', style='margin-top: 8px;').contents[5].text.strip():
                Title = soup_company.find('div', style='margin-top: 8px;').contents[5].text.strip()
            elif soup_company.find('i', class_='fa fa-user fa-fw').contents[5].text.strip():
                Title = soup_company.find('i', class_='fa fa-user fa-fw').contents[5].text.strip()
        except Exception:
            Title = ''
        try:
            all_social_media = soup_company.find('p',
                                                 style="font-size: 22px; text-align: left;margin:20px 0 0 0;").find_all(
                'a')
            Facebook = ''
            Twitter = ''
            Youtube = ''
            Linkedin = ''
            Instagram = ''
            for social_media in all_social_media:
                if 'facebook' in social_media.get('href'):
                    Facebook = social_media.get('href')
                elif 'twitter' in social_media.get('href'):
                    Twitter = social_media.get('href')
                elif 'youtube' in social_media.get('href'):
                    Youtube = social_media.get('href')
                elif 'linkedin' in social_media.get('href'):
                    Linkedin = social_media.get('href')
                elif 'instagram' in social_media.get('href'):
                    try:
                        Instagram = social_media.get('href')
                    except Exception:
                        Instagram = ''
        except Exception:
            Facebook = ''
            Twitter = ''
            Youtube = ''
            Linkedin = ''
            Instagram = ''
        with open('persoenlich_after_fix.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(
                [Branche, Company_Name, Adresse, PLZ, Ort, Land, Telefon, Email, Website, Anrede, Vorname, Name,
                 Title, Mitglied, Facebook, Twitter, Youtube, Linkedin, Instagram, Company_Description,
                 url_company])
            print(f'Succsesfully saved {Company_Name}')




