"""
Парсер kinoteatr. Итерируемся по буквам алфавита, потом по номерам страниц.
Сохраняет в папку "actors_ru/"
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
    print(alphabet)
    filename = ''.join(c for c in s if c in alphabet)
#    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


domain = 'https://www.kino-teatr.ru/'
letters = ['a', 'b', 'v', 'g', 'd', 'e', 'j', 'z', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'c', 'cz', 'sh', 'sch', 'ye', 'yu', 'ya']

for letter in letters:
    letter_url = 'https://www.kino-teatr.ru/kino/acter/all/ros/' + letter + '/'
    response = requests.get(letter_url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = set()
    links.add(letter_url)

    quotes = soup.find(class_='page_numbers')
    if quotes is not None:
        quotes = quotes.find_all('a')
        for q in quotes:
            print(q['href'])
            links.add(domain + q['href'])

    print('Count for ' + letter + ': ' + str(len(links)))

    for url in links:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('img', class_='list_item_img')

        for quote in quotes:
            print(quote['src'])
            print(quote['alt'])

            loaded_image = requests.get(domain + quote['src'])
            path = "actors_ru/" + format_filename(quote['alt']) + '.jpg'
            out = open(path, "wb")
            out.write(loaded_image.content)
            time.sleep(0.15)
