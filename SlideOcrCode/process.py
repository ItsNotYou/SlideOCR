'''
Created on 08.12.2013

@author: hgessner
'''

import argparse
import os
from slideocr.PreProcessors import PreProcessors
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor


def recognizeFile(sourceFile, workingDirectory, skipAbbyy):
    extractor = VideoExtractor()
    images = extractor.convertSingleImage(sourceFile, workingDirectory)
    
    pre = PreProcessors()
    images = pre.process(images)
    
    ocr = OcrEngines(skipAbbyy)
    images = ocr.process(images)
    for image in images:
        print image.text


parser = argparse.ArgumentParser( description="Recognize a file via web service" )
parser.add_argument( 'sourceFile' )
parser.add_argument( 'workingDirectory' )
parser.add_argument("--skip-abbyy", help="skips ABBYY Cloud OCR processing", action="store_true")
args = parser.parse_args()

sourceFile = args.sourceFile
workingDirectory = args.workingDirectory
skipAbbyy = args.skip_abbyy

if os.path.isfile(sourceFile):
    recognizeFile(sourceFile, workingDirectory, skipAbbyy)
else:
    print(sourceFile + " ist keine Datei")
    print("Vorgang abgebrochen")
