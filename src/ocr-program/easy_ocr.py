import easyocr
#import matplotlib.pyplot as plt
import cv2
import time
import numpy as np

## source: https://www.youtube.com/watch?v=j_gI4SlVrz8
## Channel: Augmented Startups

reader = easyocr.Reader(['en'], gpu=False) #gpu=False to use CPU
#vid = cv2.VideoCapture("numplate.mp4") ##use for video, not for an image
file = input('Enter file name: ')
img = cv2.imread(file) #use for an image
print(img.shape)
init: bool = True
iter = 0

while(iter < 1):
    a = time.time()
    #ret, img = 'Capture.JPG'
    #ret, img = vid.read()

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #img_sharp = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = reader.readtext(gray)
    #result = reader.readtext(img)
    #result = reader.readtext(img_sharp)
    text = ""

    for res in result:
        text += res[1] + ","
    #cv2.putText(img, text, (50,70), cv2.QT_FONT_NORMAL, 1, (0,0,0), 2) #PERFORMANCE

    ##FPS
    b = time.time()
    fps = 1/(b-a) #PERFORMANCE
    #cv2.line(img, (20,25), (127,25), [85,45,255],30) #PERFORMANCE
    #cv2.putText(img, f'FPS: {int(fps)}', (11,35), cv2.QT_FONT_NORMAL, 1, (255,255,255), 2, lineType=cv2.LINE_AA) #PERFORMANCE
    #cv2.imshow("result", img) #PERFORMANCE

    #attempt to write text as a csv file
    f = open("foundTextTest#1.csv", "a")
    f.write(text + "\n")
    f.close()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print(fps)
    print(text)

    init = False
    iter += 1