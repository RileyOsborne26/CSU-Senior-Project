import numpy as np
import pytesseract
import cv2
# Code -- source: https://www.projectpro.io/article/how-to-train-tesseract-ocr-python/561
# Tips on accuracy improvement -- source: https://github.com/tesseract-ocr/tessdoc/tree/main/tess5

# get grayscale image
def convert_grayscale(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

# noise removal
def blur(img, param):
    img = cv2.medianBlur(img, param)
    return img

# thresholding
def threshold(img):
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img

# MAKE SURE the path is to the correct location with the pytesseract executable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# for config help, type "tesseract --help-oem" and "tesseract --help-psm"
# PSMs not working: [0, 2]
# PSMs work best: [11, 12, 1, 3, 4, 6]
config = r'--oem 1 --psm 6'

# the test-images folder is used so subdirectory maps to the image requested.
subdirectory = "test-images/"
file = subdirectory + input('Enter file name: ')
img = cv2.imread(file)

gray = convert_grayscale(img)
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharp = cv2.filter2D(gray, -1, kernel)

# fetch image shape
h, w, c = img.shape

# obtain boxes 
boxes = pytesseract.image_to_boxes(img)

# for loop to draw rectangles on detected boxes
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

#display image
#cv2.imshow('img', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# to clarift english add ", lang='eng'" to the command
text = pytesseract.image_to_string(sharp, config=config)

## testing psm configs
print("\nPSM: 6")
print(text) 

#config = r'--oem 1 --psm 0'
#text = pytesseract.image_to_string(sharp, config=config)
#print("\nPSM: 0")
#print(text) 

config = r'--oem 1 --psm 1'
text = pytesseract.image_to_string(sharp, config=config)
print("\nPSM: 1")
print(text)  

config = r'--oem 1 --psm 3'
text = pytesseract.image_to_string(sharp, config=config)
print("\nPSM: 3")
print(text) 

config = r'--oem 1 --psm 4'
text = pytesseract.image_to_string(sharp, config=config)
print("\nPSM: 4")
print(text) 

config = r'--oem 1 --psm 11'
text = pytesseract.image_to_string(sharp, config=config)
print("\nPSM: 11")
print(text) 

config = r'--oem 1 --psm 12'
text = pytesseract.image_to_string(sharp, config=config)
print("\nPSM: 12")
print(text) 