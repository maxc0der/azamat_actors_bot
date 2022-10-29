import numpy as np
from random import randint
import cv2
import os

print(cv2.__version__)
image = np.random.randint(255, size=(512, 512, 3))
random_number = randint(100000, 999999)

file_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(file_path, 'images/1_1.jpeg')
print(path)
val = cv2.imwrite(path, image)
print(val)

