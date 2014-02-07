SlideOCR: Automated lecture slide recognition via OCR
=====================================================

This project focuses on OCR pre processing. Its goal is to extract text from a video stream of lecture slides given specific timestamps. It is part of a bigger project called [Gewinnung von Meta-Daten aus multimedialen Inhalten][seminar-link] that aims at completely automated lecture content recognition via slides and audio.

   [seminar-link]: http://apache.cs.uni-potsdam.de/de/profs/ifi/mm/lehre

Where to start
--------------

### Installation ###

The code is written in [Python 2.7][python]. Apart from that we need several libraries and tools. Luckily they are all available for free.

If you are on Windows 7 (64 bit) you can just use the install script. The script may also runs on other Windows platforms. Before running the script, you will have to set the *pythonInstallDir* in *slideocr/conf/Paths.py*. If you don't do so and the script can't find the python install directory then it will stop its execution and politely ask you for help. **The script requires administrator privileges.**

A manual installation requires the following:

1. [requests] (via [pip])
1. [ftfy] (via [pip])
1. [django] (via [pip])
1. [OpenCV for Python][opencv] (included in install directory)
1. [Python Imaging Library (PIL)][pil]
1. [NumPy][numpy]
1. [python-dateutil][dateutil]
1. [MySQLdb][mysqldb]
1. [FFmpeg][ffmpeg] (included in install directory)
1. [Tesseract][tesseract] (included in install directory)

FFmpeg and Tesseract have to be in the systems path variable.

   [python]: http://www.python.org/download/releases/2.7.6/
   [opencv]: http://opencvpython.blogspot.de/2012/05/install-opencv-in-windows-for-python.html
   [tesseract]: https://code.google.com/p/tesseract-ocr/
   [ffmpeg]: http://www.ffmpeg.org/
   [requests]: http://requests.readthedocs.org/en/latest/user/install/
   [ftfy]: http://blog.luminoso.com/2012/08/24/fixing-unicode-mistakes-and-more-the-ftfy-package/
   [dateutil]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-dateutil
   [mysqldb]: http://pypi.python.org/pypi/MySQL-python/
   [pil]: http://www.pythonware.com/products/pil/
   [pip]: https://pypi.python.org/pypi/pip
   [django]: https://www.djangoproject.com/download/
   [numpy]: http://www.numpy.org/
   
### Configuration ###

Part of the OCR works via [ABBYY Cloud OCR SDK][abbyy] so we need to configure the necessary account details. We will need a [developer account][abbyy-register]. If you don't want to use the ABBYY Cloud OCR SDK, then you should consider specifying the execution parameter *--skip-abbyy*.

If you want to use the MySQL extractor you will also have to specify your MySQL details. The programm connects to *localhost* on the default MySQL port (3306) and uses the *mydb* database.

To set all the details, **create a Secrets.py** in *SlideOCR/SlideOcrCode/slideocr/conf* and insert the following code:

```python
class Secrets:
	
	ABBYY_APP_ID = "<your-app-id-goes-here>"
	ABBYY_PWD = "<your-app-password-goes-here>"

	MYSQL_USER = "<your-db-user-goes-here>"
	MYSQL_PWD = "<your-db-password-goes-here>"
```

   [abbyy]: http://ocrsdk.com/
   [abbyy-register]: http://cloud.ocrsdk.com/Account/Register
   
### Execution ###

The most convenient way to use the program is via executing *process.py*.

