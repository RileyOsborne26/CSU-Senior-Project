import numpy as np
import pytesseract
import cv2
import craft_text_detector
from imutils.object_detection import non_max_suppression
from PIL import Image
#from torchvision.models.resnet import ResNet50_Weights
# Code -- source: https://www.projectpro.io/article/how-to-train-tesseract-ocr-python/561
# Tips on accuracy improvement -- source: https://github.com/tesseract-ocr/tessdoc/tree/main/tess5
#org_resnet = torch.utils.model_zoo.load_url(ResNet50_Weights.IMAGENET1K_V2.url)
print(cv2.__version__)

# resize image to pixel sizes that are a multiple of 32 for the EAST algorithm
def resize_to_32_multiple(img):
    dimensions = img.shape
    h = dimensions[0]
    w = dimensions[1]
    if (h % 32) != 0:
        new_h = h + (32 - h % 32)
    else:
        new_h = h

    if (w % 32) != 0:
        new_w = w + (32 - w % 32)
    else:
        new_w = w
    
    resized_img = cv2.resize(img, (new_w, new_h))
    return resized_img

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
# PSMs without a generally applicable use for the project: [0, 1, 2, 9]
config = r'-l eng --oem 1 --psm 3'

# the test-images folder is used so subdirectory maps to the image requested.
subdirectory = "test-images/"
file = subdirectory + input('Enter file name for card front image: ')
img = cv2.imread(file)
orig = img.copy()     # a copy to be safe

#display image
cv2.imshow('img_CLEAN', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#display image
cv2.imshow('img_COPY', orig)
cv2.waitKey(0)
cv2.destroyAllWindows()

#file_back = subdirectory + input('Enter file name for card back image: ')
#img_back = cv2.imread(file_back)

##### EAST
#
# Source: https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV/tree/master
#
# define the two output layer names for the EAST detector model that
# we are interested -- the first is the output probabilities and the
# second can be used to derive the bounding box coordinates of text
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]

# get dimensions and resize
(h, w) = img.shape[:2]

# set the new width and height and then determine the ratio in change
# for both the width and height (default=320)
(new_w, new_h) = (320, 320)
ratio_w = w / float(new_w)
ratio_h = h / float(new_h)
## FIX THIS

# resize the image and grab the new image dimensions
img = cv2.resize(img, (new_w, new_h))
(h, w) = img.shape[:2]

#display image
cv2.imshow('img_RESIZE_1st', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#resized_img = resize_to_32_multiple(img)

# load the pre-trained EAST text detector
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

# construct a blob from the image and then perform a forward pass of
# the model to obtain the two output layer sets
blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (123.68, 116.78, 103.94), swapRB=True, crop=False)

# Set the blob as input to the network
net.setInput(blob)

# Forward pass through the network to perform text detection
(scores, geometry) = net.forward(layerNames)

# grab the number of rows and columns from the scores volume, then
# initialize our set of bounding box rectangles and corresponding
# confidence scores
(numRows, numCols) = scores.shape[2:4]
rects = []
confidences = []

# loop over the number of rows
for y in range(0, numRows):
    # extract the scores (probabilities), followed by the geometrical
    # data used to derive potential bounding box coordinates that
    # surround text
    scoresData = scores[0, 0, y]
    xData0 = geometry[0, 0, y]
    xData1 = geometry[0, 1, y]
    xData2 = geometry[0, 2, y]
    xData3 = geometry[0, 3, y]
    anglesData = geometry[0, 4, y]

    # loop over the number of columns
    for x in range(0, numCols):
        # if our score does not have sufficient probability, ignore it. default is 0.5
        if scoresData[x] < 0.5:
            continue

        # compute the offset factor as our resulting feature maps will
        # be 4x smaller than the input image
        (offsetX, offsetY) = (x * 4.0, y * 4.0)

        # extract the rotation angle for the prediction and then
        # compute the sin and cosine
        angle = anglesData[x]
        cos = np.cos(angle)
        sin = np.sin(angle)

        # use the geometry volume to derive the width and height of
        # the bounding box
        h = xData0[x] + xData2[x]
        w = xData1[x] + xData3[x]

        # compute both the starting and ending (x, y)-coordinates for
        # the text prediction bounding box
        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
        endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
        startX = int(endX - w)
        startY = int(endY - h)

        # add the bounding box coordinates and probability score to
        # our respective lists
        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
boxes = non_max_suppression(np.array(rects), probs=confidences)

