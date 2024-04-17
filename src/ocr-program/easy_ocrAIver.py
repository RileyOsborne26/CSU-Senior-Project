import easyocr
import matplotlib.pyplot as plt
import cv2
import numpy as np
from easyocr import detection
import pytesseract
import time

# Uses x,y,w,h coordinates to create a cropped image. 
# The arguments are an image and array of coordinates, respectively
# array in form [x,y,w,h]
def coordinates_to_image(image, array):
    # crop is in form [y:y+h, x:x+w], round is to erase an error type where float is used for some reason
    new_image = image[round((array[1])):round((array[1]+array[3])), round((array[0])):round((array[0]+array[2]))]
    
    return new_image

# calls the easyocr reader to find and return the OCR results for the image parameter (2nd) given.
# a blacklist is passed as an argument.
def easyocr_get_results(reader, img, blacklist_pattern):
    # blacklist certain characters
    blacklist_special = ['\{}'.format(c) for c in '|[{]}']
    additional_characters = ['\\']

    # Combine special and additional characters then join into a single string
    all_characters = blacklist_special + additional_characters
    blacklist_pattern = ''.join(all_characters)
    #print(blacklist_pattern)

    result = reader.readtext(img, blocklist=blacklist_pattern)

    return result

# This function takes an OCR results array, an array of text bounding boxes,
# an array of words found, an array of OCR confidence levels, and a string for image text.
# returns text
def add_OCRdata_to_arrays(result, text_boxes, words, confidence_level, text):
    # x:y is the top left corner of the rectangle
    # W = res[i][1][0] - res[i][0][0]
    # H = res[i][2][1] - res[i][0][1]
    # coordinates array is [x,y,w,h]
    for res in result:
        # add to text string
        text += res[1] + ","

        # adds each element to its array
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

    return text

# Takes the three arrays with the OCR results and prints them to the screen
def print_OCRresults(text_boxes, words, confidence_level):
    # print the results
    for i in range ( len(words) ):
        print("Bounding Box #" + str(i) + ": ")
        print(text_boxes[i])
        print("Word #" + str(i) + ": ")
        print(words[i])
        print("Confidence Level #" + str(i) + ": ")
        print(confidence_level[i])
        print('\n')

# Crops the images based off of EasyOCR's results, runs pytesseract on the cropped images,
# displays the cropped images, and prints the pytesseract OCR results. Also re-runs easyocr on
# the CROPPED version of the image and displays those results as well.
def pytesseract_crop_and_display(reader, img, cropped_images, text_boxes, words):   
    # declare the timing variables as global to solve to issue of them not changing after the function completes
    global time_cropped_easyocr, time_cropped_pytesseract 
    
    # uses the words array to iterate through the found text
    for i in range ( len(words) ):
        # crops the images using the well set up bounding box coordinates stored in an array for each instance of text.
        cropped_images.append(coordinates_to_image(img, text_boxes[i]))

        # show all of the cropped images, if any have an error displaying the program will no longer crash!
        try:
            cv2.imshow("Text Detection #" + str(i), cropped_images[i])
            cv2.waitKey(0)
        except cv2.error as e:
            print("OpenCV Error:", e)
            continue     # because it is a cropped image problem, the rest will not work.

        # run pytesseract if confidence level is under 0.9
        # MAKE SURE the path is to the correct location with the pytesseract executable
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

        # create uniform flags to add like blacklists and whitelists
        addFlags = r'--blacklist \|[{]}'

        ### for config help, type "tesseract --help-oem" and "tesseract --help-psm"
        ### to read an article about the psm settings, my source for the comments provided is:
        ### https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/
        ### PSMs without a generally applicable use for the project: [0, 1, 2, 9]
        # PSM 6: The text is treated as having a single font face with no variation. Good for single,
        #      consistent font and for materials like simple book pages.
        config = r'-l eng --oem 1 --psm 6'
        config += addFlags #add extra flags
        pytesseract_time_start = time.time()    # start the time
        text = pytesseract.image_to_string(cropped_images[i], config=config)
        ## testing psm configs
        print("\nPSM: 6")
        print(text) 

        # PSM 7: is for a single line of UNIFORM text. A good use case is license plates.
        config = r'-l eng --oem 1 --psm 7'
        config += addFlags #add extra flags
        text = pytesseract.image_to_string(cropped_images[i], config=config)
        ## testing psm configs
        print("\nPSM: 7")
        print(text) 

        # PSM 13: throws OCD, segmentation, and tesseract preprocessing out the window. Useful for when
        #      those things HURT the accuracy, the crop is too close, or the font is unrecognized.
        #      Using PSM 13 is seen as a last resort tactic.
        config = r'-l eng --oem 1 --psm 13'
        config += addFlags #add extra flags
        text = pytesseract.image_to_string(cropped_images[i], config=config)
        pytesseract_time_end = time.time()    # end the time

        # add the time to the pytesseract ocr total time
        pytesseract_elapsed = pytesseract_time_end - pytesseract_time_start
        time_cropped_pytesseract = time_cropped_pytesseract + pytesseract_elapsed

        ## testing psm configs
        print("\nPSM: 13")
        print(text)

        
        # re-run EasyOCR with the cropped images.
        crop_easyocr_start = time.time()    # start easyOCR time
        result = reader.readtext(cropped_images[i])
        crop_easyocr_end = time.time()    # end easyOCR time

        #add the timing to total cropped easyOCR time
        crop_easyocr_elapsed = crop_easyocr_end - crop_easyocr_start
        time_cropped_easyocr = time_cropped_easyocr + crop_easyocr_elapsed
        print("time pytesseract: " + str(pytesseract_elapsed))
        print("time easyOCR: " + str(crop_easyocr_elapsed))
        for res in result:
            print(res)

