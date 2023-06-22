import requests
from bs4 import BeautifulSoup
import json
from io import BytesIO
from PIL import Image
import random

with open('http_prox.txt', 'r') as file:
    prox = file.readlines()

with open('http_prox_2.txt', 'r') as file_1:
    prox2 = file_1.readlines()


def get_initial_load():
    image_counter = 0

    soups = []
    announces = []
    urls = []
    car_parameters_main = []
    missing_offers = []

    def get_number_of_pages():
        url = f'https://www.autoscout24.pl/lst/saab?atype=C&desc=0&page=1&search_id=11ap13gonil&sort=standard&source' \
              f'=listpage_pagination&ustate=N%2CU'
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        pages = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text())
        number_of_pages = int(pages['props']['pageProps']['numberOfPages'])
        return number_of_pages

    def initial_data(number_of_pages):
        '''
     This function is the initial loader of the data. It takes the basic information from the main descriptions of the cars
     currently available in the announcements portal and prepares them for the further development. It requires user's input
     to provide the number of pages currently available.
     :param number_of_pages: number of pages with announces at the day of running the function.
     :return: list of html's codes (one entry per one announcement).
     '''
        for page in range(1, number_of_pages + 1):
            url = f'https://www.autoscout24.pl/lst/saab?atype=C&desc=0&page={page}&search_id=11ap13gonil&sort=standard' \
                  f'&source=listpage_pagination&ustate=N%2CU'
            response = requests.get(url, proxies={'http': f"http://{random.choice(prox)}"})
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            soups.append(soup)

    def get_detailed_urls():
        for soup in range(0, len(soups)):
            announce = soups[soup].find_all('a', {
                'class': 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l'})
            announces.append(announce)
        for announce in announces:
            for element in range(0, len(announce)):
                url = announce[element]['href']
                urls.append(url)

    def get_detailed_offers(urls_list, i=0, img_count=0):
        for url in urls:
            try:
                new_url = 'https://www.autoscout24.pl' + urls[i]
                detailed_content = requests.get(new_url, proxies={'http': f"http://{random.choice(prox)}"})
                content = detailed_content.content
                soup = BeautifulSoup(content, 'html.parser')
                params = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text())
                params_val = params['offers']
                image = soup.find_all('source',
                                      {
                                          'media': '(max-width: 720px) and (-webkit-max-device-pixel-ratio: 1), (min-width: '
                                                   '481px) and (max-width: 719px) and (-webkit-min-device-pixel-ratio: '
                                                   '1.01), (min-width: 1024px)'})
                image_html = image[0]['srcset']
                response_image = requests.get(image_html, proxies={'http': f"http://{random.choice(prox)}"})
                image_content = response_image.content
                img = Image.open(BytesIO(image_content))
                img_name = f'image{img_count}.png'
                img_path = f'D:\Projekty Python\SAAB_Youngtimer_Detector\Images\{img_name}'
                img.save(img_path)
                car_parameters_main.append(params_val)
                img_count += 1
                i += 1
            except:
                missing_offers.append(i)
                i += 1

    initial_data(get_number_of_pages())

    get_detailed_urls()

    get_detailed_offers(urls, 0, img_count=image_counter)

    soups_oto = []
    announces_oto = []
    urls_oto = []
    car_parameters_detailed_oto = []
    car_parameters_main_oto = []
    missing_offers_oto = []

    def get_number_of_pages_oto():
        url = f'https://www.otomoto.pl/osobowe/saab'
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        pages = soup.find_all('li', {'class': 'pagination-item ooa-1xgr17q'})
        number_of_pages_oto = int(pages[-1].get_text())
        return number_of_pages_oto

    def initial_data_oto(number_of_pages):
        """
     This function is the initial loader of the data. It takes the basic information from the main descriptions of the cars
     currently available in the announcements portal and prepares them for the further development. It requires user's input
     to provide the number of pages currently available.
     :param number_of_pages: number of pages with announces at the day of running the function.
     :return: list of html's codes (one entry per one announcement).
     """
        for page in range(1, number_of_pages + 1):
            url = f'https://www.otomoto.pl/osobowe/saab?page={page}'
            response = requests.get(url, proxies={'http': f"http://{random.choice(prox)}"})
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            soups_oto.append(soup)

    def get_example():
        sample = soups_oto[0].find('h2')['class']
        a = sample[0] + ' ' + sample[1] + ' ' + sample[2] + ' ' + sample[3]
        return a

    def get_detailed_urls_oto(class_code):
        for soup in range(0, len(soups_oto)):
            announce = soups_oto[soup].find_all('h2', {'class': class_code})
            announces_oto.append(announce)
        for announce in announces_oto:
            for element in range(0, len(announce)):
                url = announce[element].find('a')['href']
                urls_oto.append(url)

    def get_detailed_offers(urls_list, i=0, j=0, img_count=0):
        main_keys = ['Rok', 'Przebieg', 'Paliwo', 'Typ_nadwozia']
        for url in urls:
            try:
                new_url = urls_oto[i]
                detailed_content = requests.get(new_url, proxies={'http': f"http://{random.choice(prox)}"})
                content = detailed_content.content
                soup = BeautifulSoup(content, 'html.parser')
                params_val = soup.find_all('li', {'class': 'offer-params__item'})
                main_val = soup.find_all('span', {'class': 'offer-main-params__item'})
                image = soup.find_all('img', {'class': 'bigImage'})
                a = image[0]['data-lazy']
                get_image = a
                response_image = requests.get(get_image, proxies={'http': f"http://{random.choice(prox2)}"})
                image_content = response_image.content
                img = Image.open(BytesIO(image_content))
                img_name = f'image{img_count}.png'
                img_path = f'D:\Projekty Python\SAAB_Youngtimer_Detector\Images\{img_name}'
                img.save(img_path)
                img_count += 1
                new_car_param = {}
                new_car_main = {}
                keys = []
                features = []
                main_features = []
                for par in params_val:
                    item = params_val[j].get_text()
                    item = item.split(sep='\n')
                    feature_1 = item[1]
                    if item[3] == '':
                        featrue_2 = item[4]
                    else:
                        featrue_2 = item[3]
                        feature_1 = feature_1.strip()
                        featrue_2 = featrue_2.strip()
                        keys.append(feature_1)
                        features.append(featrue_2)
                        j += 1
                for k in range(len(keys)):
                    new_car_param[keys[k]] = features[k]
                car_parameters_detailed_oto.append(new_car_param)
                for par in range(0, 4):
                    item = main_val[par].get_text().strip()
                    feature = item
                    main_features.append(feature)
                for k in range(len(main_keys)):
                    new_car_main[main_keys[k]] = main_features[k]
                car_parameters_main_oto.append(new_car_main)
                i += 1
                j = 0
            except:
                missing_offers_oto.append(i)
                i += 1

    initial_data_oto(get_number_of_pages_oto())

    get_example()

    get_detailed_urls_oto(get_example())

    get_detailed_offers(urls_oto, i=0, j=0, img_count=len(car_parameters_main))

    return car_parameters_main, car_parameters_detailed_oto, car_parameters_main_oto
