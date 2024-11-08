import easyocr
import matplotlib.pyplot as plt
import cv2
import numpy as np
from easyocr import detection
import pytesseract
import time
from multiprocessing import Pool, cpu_count

# "global" variables, not to be changed and they need to be accessed by functions without being a parameter
config_psm6 = r'-l eng --oem 1 --psm 6 -c tessedit_char_blacklist=\|[{]}'
config_psm7 = r'-l eng --oem 1 --psm 7 -c tessedit_char_blacklist=\|[{]}'
config_psm13 = r'-l eng --oem 1 --psm 13 -c tessedit_char_blacklist=\|[{]}'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'   # MAKE SURE the path is to the correct location with the pytesseract executable

# version information
print("cv2 version: ")
print(cv2.__version__)
print("teseract version: ")
print(pytesseract.get_tesseract_version())
num_processes = cpu_count()
print("Number of CPU cores: " + str( num_processes ))

# used to run multiprocessing for pytesseract three functions: one for psm6, psm7, and psm13
def multiprocess_psm_six(cropped_images):
    return pytesseract.image_to_data(cropped_images, config=config_psm6, output_type=pytesseract.Output.DICT)

def multiprocess_psm_seven(cropped_images):
    return pytesseract.image_to_data(cropped_images, config=config_psm7, output_type=pytesseract.Output.DICT)

def multiprocess_psm_thirteen(cropped_images):
    return pytesseract.image_to_data(cropped_images, config=config_psm13, output_type=pytesseract.Output.DICT)

# Uses x,y,w,h coordinates to create a cropped image. 
# The arguments are an image and array of coordinates, respectively
# array in form [x,y,w,h]
def coordinates_to_image(image, array):
    # crop is in form [y:y+h, x:x+w], round is to erase an error type where float is used for some reason
    new_image = image[round((array[1])):round((array[1]+array[3])), round((array[0])):round((array[0]+array[2]))]
    
    return new_image

# display the cropped image with the index of the array first parameter and second parameter being the array
def display_cropped_image(idx, cropped_images):
    # show all of the cropped images, if any have an error displaying the program will no longer crash!
    try:
        cv2.imshow("Text Detection #" + str(idx), cropped_images[idx])
        cv2.waitKey(0)
    except cv2.error as e:
        print("OpenCV Error:", e)

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

