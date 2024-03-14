import easyocr
import matplotlib.pyplot as plt
import cv2
import numpy as np
from easyocr import detection
import pytesseract

# Uses x,y,w,h coordinates to create a cropped image. 
# The arguments are an image and array of coordinates, respectively
# array in form [x,y,w,h]
def coordinates_to_image(image, array):
    # crop is in form [y:y+h, x:x+w]
    new_image = image[(array[1]):(array[1]+array[3]), (array[0]):(array[0]+array[2])]
    
    return new_image


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
count = 0

# the index for each will be parallel so index[0] for all arrays gets the confidence, box, and word
text_boxes = []
words = []
confidence_level = []

# x:y is the top left corner of the rectangle
# W = res[i][1][0] - res[i][0][0]
# H = res[i][2][1] - res[i][0][1]
# coordinates array is [x,y,w,h]
for res in result:
    text += res[1] + ","

    for i in range ( len(res) ):
        # add the word to the words array
        if i % 3 == 1:
            words.append(res[i])

        # add the confidence level in the appropriate array
        if i % 3 == 2:
            confidence_level.append(res[i])

        # prints bounding boxes coordinates and adds them to an array
        if i % 3 == 0:
            # Create an array with all components for a bounding box and append to text_boxes
            bounding_box = [res[i][0][0], res[i][0][1], (res[i][1][0] - res[i][0][0]), (res[i][2][1] - res[i][0][1])]
            text_boxes.append(bounding_box)
            print(res[i][0])
            print(res[i][1])
            print(res[i][2])
            print(res[i][3])
        else:
            print(res[i])
        print(count)
        count = count + 1

# print the results
for i in range ( len(words) ):
    print("Bounding Box #" + str(i) + ": ")
    print(text_boxes[i])
    print("Word #" + str(i) + ": ")
    print(words[i])
    print("Confidence Level #" + str(i) + ": ")
    print(confidence_level[i])
    print('\n')

# cropping images using bounding boxes and retrying them individually with the reader
cropped_images = []

for i in range ( len(words) ):
    cropped_images.append(coordinates_to_image(img, text_boxes[i]))

    # show all of the cropped images
    cv2.imshow("Text Detection", cropped_images[i])
    cv2.waitKey(0)

    # run pytesseract if confidence level is under 0.9

    result = reader.readtext(cropped_images[i])
    for res in result:
        print(res)


f = open("foundTextTest#1.csv", "a")
f.write(text + "\n")
f.close()

text2 = '\n'.join([res[1] for res in result])
print(text2)