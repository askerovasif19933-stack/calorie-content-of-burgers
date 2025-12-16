import random
from re import I
from time import sleep

import requests

from bs4 import BeautifulSoup
import json

from src.logger import get_logger

logger = get_logger(__name__)


headers = {
    'accept': '*/*',
    'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36'
}


def parse_int(headers):
    """Парсер сайта vkusnoitochka.ru для получения данных о бургерах и их калорийности."""

    with open('page.json', 'r', encoding='utf-8') as file:
        src = json.load(file)


    result_dict = {}

    for name, url in src.items():
        req = requests.get(url, headers)
        src_page = req.text

        soup = BeautifulSoup(src_page, 'lxml')

        all_product_hrefs = soup.find_all(class_='text-decoration-none')
        all_categories_dict = {}
        for i in all_product_hrefs:
            item_text = i.text.strip('\n')
            item_href = i.get('href')
            all_categories_dict[item_text] = item_href
            sleep(random.randint(2, 3))
        logger.info(f'{len(all_categories_dict)} обьектов')




        for text, href in all_categories_dict.items():
            name_burger = text
            req = requests.get(href, headers)
            src_burger = req.text
            soup = BeautifulSoup(src_burger, 'lxml')
            image_src = soup.find(class_='img-responsive')
            img = image_src.get('src')
    
            mass = soup.find(class_="list-unstyled").find('li').find('strong').text
            mass = mass.split()[0]
            result_dict[name_burger] = {}
            result_dict[name_burger]['image'] = img
            result_dict[name_burger]['масса'] = mass
            logger.info(name_burger, mass, f'фото {img}')


            tabl_calories = soup.find(class_="table table-bordered").find_all('td')
            for k, v in zip(tabl_calories[0::2], tabl_calories[1::2]):
                result_dict[name_burger][k.text] = v.text.split()[0]
                logger.info(k, v)

   
        sleep(random.randint(2, 3))

    with open('vkusno_tochka_burger.json', 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    parse_int(headers)