```
usage: process.py [-h] [--configFile CONFIGFILE]
                  [--workingDirectory WORKINGDIRECTORY] --sourceFile
                  SOURCEFILE [-e EXTRACTION] [--videoId] [--skipAbbyy]
                  [--skipTesseract]
                  [--preProcessingBounding PREPROCESSINGBOUNDING [PREPROCESSINGBOUNDING ...]]
                  [--preProcessingOCR PREPROCESSINGOCR [PREPROCESSINGOCR ...]]
                  [--skipCleanup] [--sigmaX SIGMAX] [--sigmaColor SIGMACOLOR]
                  [--thresh THRESH] [--blockSize BLOCKSIZE] [--C C] [--px PX]
                  [--interpolationMode {nearest,bicubic,bilinear,antialias}]
                  [--minAreaSize MINAREASIZE] [--maxAreaHeight MAXAREAHEIGHT]
                  [--mergeThreshold MERGETHRESHOLD]
                  [--boxWideningValue BOXWIDENINGVALUE]
                  [--heightOffset HEIGHTOFFSET]
                  [--tesseractLanguage TESSERACTLANGUAGE]
                  [--abbyyLanguage ABBYYLANGUAGE]
                  [--abbyyBatchSize ABBYYBATCHSIZE]

Extract text from a video stream of lecture slides

optional arguments:
  -h, --help            show this help message and exit

General:
  --configFile CONFIGFILE
                        Path to config-file.
  --workingDirectory WORKINGDIRECTORY
                        Path to a directory that will be used as temporary
                        workspace
  --sourceFile SOURCEFILE
                        Path to an image, a zipped set of images or a video
                        file that will be processed. Video files require the
                        option -e
  -e EXTRACTION, --extraction EXTRACTION
                        Path to a file that contains the frame extraction data
  --videoId             Set if sourceFile is an ID of a video that contains
                        the frame extraction data
  --skipAbbyy           skips ABBYY Cloud OCR processing
  --skipTesseract       skips Tesseract OCR processing
  --preProcessingBounding PREPROCESSINGBOUNDING [PREPROCESSINGBOUNDING ...]
                        List of pre processing steps that are executed to
                        enhance image quality for bounding box algorithms.
  --preProcessingOCR PREPROCESSINGOCR [PREPROCESSINGOCR ...]
                        List of pre processing steps that are executed to
                        enhance image quality for OCR runs.
  --skipCleanup         Keep the temporary files. Defaults to false

gaussianBlurring:
  --sigmaX SIGMAX       Gaussian kernel standard deviation in X direction. The
                        higher sigmaX, the stronger the blur effect. Should be
                        a value between 0 and 3.

bilateralFiltering:
  --sigmaColor SIGMACOLOR
                        Filter sigma in the color space. A larger value of the
                        parameter means that farther colors within the pixel
                        neighborhood (see sigmaSpace ) will be mixed together,
                        resulting in larger areas of semi-equal color.The
                        higher sigmaColor, the stronger the blur effect.

simpleThresholding:
  --thresh THRESH       threshold value.

adaptiveThresholding:
  --blockSize BLOCKSIZE
                        Size of a pixel neighborhood that is used to calculate
                        a threshold value for the pixel: 3, 5, 7, and so on.
  --C C                 Constant subtracted from the mean or weighted mean
                        (see the details below). Normally, it is positive but
                        may be zero or negative as well. Reduces Noises.

opening:
  --px PX               Discarded pixel.

Interpolation:
  --interpolationMode {nearest,bicubic,bilinear,antialias}
                        Interpolationsmodus.

BoundingBoxes:
  --minAreaSize MINAREASIZE
                        Minimal size of a text area. For detecting small
                        characters use a small value, but you will get quite
                        more boxes as result.
  --maxAreaHeight MAXAREAHEIGHT
                        Maximal height of a text area. For detecting large
                        characters, use a large value, but than lines with
                        small characters will be combined in one box, if the
                        sum of their heights is smaller than this
                        maxAreaHeight.
  --mergeThreshold MERGETHRESHOLD
                        Merging threshold to combine bounding boxes.
  --boxWideningValue BOXWIDENINGVALUE
                        Padding for bounding boxes.

textClassification:
  --heightOffset HEIGHTOFFSET
                        Distance of caption and footing to the average text
                        height.

ocrOptions:
  --tesseractLanguage TESSERACTLANGUAGE
                        Tesseract recognition language. Languages are set as
                        three character words (eng, deu, fra etc). Default is
                        eng.
  --abbyyLanguage ABBYYLANGUAGE
                        ABBYY recognition language. Languages are set as full
                        word (English, German, French etc). Default is
                        English.
  --abbyyBatchSize ABBYYBATCHSIZE
                        Number of ABBYY tasks that are processed in parallel.
```
