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
pages = range(108, 152)

for page in pages:
    print('Page: ', str(page))
    response = requests.get(domain + 'art/groups/actresses?page=' + str(page))
    print(domain + 'art/groups/actresses?page=' + str(page))
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', class_='iso_item_list_portrait_full')
    for quote in quotes:
        src = quote['style'].split('"')[1].strip()
        alt = quote.find('h4').text
        print(alt)
        loaded_image = requests.get(domain + src)
        path = "actors_ruskino_female/" + format_filename(alt) + '.jpg'
        out = open(path, "wb")
        out.write(loaded_image.content)
        time.sleep(0.15)

"""
#   faces = get_faces(path)
#    if len(faces) > 0:
#        print('Count: ', str(len(faces)))
#       store_face(file_name=path, caption=quote['alt'])
"""