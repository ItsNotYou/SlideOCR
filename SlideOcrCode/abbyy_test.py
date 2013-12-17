'''
Created on 16.12.2013

@author: hgessner
'''

import time
from slideocr.VideoExtractor import VideoExtractor


source = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\desktop.mp4"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace"
table = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\slide-timestamps.txt"

start = int(round(time.time() * 1000))

extractor = VideoExtractor()
images = extractor.convertVideoByTable(source, table, workspace)

end = int(round(time.time() * 1000))

print "Time taken:"
print end - start
