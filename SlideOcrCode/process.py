'''
Created on 08.12.2013

@author: hgessner
'''

import argparse
import os
from slideocr.ocr.Abbyy import AbbyyCloud
from slideocr.Data import OcrImage


def recognizeFile(sourceFile):
    images = [OcrImage()]
    images[0].path = sourceFile
    
    abbyy = AbbyyCloud()
    abbyy.process(images)
    
    print images[0].text


parser = argparse.ArgumentParser( description="Recognize a file via web service" )
parser.add_argument( 'sourceFile' )
args = parser.parse_args()

sourceFile = args.sourceFile

if os.path.isfile(sourceFile):
    print("Parse Datei")
    recognizeFile(sourceFile)
else:
    print(sourceFile + " ist keine Datei")
    print("Vorgang abgebrochen")
