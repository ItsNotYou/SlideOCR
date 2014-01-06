SlideOCR: Automated lecture slide recognition via OCR
-----------------------------------------------------

This project focuses on OCR pre processing. Its goal is to extract text from a video stream of lecture slides given specific timestamps. It is part of a bigger project called [Gewinnung von Meta-Daten aus multimedialen Inhalten][seminar-link] that aims at completely automated lecture content recognition via slides and audio.

   [seminar-link]: http://apache.cs.uni-potsdam.de/de/profs/ifi/mm/lehre

Where to start
--------------

### Installation ###

The code is written in [Python 2.7][python]. Apart from that we need [OpenCV for Python][opencv] for pre processing, [Tesseract][tesseract] for OCR processing, [FFmpeg][ffmpeg] for frame extraction and [Requests][requests] for network communication. Tesseract and FFmpeg have to be in our path variable. We recommend the 32-Bit version of every program and library.

   [python]: http://www.python.org/download/releases/2.7.6/
   [opencv]: http://opencvpython.blogspot.de/2012/05/install-opencv-in-windows-for-python.html
   [tesseract]: https://code.google.com/p/tesseract-ocr/
   [ffmpeg]: http://www.ffmpeg.org/
   [requests]: http://requests.readthedocs.org/en/latest/user/install/
   
   [dateutil]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-dateutil
   [pyparsing]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyparsing
   [six]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#six

### Configuration ###

Part of the OCR works via [ABBYY Cloud OCR SDK][abbyy] so we need to configure the necessary account details. We will need a [developer account][abbyy-register]. After completing registration, **create a Secrets.py** in *SlideOCR/SlideOcrCode/slideocr/conf* and insert the following code:

    class Secrets:
        
        ABBYY_APP_ID = "<your-app-id-goes-here>"
        ABBYY_PWD = "<your-app-password-goes-here>"

If you don't want to use the ABBYY Cloud OCR SDK, then you should consider specifying the execution parameter *--skip-abbyy*.

   [abbyy]: http://ocrsdk.com/
   [abbyy-register]: http://cloud.ocrsdk.com/Account/Register

### Execution ###

The most convenient way to use the program is via executing *process.py*.

    usage: process.py [-h] [-e EXTRACTION] [--skipAbbyy]
                      workingDirectory sourceFile
    
    Extract text from a video stream of lecture slides
    
    positional arguments:
      workingDirectory      Path to a directory that will be used as temporary
                            workspace
      sourceFile            Path to an image or video file that will be processed.
                            Video files require the option -e
    
    optional arguments:
      -h, --help            show this help message and exit
      -e EXTRACTION, --extraction EXTRACTION
                            Path to a file that contains the frame extraction data
      --skipAbbyy          skips ABBYY Cloud OCR processing
