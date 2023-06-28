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
    """
    This is the main function for getting the initial data for the further processing.
    It includes a couple of sub-functions needed to correctly get the data from the autoscout and otomoto websites,
    collect them and organize in the way in which they are available for the further processing.
    :return: car_parameters_autoscout24 - list of json files from autoscout,
             car_parameters_otomoto - list of dictionaries from otomoto,
             car_version - list of strings from autoscout,
             main image for each of the detailed offer.
    """
    image_counter = []

    # Code from this moment covers the scrapping of the autoscout webpage.

    soups = []
    announces = []
    urls = []
    car_parameters_autoscout24 = []

    def get_number_of_pages():
        """
        This function is checking how many pages of detailed offered are available at the moment.
        :return: Number of currently available subpages with detailed offers.
        """
        url = f'https://www.autoscout24.pl/lst/saab?atype=C&desc=0&page=1&search_id=11ap13gonil&sort=standard&source' \
              f'=listpage_pagination&ustate=N%2CU'
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        pages = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text())
        number_of_pages = int(pages['props']['pageProps']['numberOfPages'])
        return number_of_pages

    def initial_data(number_of_pages):
        """
        This function is the initial loader of the data. It takes the basic information from the main descriptions of
        the cars currently available in the announcements portal and prepares them for the further development. It
        requires user's input to provide the number of pages currently available.
        :param number_of_pages: number of pages with announces at the day of running the function.
        :return: list of html's codes (one entry per one announcement).
        """
        for page in range(1, number_of_pages + 1):
            url = f'https://www.autoscout24.pl/lst/saab?atype=C&desc=0&page={page}&search_id=11ap13gonil&sort=standard' \
                  f'&source=listpage_pagination&ustate=N%2CU'
            response = requests.get(url, proxies={'http': f"http://{random.choice(prox)}"})
            content = response.content
            soup = BeautifulSoup(content, 'html.parser')
            soups.append(soup)

    def get_detailed_urls():
        """
        This function is retrieving the url addresses for each detailed offer available.
        :return: List of urls.
        """
        for soup in range(0, len(soups)):
            announce = soups[soup].find_all('a', {
                'class': 'ListItem_title__znV2I ListItem_title_new_design__lYiAv Link_link__pjU1l'})
            announces.append(announce)
        for announce in announces:
            for element in range(0, len(announce)):
                url = announce[element]['href']
                urls.append(url)

    def get_detailed_offers(urls_list, i=0, img_count=0):
        """
        This function is passing by each url from the list of the detailed offers seeking for the information needed
        for the further processing.
        :param urls_list: list taken from the get_detailed_urls function.
        :param i: internal parameter for looping through the list. Default = 0.
        :param img_count: internal parameter used for saving the images with the numbers which are inline with
        the features of car taken from the announcement. Default = 0.
        :return: First image of each car.
                 List of features of each car.
        """
        for url in urls:
            try:
                new_url = 'https://www.autoscout24.pl' + urls[i]
                # detailed_content = requests.get(new_url, proxies={'http': f"http://{random.choice(prox)}"})
                detailed_content = requests.get(new_url)
                content = detailed_content.content
                soup = BeautifulSoup(content, 'html.parser')
                params = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text())
                params_val = params['offers']
                version = soup.find('div', {'class': "StageTitle_modelVersion__Rmzgd"}).get_text()
                params_val['version'] = version
                image = soup.find_all('source',
                                      {
                                          'media': '(max-width: 720px) and (-webkit-max-device-pixel-ratio: 1), (min-width: '
                                                   '481px) and (max-width: 719px) and (-webkit-min-device-pixel-ratio: '
                                                   '1.01), (min-width: 1024px)'})
                image_html = image[0]['srcset']
                # response_image = requests.get(image_html, proxies={'http': f"http://{random.choice(prox)}"})
                response_image = requests.get(image_html)
                image_content = response_image.content
                img = Image.open(BytesIO(image_content))
                img_name = f'image{img_count}.png'
                img_path = f'D:\Projekty Python\SAAB_Youngtimer_Detector\Images\{img_name}'
                img.save(img_path)
                params_val['id'] = img_count
                car_parameters_autoscout24.append(params_val)
                image_counter.append(img_count)
                img_count += 1
                i += 1
            except:
                i += 1
                img_count += 1


    initial_data(get_number_of_pages())
    get_detailed_urls()
    get_detailed_offers(urls, 0, img_count=0)

    # Code from this moment covers the scrapping of the otomoto website.

    soups_oto = []
    announces_oto = []
    urls_oto = []
    car_parameters_otomoto = []
    id_oto =[]

    def get_number_of_pages_oto():
        """
        This function is checking how many pages of detailed offered are available at the moment.
        :return: Number of currently available subpages with detailed offers.
        """
        url = f'https://www.otomoto.pl/osobowe/saab'
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        pages = soup.find_all('li', {'class': 'pagination-item ooa-1xgr17q'})
        number_of_pages_oto = int(pages[-1].get_text())
        return number_of_pages_oto

    def initial_data_oto(number_of_pages):
        """
        This function is the initial loader of the data. It takes the basic information from the main descriptions of
        the cars currently available in the announcements portal and prepares them for the further development. It
        requires user's input to provide the number of pages currently available.
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
        """
        This function is checking the current class code for the offers as the class code has tendencies to change.
        :return: Class code currently used at the otomoto website.
        """
        sample = soups_oto[0].find('h2')['class']
        a = sample[0] + ' ' + sample[1] + ' ' + sample[2] + ' ' + sample[3]
        return a

    def get_detailed_urls_oto(class_code):
        """
        This function is retrieving the url addresses for each detailed offer available.
        :return: List of urls.
        """
        for soup in range(0, len(soups_oto)):
            announce = soups_oto[soup].find_all('h2', {'class': class_code})
            announces_oto.append(announce)
        for announce in announces_oto:
            for element in range(0, len(announce)):
                url = announce[element].find('a')['href']
                urls_oto.append(url)

    def get_detailed_offers(urls_list, i=0, img_count=0):
        """
        This function is passing by each url from the list of the detailed offers seeking for the information needed
        for the further processing.
        :param urls_list: list taken from the get_detailed_urls function.
        :param i: internal parameter for looping through the list. Default = 0.
        :param img_count: internal parameter used for saving the images with the numbers which are inline with
        the features of car taken from the announcement. Default = 0.
        :return: First image of each car.
                 List of features of each car.
        """
        main_keys = ['Rok', 'Przebieg_add', 'Paliwo', 'Typ_nadwozia_add']
        for url in urls:
            try:
                new_url = urls_oto[i]
                # detailed_content = requests.get(new_url, proxies={'http': f"http://{random.choice(prox)}"})
                detailed_content = requests.get(new_url)
                content = detailed_content.content
                soup = BeautifulSoup(content, 'html.parser')
                params_val = soup.find_all('li', {'class': 'offer-params__item'})
                main_val = soup.find_all('span', {'class': 'offer-main-params__item'})
                offer = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text())
                price = offer['offers']
                image = soup.find_all('img', {'class': 'bigImage'})
                a = image[0]['data-lazy']
                get_image = a
                # response_image = requests.get(get_image, proxies={'http': f"http://{random.choice(prox2)}"})
                response_image = requests.get(get_image)
                image_content = response_image.content
                img = Image.open(BytesIO(image_content))
                img_name = f'image{img_count}.png'
                img_path = f'D:\Projekty Python\SAAB_Youngtimer_Detector\Images\{img_name}'
                img.save(img_path)
                ida = img_count
                img_count += 1
                new_car_param = {}
                keys = []
                features = []
                for par in params_val:
                    item = par.get_text()
                    item = item.split(sep='\n')
                    feature_1 = item[1]
                    if item[3] == '':
                        feature_2 = item[4]
                        feature_1 = feature_1.strip()
                        feature_2 = feature_2.strip()
                    else:
                        feature_2 = item[3]
                        feature_1 = feature_1.strip()
                        feature_2 = feature_2.strip()
                    keys.append(feature_1)
                    features.append(feature_2)
                for k in range(len(keys)):
                    new_car_param[keys[k]] = features[k]
                value = price['price']
                curr = price['priceCurrency']
                new_car_param['price'] = value
                new_car_param['currency'] = curr
                for par in range(0, 4):
                    item = main_val[par].get_text().strip()
                    new_car_param[main_keys[par]] = item
                car_parameters_otomoto.append(new_car_param)
                id_oto.append(ida)
                ida += 1
                i += 1
            except:
                i += 1
                img_count += 1

    image_counter_oto = (image_counter[len(image_counter)-1])+1
    initial_data_oto(get_number_of_pages_oto())
    get_example()
    get_detailed_urls_oto(get_example())
    get_detailed_offers(urls_oto, i=0, img_count=image_counter_oto)

    return car_parameters_autoscout24, car_parameters_otomoto, id_oto


