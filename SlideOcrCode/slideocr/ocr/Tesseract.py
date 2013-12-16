'''
Created on 16.12.2013

@author: hgessner
'''

import subprocess
import os
from slideocr.Handlers import Ocr


class Tesseract(Ocr):
    '''
    Runs tesseract on all images and reads the detection result
    '''
    
    procName = "tesseract"
    procPath = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"
    # Default: detect language as english
    language = "eng"
    
    def process(self, images):
        for image in images:
            resultFile = self._createFileName(image.path, [], self.procName)
            self._runTesseract(image.path, resultFile, self.language)
            # Tesseract will automatically append the file ending ".txt", so we have to copy this behaviour
            image.text = self._readFileIntoString(resultFile + ".txt")
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