# A failed attempt to run 
def rerun_with_pytess(img, cropped_images, text_boxes, words, pytesseract_results):
    # declare the timing variables as global to solve to issue of them not changing after the function completes
    global time_cropped_easyocr, time_cropped_pytesseract 
    
    # uses the words array to iterate through the found text
    for i in range ( len(words) ):
        # crops the images using the well set up bounding box coordinates stored in an array for each instance of text.
        cropped_images.append(coordinates_to_image(img, text_boxes[i]))

        # show the cropped image
        #display_cropped_image(i, cropped_images)

    pytesseract_time_start = time.time()    # start the time
    print("Check 1") #test

    # this is a dictionary which will include all of the different PSM results. The complete dictionary will then be appended to an array.
    pytess_dict = {
        "psm_six_text" : "NULL",
        "psm_six_confidence" : -1,
        "psm_seven_text" : "NULL",
        "psm_seven_confidence" : -1,
        "psm_thirteen_text" : "NULL",
        "psm_thirteen_confidence" : -1
    }

    # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
    #temp_results6 = pytesseract.image_to_data(cropped_images[i], config=config, output_type=pytesseract.Output.DICT)
    # run pytesseract with multiprocessing
    if __name__ == "__main__":
        with Pool(processes=2) as pool:
            temp_results6 = pool.map(multiprocess_psm_six, cropped_images)
    else:
        return
    print("Check 2") #test

    temp_text = []   # needed in case the results return multiple words
    temp_conf = []   # needed in case the results return multiple confidence levels
    #temp_results_trimmed = []

    #for res in temp_results6:
        # get the only two values out of the dictionary that I care about: text and conf
        #temp_results_trimmed = {key: temp_results6[count][key] for key in temp_results6[count].keys() & {'text', 'conf'}}

    a = 0

    # find the 'text' in temp results by looking to see if a confidence level exists. -1=FALSE
    for idx in temp_results6: 
        b = 0        # count variable for accessing items in the dictionary
        for idy in temp_results6[a]['text']:
            if temp_results6[a]['conf'][b] != -1:
                temp_text.append(temp_results6[a]['text'][b])
                temp_conf.append(temp_results6[a]['conf'][b])
            b += 1
        a += 1
    print("Check 3") #test

    # update the python dictionary confidence level result
    pytess_dict.update({'psm_six_confidence': temp_conf})
    pytess_dict.update({'psm_six_text': temp_text})
    

    # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
    #temp_results7 = pytesseract.image_to_data(cropped_images[i], config=config, output_type=pytesseract.Output.DICT)
    # run pytesseract with multiprocessing
    if __name__ == "__main__":
        with Pool(processes=2) as pool:
            temp_results7 = pool.map(multiprocess_psm_seven, cropped_images)
    print("Check 4") #test

    temp_text = []   # needed in case the results return multiple words
    temp_conf = []   # needed in case the results return multiple confidence levels

    # get the only two values out of the dictionary that I care about: text and conf
    #temp_results_trimmed = {key: temp_results7[count][key] for key in temp_results7[count].keys() & {'text', 'conf'}}

    a = 0

    # find the 'text' in temp results by looking to see if a confidence level exists. -1=FALSE
    for idx in temp_results7: 
        b = 0        # count variable for accessing items in the dictionary
        for idy in temp_results7[a]['text']:
            if temp_results7[a]['conf'][b] != -1:
                temp_text.append(temp_results7[a]['text'][b])
                temp_conf.append(temp_results7[a]['conf'][b])
            b += 1
        a += 1
    print("Check 5") #test

    # update the python dictionary confidence level result
    pytess_dict.update({'psm_seven_confidence': temp_conf})
    pytess_dict.update({'psm_seven_text': temp_text})


    # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
    #temp_results7 = pytesseract.image_to_data(cropped_images[i], config=config, output_type=pytesseract.Output.DICT)
    # run pytesseract with multiprocessing
    if __name__ == "__main__":
        with Pool(processes=2) as pool:
            temp_results13 = pool.map(multiprocess_psm_thirteen, cropped_images)
    print("Check 6") #test

    pytesseract_time_end = time.time()    ### END THE TIME
    temp_text = []   # needed in case the results return multiple words
    temp_conf = []   # needed in case the results return multiple confidence levels

    # get the only two values out of the dictionary that I care about: text and conf
    #temp_results_trimmed = {key: temp_results7[count][key] for key in temp_results7[count].keys() & {'text', 'conf'}}

    a = 0

    # find the 'text' in temp results by looking to see if a confidence level exists. -1=FALSE
    for idx in temp_results13: 
        b = 0        # count variable for accessing items in the dictionary
        for idy in temp_results13[a]['text']:
            if temp_results13[a]['conf'][b] != -1:
                temp_text.append(temp_results13[a]['text'][b])
                temp_conf.append(temp_results13[a]['conf'][b])
            b += 1
        a += 1
    print("Check 7") #test

    # update the python dictionary confidence level result
    pytess_dict.update({'psm_thirteen_confidence': temp_conf})
    pytess_dict.update({'psm_thirteen_text': temp_text})

    # add the time to the pytesseract ocr total time
    pytesseract_elapsed = pytesseract_time_end - pytesseract_time_start
    time_cropped_pytesseract = time_cropped_pytesseract + pytesseract_elapsed

    # append the dictionary to the pytesseract results array
    pytesseract_results.append(pytess_dict)
    
    # show time for pytesseract to complete
    print("time pytesseract: " + str(pytesseract_elapsed))
    print(pytesseract_results)

    