# first option has no gpu and the second option has gpu. Create the blacklist here too
blacklist_special = ['\{}'.format(c) for c in '|[{]}']
additional_characters = ['\\']

# Combine special and additional characters then join into a single string
all_characters = blacklist_special + additional_characters
blacklist_pattern = ''.join(all_characters)
#print(blacklist_pattern)

reader = easyocr.Reader(['en'], gpu=False)
#reader = easyocr.Reader(['en'], gpu=True)
detection.CRAFT

# the test-images folder is used so subdirectory maps to the image requested.
subdirectory = "test-images/"
fileF = subdirectory + input('Enter file name for card FRONT image: ')
imgF = cv2.imread(fileF)

# this image is for the back of the card.
#fileB = subdirectory + input('Enter file name for card BACK image: ')
#imgB = cv2.imread(fileB)

gray = cv2.cvtColor(imgF, cv2.COLOR_BGR2GRAY)

kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharp = cv2.filter2D(gray, -1, kernel)

# create all the timing variables and start timer
time_cropped_easyocr = 0
time_cropped_pytesseract = 0
start_time = time.time()

# call function to get results for the image front and back
resultFront = easyocr_get_results(reader, imgF, blacklist_pattern)
#resultBack = easyocr_get_results(reader, imgB, blacklist_pattern)

# end timer
end_time = time.time()
elapsed_time = end_time - start_time

### These are the variables for the FRONT of the image
F_text = ""

# the index for each will be parallel so index[0] for all arrays gets the confidence, box, and word
F_text_boxes = []
F_words = []
F_confidence_level = []

### These are the variables for the BACK of the image
B_text = ""

# the index for each will be parallel so index[0] for all arrays gets the confidence, box, and word
B_text_boxes = []
B_words = []
B_confidence_level = []


# Gather OCR data into arrays for FRONT and BACK
F_text = add_OCRdata_to_arrays(resultFront, F_text_boxes, F_words, F_confidence_level, F_text)
#B_text = add_OCRdata_to_arrays(resultBack, B_text_boxes, B_words, B_confidence_level, B_text)

# Print OCR results from the 3 separate arrays with parallel indexes for FRONT and BACK of card
print_OCRresults(F_text_boxes, F_words, F_confidence_level)
#print_OCRresults(B_text_boxes, B_words, B_confidence_level)

# cropping images using bounding boxes and retrying them individually with the reader
F_cropped_images = []
#B_cropped_images = []

# run the function that crops, displays, runs pytesseract, and re-runs EasyOCR for FRONT and BACK
pytesseract_crop_and_display(reader, imgF, F_cropped_images, F_text_boxes, F_words)
#pytesseract_crop_and_display(reader, imgB, B_cropped_images, B_text_boxes, B_words)

# print times
print("time to complete easyOCR for WHOLE image: " + str(elapsed_time))
print("time to complete easyOCR for CROPPED images: " + str(time_cropped_easyocr))
print("time to complete pytesseract for CROPPED images: " + str(time_cropped_pytesseract) + "\n")

# saves words found to a CSV file
f = open("foundTextTest#1.csv", "a")
f.write(F_text + "\n")
f.close()

# reprints the words found again
text2 = '\n'.join([res[1] for res in resultFront])
print(text2)