'''
Created on 16.12.2013

@author: hgessner
'''

import os
import time
from slideocr.VideoExtractor import FrameExtractor, TableReader


def file_contained(images, fullPath):
    for image in images:
        if fullPath == image.path:
            return True
    return False

source = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\desktop.mp4"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace"
table = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\slide-timestamps.txt"

start = int(round(time.time() * 1000))
 
timestamps = TableReader().readTimestamps(table, source)
images = FrameExtractor(workspace).mapTimestampsToFrames(timestamps)
 
end = int(round(time.time() * 1000))
 
print "Time taken:"
print end - start

for someFile in os.listdir(workspace):
    fullPath = os.path.join(workspace, someFile);
    if not file_contained(images, fullPath):
        os.remove(fullPath)