# Crops the images based off of EasyOCR's results, runs pytesseract on the cropped images,
# displays the cropped images, and prints the pytesseract OCR results. Also re-runs easyocr on
# the CROPPED version of the image and displays those results as well. 
def rerun_with_crop_and_display(reader, img, cropped_images, text_boxes, words, pytesseract_results, easyocr_results):   
    # declare the timing variables as global to solve to issue of them not changing after the function completes
    global time_cropped_easyocr, time_cropped_pytesseract 
    
    # this is a dictionary which will include all of the different PSM results. The complete dictionary will then be appended to an array.
    pytess_dict = {
        "psm_six_text" : "NULL",
        "psm_six_confidence" : -1,
        "psm_seven_text" : "NULL",
        "psm_seven_confidence" : -1,
        "psm_thirteen_text" : "NULL",
        "psm_thirteen_confidence" : -1
    }

    # this is a dictionary for the EasyOCR rerun results. I do not care about the bounding boxes and will only have the text and confidence levels.
    easyocr_dict = {
        "text" : "NULL",
        "confidence" : -1
    }

    # variables for processing results (the number indicates the psm type)
    temp_text6 = []   # needed in case the results return multiple words
    temp_conf6 = []   # needed in case the results return multiple confidence levels
    temp_text7 = []   # needed in case the results return multiple words
    temp_conf7 = []   # needed in case the results return multiple confidence levels
    temp_text13 = []   # needed in case the results return multiple words
    temp_conf13 = []   # needed in case the results return multiple confidence levels
    easyocr_text_results = [] # array needed to store the text results from the EasyOCR rerun
    easyocr_conf_results = [] # array needed to store the confidence level results from the EasyOCR rerun

    # uses the words array to iterate through the found text
    for i in range ( len(words) ):
        # crops the images using the well set up bounding box coordinates stored in an array for each instance of text.
        cropped_images.append(coordinates_to_image(img, text_boxes[i]))

        # show the cropped image
        display_cropped_image(i, cropped_images)

        # run pytesseract on the cropped images
        # run pytesseract if confidence level is under 0.9

        ### for config help, type "tesseract --help-oem" and "tesseract --help-psm"
        ### to read an article about the psm settings, my source for the comments provided is:
        ### https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/
        ### PSMs without a generally applicable use for the project: [0, 1, 2, 9]
        ## PSM 6: The text is treated as having a single font face with no variation. Good for single,
        #      consistent font and for materials like simple book pages.
        pytesseract_time_start = time.time()    # start the time

        # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
        temp_results6 = pytesseract.image_to_data(cropped_images[i], config=config_psm6, output_type=pytesseract.Output.DICT)
        
        # count variable for accessing items in the dictionary
        count = 0

        ## testing psm configs
        print("\nPSM: 6")

        # loop through the results and only append the text and confidence to the results array in the dictionary if they exist, which you can detemine
        # with the confidence level where negative one equals false
        for idx in temp_results6['text']:
            if temp_results6['conf'][count] != -1:
                conf_as_decimal = temp_results6['conf'][count] * 0.01   # convert the confidence level to a float
                temp_text6.append(temp_results6['text'][count])
                temp_conf6.append(conf_as_decimal)

                # print results to see what you got
                print("Text and confidence ['" + str( temp_results6['text'][count] ) + "', " + str( conf_as_decimal ) + "]")
            count += 1


        ## PSM 7: is for a single line of UNIFORM text. A good use case is license plates.
        # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
        temp_results7 = pytesseract.image_to_data(cropped_images[i], config=config_psm7, output_type=pytesseract.Output.DICT)

        # count variable for accessing items in the dictionary
        count = 0

        ## testing psm configs
        print("\nPSM: 7")

        # loop through the results and only append the text and confidence to the results array in the dictionary if they exist, which you can detemine
        # with the confidence level where negative one equals false
        for idx in temp_results7['text']:
            if temp_results7['conf'][count] != -1:
                conf_as_decimal = temp_results7['conf'][count] * 0.01   # convert the confidence level to a float
                temp_text7.append(temp_results7['text'][count])
                temp_conf7.append(conf_as_decimal)
                
                # print results to see what you got
                print("Text and confidence ['" + str( temp_results7['text'][count] ) + "', " + str( conf_as_decimal ) + "]")
            count += 1 


        ## PSM 13: throws OCD, segmentation, and tesseract preprocessing out the window. Useful for when
        #      those things HURT the accuracy, the crop is too close, or the font is unrecognized.
        #      Using PSM 13 is seen as a last resort tactic.
        # run image_to_data and get the text, bounding box, and confidence outputted to a dictionary
        temp_results13 = pytesseract.image_to_data(cropped_images[i], config=config_psm13, output_type=pytesseract.Output.DICT)

        pytesseract_time_end = time.time()    ### END THE TIME
        # count variable for accessing items in the dictionary
        count = 0

        ## testing psm configs
        print("\nPSM: 13")

        # loop through the results and only append the text and confidence to the results array in the dictionary if they exist, which you can detemine
        # with the confidence level where negative one equals false
        for idx in temp_results13['text']:
            if temp_results13['conf'][count] != -1:
                conf_as_decimal = temp_results13['conf'][count] * 0.01   # convert the confidence level to a float
                temp_text13.append(temp_results13['text'][count])
                temp_conf13.append(conf_as_decimal)

                # print results to see what you got
                print("Text and confidence ['" + str( temp_results13['text'][count] ) + "', " + str( conf_as_decimal ) + "]")
            count += 1

        # add the time to the pytesseract ocr total time
        pytesseract_elapsed = pytesseract_time_end - pytesseract_time_start
        time_cropped_pytesseract = time_cropped_pytesseract + pytesseract_elapsed
        

        # re-run EasyOCR with the cropped images.
        crop_easyocr_start = time.time()    # start easyOCR time
        result = reader.readtext(cropped_images[i])
        crop_easyocr_end = time.time()    # end easyOCR time

        #add the timing to total cropped easyOCR time
        crop_easyocr_elapsed = crop_easyocr_end - crop_easyocr_start
        time_cropped_easyocr = time_cropped_easyocr + crop_easyocr_elapsed
        print("time pytesseract: " + str(pytesseract_elapsed))
        print("time easyOCR: " + str(crop_easyocr_elapsed))
        
        # print the results and add them to the EasyOCR cropped results array. I will do my best to not create a triple nested for loop.
        for res in result:
            print("EasyOCR text and confidence ['" + str( res[1] ) + "', " + str( res[2] ) + "]")

            # append the results to the EasyOCR results array, which will be used to update the results dictionary.
            easyocr_text_results.append(res[1])
            easyocr_conf_results.append(res[2])
            
    
    # update the dictionary confidence level and text results for all psms on Pytesseract and EasyOCR
    pytess_dict.update({'psm_six_confidence': temp_conf6})
    pytess_dict.update({'psm_six_text': temp_text6})
    pytess_dict.update({'psm_seven_confidence': temp_conf7})
    pytess_dict.update({'psm_seven_text': temp_text7})
    pytess_dict.update({'psm_thirteen_confidence': temp_conf13})
    pytess_dict.update({'psm_thirteen_text': temp_text13})
    easyocr_dict.update({"text": res[1]})
    easyocr_dict.update({"confidence": res[2]})

    # append the dictionaries to their respective results arrays
    pytesseract_results.append(pytess_dict)
    easyocr_results.append(easyocr_dict)


