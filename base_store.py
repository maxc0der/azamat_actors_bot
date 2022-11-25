"""
Скрипт для распознавания лиц и записи в базу
в переменную path - путь к папке (15 строка)
в переменную ext - расширение изображений в папке (16 строка)
"""

import requests
from bs4 import BeautifulSoup
import time
import string
import os
import shutil
from dface import *

path = 'actors_ruskino_male/'
ext = '.jpg'

if os.path.exists(path):
    image_files = [os.path.join(path, img) for img in os.listdir(path) if img.endswith(ext)]
    image_files.sort(key=lambda s: s.partition('/')[-1])

print(str(len(image_files)))

i = 0
for img in image_files:
    start_time = time.time()
    i = i + 1
    print(str(i) + ' / ' + str(len(image_files)))
    print(img)
    shutil.copyfile(img, 'buffer.png')
    faces = get_faces('buffer.png')
    if len(faces) > 0:
        print('Count: ', str(len(faces)))
        print(img.partition('/')[-1].partition('.')[0])
        store_face(file_name='buffer.png', db_file_name=img, caption=img.partition('/')[-1].partition('.')[0])
        store_yo(file_name='buffer.png', db_file_name=img)
    print('Time left: ', str(time.time() - start_time))
