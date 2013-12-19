'''
Created on 08.12.2013

@author: hgessner
'''

from parameter_parser import ParameterParser
from slideocr.PreProcessors import *
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor, ImageExtractor

import sys

def recognizeFile(extractor, skipAbbyy):
    images = extractor.extract();
    
    pre = PreProcessors()
    images = pre.process(images)
    
    ocr = OcrEngines(skipAbbyy)
    images = ocr.process(images)
    for image in images:
        print image.text

parser = ParameterParser()

#parse parameter
(args,unknown_args) = parser.parse(sys.argv[1:])

workingDirectory = args.workingDirectory
sourceFile = args.sourceFile
split = args.extraction
skipAbbyy = args.skipAbbyy

extractor = None
if split == None:
    extractor = ImageExtractor(workingDirectory, sourceFile)
else:
    extractor = VideoExtractor(workingDirectory, sourceFile, split)

recognizeFile(extractor, skipAbbyy)
