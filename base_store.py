import requests
from bs4 import BeautifulSoup
import time
import string
import os
import shutil
from dface import *


if os.path.exists('actors_ru/'):
    image_files = [os.path.join('actors_ru/', img) for img in os.listdir('actors_ru/') if img.endswith(".jpg")]
    image_files.sort(key=lambda s: s.partition('/')[-1])

print(str(len(image_files)))

i = 0
for img in image_files:
# Рамиль Азимов
#    if img < 'actors/Хорхе Лендеборгмл.jpg':
 #   if img < 'actors_ru/Сергей Алексеев IV.jpg':
#        i = i + 1
#        continue
    start_time = time.time()
    i = i + 1
    print(str(i) + ' / ' + str(len(image_files)))
    print(img)
    shutil.copyfile(img, 'buffer.png')
    #faces = get_faces('buffer.png')
    #if len(faces) > 0:
        #print('Count: ', str(len(faces)))
        #print(img.partition('/')[-1].partition('.')[0])
        #store_face(file_name='buffer.png', db_file_name=img, caption=img.partition('/')[-1].partition('.')[0])
    store_yo(file_name='buffer.png', db_file_name=img)
    print('Time left: ', str(time.time() - start_time))
