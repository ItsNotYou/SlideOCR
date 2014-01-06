'''
Created on 18.12.2013

@author: hgessner
'''

from slideocr.Data import BoundingBox
from slideocr.VideoExtractor import ExtractionHelper
from slideocr.ocr.Abbyy import AbbyyUploader, AbbyyTask


src = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\first_slide.png"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace\\"
bounding = BoundingBox()
bounding.left = 180
bounding.top = 560
bounding.right = 880
bounding.bottom = 600
# bounding.left = 1
# bounding.top = 1
# bounding.right = 1200
# bounding.bottom = 700

helper = ExtractionHelper()
images = helper.convertSingleImage(src, workspace)
images[0].bounding = bounding

task = AbbyyTask()
task.image = images[0]

uploader = AbbyyUploader()
uploader.callSubmitImage(task)
uploader.callProcessFields(task)
# uploader.callProcessImage(task)
# uploader.callProcessTextField(task)
uploader.waitForImageCompletion(task)
uploader.downloadResult(task)

print task.image.text

# ocr = AbbyyCloud()
# images = ocr.process(images)
# for image in images:
#     print image.text
