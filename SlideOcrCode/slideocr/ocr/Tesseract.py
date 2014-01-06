'''
Created on 16.12.2013

@author: hgessner
'''

import subprocess
import os
from slideocr.Handlers import Ocr
from slideocr.ocr.OcrCommons import BoundingBoxExtraction
from ftfy import fix_text


class Tesseract(Ocr):
    '''
    Runs tesseract on all images and reads the detection result
    If a bounding box is specified, the box is copied into a separate file before tesseract is executed
    '''
    
    procName = "tesseract"
    procPath = "tesseract"
    # Default: detect language as english
    language = "eng"
    
    def process(self, images):
        images = BoundingBoxExtraction().process(images)
        
        for image in images:
            path = image.boundingPath
            resultFile = self._createFileName(path, [], self.procName)
            self._runTesseract(path, resultFile, self.language)
            # Tesseract will automatically append the file ending ".txt", so we have to copy this behaviour
            image.text = self._readFileIntoString(resultFile + ".txt")
            # Clean encoding mistakes
            image.text = fix_text(image.text.decode("utf-8"))
        return images;
        
        
    def _runTesseract(self, inImagePath, outTextPath, language):
        subprocess.call([self.procPath, inImagePath, outTextPath, "-l", language]);
        
        
    def _readFileIntoString(self, filePath):
        with open(filePath, "r") as myfile:
            data=myfile.read().replace('\n', '').replace('\r', '')
        return data
        
        
    # creates the file name of an output image        
    def _createFileName(self, path, argList, procName):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        add = ""
        for arg in argList:
            add += "_" + str(arg)
        return os.path.join(head,name + "_%s%s" % (procName,add) + ext)
