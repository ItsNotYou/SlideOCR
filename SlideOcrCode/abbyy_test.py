'''
Created on 16.12.2013

@author: hgessner
'''

import time
from slideocr.VideoExtractor import FrameExtractor, TableReader


source = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\desktop.mp4"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace"
table = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\slide-timestamps.txt"

start = int(round(time.time() * 1000))

timestamps = TableReader().readTimestamps(table, source)
images = FrameExtractor(workspace).mapTimestampsToFrames(timestamps)

end = int(round(time.time() * 1000))

print "Time taken:"
print end - start
