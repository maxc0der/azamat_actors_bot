import numpy as np
from random import randint
import cv2

print(cv2.__version__)
image = np.random.randint(255, size=(512, 512, 3))
random_number = randint(100000, 999999)
path = 'images/1_1.jpeg'
print(path)
val = cv2.imwrite(path, image)
print(val)

val = cv2.imwrite('images/1_2.jpeg', image[0:100, 0:100])
print(val)