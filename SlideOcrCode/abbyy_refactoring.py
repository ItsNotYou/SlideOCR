'''
Created on 16.12.2013

@author: hgessner
'''

from slideocr.VideoExtractor import ExtractionHelper
from slideocr.ocr.Abbyy import AbbyyCloud


source = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\img1.png"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace"

helper = ExtractionHelper()
images = helper.convertSingleImage(source, workspace)

ocr = AbbyyCloud()
ocr.process(images)

print images[0].text
