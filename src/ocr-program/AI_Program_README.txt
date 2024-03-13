This OCR Program may end up using both OCR detection models. Both the Pytesseract
and EasyOCR implementation work to some capacity.
The main implementation choice:
    EasyOCR

#####   Pytesseract   #####
Library for OCR: pytesseract
command to get pytesseract executable path:
    "which pytesseract"

Install command (pytesseract):
    sudo apt-get install tesseract-ocr

Script name in GitHub repository:
    "tesseract_ocrAIv2.py"

Command for tesseract PSM modes and more:
    tesseract --help-extra
##### Pytesseract end #####


#####   EasyOCR   #####
Library for OCR: easyocr
command to get pytesseract executable path: n/a

Install command (easyocr):
    pip install git+https://github.com/JaidedAI/EasyOCR.git

Script name in GitHub repository:
    "easy_ocrAIver.py"
    or "easy_ocr.py" (INCOMPLETE!!)

##### EasyOCR end #####

Text detector of choice: EAST algorithm
*EAST input images must be a multiple of 32 pixels

Pip commands needed for requirements (EasyOCR & Pytesseract):
    pip install numpy
    pip install opencv-python
    #pip install craft-text-detector
    pip install imutils
    #pip install torchvision==0.13.0

    # Download these two files:
    #    craft_mlt_25k.pth
    #    craft_refiner_CTW1500.pth
    #
    #    put them in: 
    #        /home/<your_user>/.craft_text_detector/weights/

I do not believe these are required but I would recommend just in case:
    sudo apt-get install libgl1-mesa-glx
    sudo apt-get install libgtk2.0-dev pkg-config