# use to run pytesseract on the cropped images
#def run_pytesseract(idx, cropped_images, time_cropped_pytesseract):
    

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
##fileB = subdirectory + input('Enter file name for card BACK image: ')
##imgB = cv2.imread(fileB)

#gray = cv2.cvtColor(imgF, cv2.COLOR_BGR2GRAY)

#kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
#sharp = cv2.filter2D(gray, -1, kernel)

# create all the timing variables and start timer
time_cropped_easyocr = 0
time_cropped_pytesseract = 0
pytesseract_elapsed = 0   # variable used in run_pytesseract for timing information.
start_time = time.time()

# call function to get results for the image front and back
resultFront = easyocr_get_results(reader, imgF, blacklist_pattern)
##resultBack = easyocr_get_results(reader, imgB, blacklist_pattern)

# end timer
end_time = time.time()
elapsed_time = end_time - start_time

### These are the variables for the FRONT of the image
F_text_full_easy = ""    # big string with full image front results from EasyOCR first run. Used to output into a CSV file.
#F_text_cropped = ""    # big string with cropped image front results from Pytesseract and EasyOCR

# the index for each will be parallel so index[0] for all arrays gets the confidence, box, and word
F_text_boxes = []
F_words = []
F_confidence_level = []

### These are the variables for the BACK of the image
B_text_full_easy = ""    # big string with full image back results from EasyOCR first run. Used to output into a CSV file.
#B_text_cropped = ""    # big string with cropped image back results from Pytesseract and EasyOCR

# the index for each will be parallel so index[0] for all arrays gets the confidence, box, and word
B_text_boxes = []
B_words = []
B_confidence_level = []


# Gather OCR data into arrays for FRONT and BACK. The return variable is used for output to a CSV file.
F_text_full_easy = add_OCRdata_to_arrays(resultFront, F_text_boxes, F_words, F_confidence_level, F_text_full_easy)
##B_text_full_easy = add_OCRdata_to_arrays(resultBack, B_text_boxes, B_words, B_confidence_level, B_text_full_easy)
# Print OCR results from the 3 separate arrays with parallel indexes for FRONT and BACK of card
print_OCRresults(F_text_boxes, F_words, F_confidence_level)
##print_OCRresults(B_text_boxes, B_words, B_confidence_level)

# cropping images using bounding boxes and retrying them individually with the reader
F_cropped_images = []
B_cropped_images = []

# arrays for storing the dictionaries with the Pytesseract results and the dictionaries with the EasyOCR cropped rerun results
F_pytess_results = []
F_cropped_easyocr_results = []
B_pytess_results = []
B_cropped_easyocr_results = []


# run the function that crops, displays, runs pytesseract, and re-runs EasyOCR for FRONT and BACK
rerun_with_crop_and_display(reader, imgF, F_cropped_images, F_text_boxes, F_words, F_pytess_results, F_cropped_easyocr_results)
##rerun_with_crop_and_display(reader, imgB, B_cropped_images, B_text_boxes, B_words, B_pytess_results, B_cropped_easyocr_results)
#rerun_with_pytess(imgF, F_cropped_images, F_text_boxes, F_words, F_pytess_results)

# print times
print("time to complete easyOCR for WHOLE image: " + str(elapsed_time))
print("time to complete easyOCR for CROPPED images: " + str(time_cropped_easyocr))
print("time to complete pytesseract for CROPPED images: " + str(time_cropped_pytesseract) + "\n")

# saves words found to a CSV file
f = open("foundTextTest#1.csv", "a")
f.write(F_text_full_easy + "\n")
f.close()

# reprints the words found again
textF = '\n'.join([res[1] for res in resultFront])
print(textF)

##textB = '\n'.join([res[1] for res in resultBack])
##print(textB)