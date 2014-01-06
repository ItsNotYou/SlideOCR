'''
Created on 18.12.2013

@author: hgessner
'''

from slideocr.Data import BoundingBox
from slideocr.VideoExtractor import ExtractionHelper
from slideocr.ocr.Abbyy import AbbyyCloud
from slideocr.ocr.Tesseract import Tesseract


src = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\first_slide.png"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace\\"
bounding = BoundingBox()
bounding.left = 180
bounding.top = 560
bounding.right = 880
bounding.bottom = 600

helper = ExtractionHelper()
images = helper.convertSingleImage(src, workspace)
images[0].bounding = bounding

ocr = AbbyyCloud()
images = ocr.process(images)
for image in images:
    print image.text
