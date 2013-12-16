SlideOCR: Automated lecture slide recognition via OCR
-----------------------------------------------------

This project focuses on OCR pre processing. Its goal is to extract text from a video stream of lecture slides given specific timestamps. It is part of a bigger project called [Gewinnung von Meta-Daten aus multimedialen Inhalten][seminar-link] that aims at completely automated lecture content recognition via slides and audio.

   [seminar-link]: http://apache.cs.uni-potsdam.de/de/profs/ifi/mm/lehre

Where to start
--------------

### Installation ###

The code is written in [Python 2.7][python]. Apart from that we need [OpenCV for Python][opencv].

   [python]: http://www.python.org/download/releases/2.7.6/
   [opencv]: http://opencvpython.blogspot.de/2012/05/install-opencv-in-windows-for-python.html

### Configuration ###

Part of the OCR works via [ABBYY Cloud OCR SDK][abbyy] so we need to configure the necessary account details. We will need a [developer account][abbyy-register]. After completing registration, create a **Secrets.py*** in SlideOCR/SlideOcrCode/slideocr/conf and insert the following code:

'class Secrets:
    
    ABBYY_APP_ID = "<your-app-id-goes-here>"
    ABBYY_PWD = "<your-app-password-goes-here>"'

   [abbyy]: http://ocrsdk.com/
   [abbyy-register]: http://cloud.ocrsdk.com/Account/Register
