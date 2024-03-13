import easyocr
import matplotlib.pyplot as plt
import cv2
import numpy as np
from easyocr import detection


reader = easyocr.Reader(['en'], gpu=False)
detection.CRAFT

# the test-images folder is used so subdirectory maps to the image requested.
subdirectory = "test-images/"
file = subdirectory + input('Enter file name for card front image: ')
img = cv2.imread(file)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharp = cv2.filter2D(gray, -1, kernel)

result = reader.readtext(img)

text = ""

for res in result:
    text += res[1] + ","
    for i in range ( len(res) ):
        print(res[i])

f = open("foundTextTest#1.csv", "a")
f.write(text + "\n")
f.close()

text2 = '\n'.join([res[1] for res in result])
print(text2)