# loop over the bounding boxes
for (startX, startY, endX, endY) in boxes:
    # scale the bounding box coordinates based on the respective
    # ratios
    startX = int(startX * ratio_w)
    startY = int(startY * ratio_h)
    endX = int(endX * ratio_w)
    endY = int(endY * ratio_h)

    # draw the bounding box on the image
    cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

# show the output image
cv2.imshow("Text Detection", orig)
cv2.waitKey(0)

# Draw the bounding boxes on the original image
#for box in boxes:
#    (startX, startY, endX, endY) = box.astype("int")
#    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

##### CRAFT
# create variable to hold the path to the CRAFT weight 
#weight_path_craft_net = "/home/rileyosborne26/.craft_text_detector/weights/craft_mlt_25k.pth"
#weight_path_refine_net = "/home/rileyosborne26/.craft_text_detector/weights/craft_refiner_CTW1500.pth"

# Text Detection Section
#craft_model = craft_text_detector.Craft(weight_path_craft_net, weight_path_refine_net, crop_type="box")   # define a craft model
#output_dir = 'craft_output/'
#craft_model = Craft(output_dir=output_dir, crop_type='poly', cuda=False)

### Resizing for Jaided.AI
# dimensions = img.shape
# h = dimensions[0]
# w = dimensions[1]
# reduce_h = 1500/h
# reduce_w = 1500/w
# if reduce_w < reduce_w:
#     reducer = reduce_w
# else:
#     reducer = reduce_h

# new_h = round(h * reducer)
# new_w = round(w * reducer)

# # (width, height)
# shrink = img.resize(new_w, new_h)

# image = Image.open(file)
# new_image = image.resize((new_w, new_h))
# new_image.save('myimage_500.jpg')

#text_regions = craft_model.detect_text(shrink)
#print(text_regions)

# unload models from ram/gpu
#craft_model.unload_craftnet_model()
#craft_model.unload_refinenet_model()

# display x, y, w, h
#for text_region in text_regions:
#    print("1: " + text_region[0])
#    print("2: " + text_region[1])
#    print("3: " + text_region[2])
#    print("4: " + text_region[3] + "\n")

# idea for MANUAL ocr that forces the machine to look a certain direction
# Select the region of interest (ROI)
roi = cv2.selectROI(img)

# Crop the ROI from the image y=roi[1] h=roi[3] x=roi[0] w=roi[2]
cropped_image = img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

# Display the cropped image
cv2.imshow("Cropped Image", cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Done with cropping, moving to OCR...\n")

# techniques to try for improving ocr
gray = convert_grayscale(img)
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharp = cv2.filter2D(gray, -1, kernel)

# fetch image shape
h, w, c = img.shape

# obtain boxes 
boxes = pytesseract.image_to_boxes(cropped_image)

# for loop to draw rectangles on detected boxes
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

#display image
#cv2.imshow('img', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# to clarift english add ", lang='eng'" to the command
text = pytesseract.image_to_string(cropped_image, config=config)

## testing psm configs
print("\nPSM: 3")
print(text) 
file1 = open("MyFile.txt", "w") 
file1.write("PSM 3" + "\n" + text)

#config = r'--oem 1 --psm 0'
#text = pytesseract.image_to_string(sharp, config=config)
#print("\nPSM: 0")
#print(text) 

config = r'-l eng --oem 1 --psm 4'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 4")
print(text)  
file1.write("PSM 4" + "\n" + text)

config = r'-l eng --oem 1 --psm 5'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 5")
print(text) 
file1.write("PSM 5" + "\n" + text)

config = r'-l eng --oem 1 --psm 6'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 6")
print(text) 
file1.write("PSM 6" + "\n" + text)

config = r'-l eng --oem 1 --psm 7'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 7")
print(text)  
file1.write("PSM 7" + "\n" + text)

config = r'-l eng --oem 1 --psm 8'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 8")
print(text)  
file1.write("PSM 8" + "\n" + text)

config = r'-l eng --oem 1 --psm 10'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 10")
print(text)  
file1.write("PSM 10" + "\n" + text)

config = r'-l eng --oem 1 --psm 11'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 11")
print(text) 
file1.write("PSM 11" + "\n" + text)

config = r'-l eng --oem 1 --psm 12'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 12")
print(text) 
file1.write("PSM 12" + "\n" + text)

config = r'-l eng --oem 1 --psm 13'
text = pytesseract.image_to_string(cropped_image, config=config)
print("\nPSM: 13")
print(text) 
file1.write("PSM 13" + "\n" + text)

file1.close()