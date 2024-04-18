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

To set up, go to:
    https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV/blob/master/frozen_east_text_detection.pb
    Download the raw file.
    Place it in your workfolder with the script that will be using it.

Pip commands needed for requirements (EasyOCR & Pytesseract):
    #sudo apt install python3-pip #if pip isn't installed
    pip install numpy
    pip install opencv-python
    #pip install craft-text-detector
    pip install imutils
    #pip install torchvision==0.13.0
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

    # Download these two files:
    #    craft_mlt_25k.pth
    #    craft_refiner_CTW1500.pth
    #
    #    put them in: 
    #        /home/<your_user>/.craft_text_detector/weights/

I do not believe these are required but I would recommend just in case:
    sudo apt-get install libgl1-mesa-glx
    sudo apt-get install libgtk2.0-dev pkg-config

Commands I had to run to set up on a ubuntu gaming PC:
sudo apt upgrade python3 #error on openjdk11
java -version
sudo apt purge oracle-java11-installer-local
dpkg -l | grep oracle-java11-installer-local
uname -a
wget https://download.oracle.com/java/21/latest/jdk-21_linux-x64_bin.tar.gz
sudo mkdir -p /usr/local/java
sudo mv jdk-21_linux-x64_bin.tar.gz /usr/local/java/
cd /usr/local/java/
sudo tar -zxvf jdk-21_linux-x64_bin.tar.gz
nano ~/.bashrc
    add lines:
       export JAVA_HOME=/usr/local/java/jdk-21.0.3
       export PATH=$JAVA_HOME/bin:$PATH
       export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
cd /
pip install matplotlib
pip install pytesseract

# go to https://pytorch.org and make sure your pytorch is the correct version
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
