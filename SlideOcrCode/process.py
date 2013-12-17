'''
Created on 08.12.2013

@author: hgessner
'''

import argparse
from slideocr.PreProcessors import PreProcessors
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor, ImageExtractor


def recognizeFile(extractor, skipAbbyy):
    images = extractor.extract();
    
    pre = PreProcessors()
    images = pre.process(images)
    
    ocr = OcrEngines(skipAbbyy)
    images = ocr.process(images)
    for image in images:
        print image.text


parser = argparse.ArgumentParser(description="Extract text from a video stream of lecture slides")
parser.add_argument("workingDirectory", help = "Path to a directory that will be used as temporary workspace")
parser.add_argument("sourceFile", help = "Path to an image or video file that will be processed. Video files require the option -e")
parser.add_argument("-e", "--extraction", help = "Path to a file that contains the frame extraction data")
parser.add_argument("--skip-abbyy", help="skips ABBYY Cloud OCR processing", action="store_true")

args = parser.parse_args()
workingDirectory = args.workingDirectory
sourceFile = args.sourceFile
split = args.extraction
skipAbbyy = args.skip_abbyy

extractor = None
if split == None:
    extractor = ImageExtractor(workingDirectory, sourceFile)
else:
    extractor = VideoExtractor(workingDirectory, sourceFile, split)

recognizeFile(extractor, skipAbbyy)
