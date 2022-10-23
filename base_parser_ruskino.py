"""
Парсер ruskino. Итерируемся по буквам алфавита, потом по номерам страниц.
Сохраняет в папку actors_ruskino_male/
"""

import requests
from bs4 import BeautifulSoup
import time
import string
from random import randint


def format_filename(s):
    alphabet_lower = "".join([chr(ord("а") + i) for i in range(32)])
    alphabet_upper = "".join([chr(ord("А") + i) for i in range(32)])
    alphabet = string.ascii_letters + alphabet_lower + alphabet_upper + string.digits + ' '
    filename = ''.join(c for c in s if c in alphabet)
#    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


domain = 'https://ruskino.ru/'
pages = range(1, 192)

for page in pages:
    print('Page: ', str(page))
    response = requests.get(domain + 'art/groups/actors?page=' + str(page))
    print(domain + 'art/groups/actresses?page=' + str(page))
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='iso_item_list_portrait_full')
    for quote in quotes:
        src = quote['style'].split('"')[1].strip()
        alt = quote.find('h4').text
        print(alt)
        loaded_image = requests.get(domain + src)
        path = "actors_ruskino_male/" + format_filename(alt) + '.jpg'
        out = open(path, "wb")
        out.write(loaded_image.content)
        time.sleep(0.25)
