'''
Created on 08.12.2013

@author: hgessner
'''

import argparse
import os
import copy
import shutil
from slideocr.ocr.Abbyy import AbbyyCloud
from slideocr.ocr.Tesseract import Tesseract
from slideocr.Data import OcrImage
from slideocr.PreProcessors import BilateralFiltering


def recognizeFile(sourceFile):
    images = [OcrImage()]
    images[0].path = sourceFile
    
    biFilter = BilateralFiltering(75)
    images = biFilter.process(images)
    
    imagesAbbyy = copy.deepcopy(images);
    imagesTesseract = copy.deepcopy(images);
    
    abbyy = AbbyyCloud()
    result = abbyy.process(imagesAbbyy)
     
    print result[0].text
    
    tesseract = Tesseract()
    result = tesseract.process(imagesTesseract)
    
    print result[0].text


parser = argparse.ArgumentParser( description="Recognize a file via web service" )
parser.add_argument( 'sourceFile' )
parser.add_argument( 'workingDirectory' )
args = parser.parse_args()

sourceFile = args.sourceFile
workingDirectory = args.workingDirectory

if os.path.isfile(sourceFile):
    targetFile = os.path.join(workingDirectory, os.path.basename(sourceFile));
    shutil.copyfile(sourceFile, targetFile)
    recognizeFile(targetFile)
else:
    print(sourceFile + " ist keine Datei")
    print("Vorgang abgebrochen")
