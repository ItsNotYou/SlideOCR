'''
Created on 16.12.2013

@author: hgessner
'''

import subprocess
from slideocr.Handlers import Ocr
from slideocr.ocr.OcrCommons import BoundingBoxExtraction
from slideocr.Helper import FileNameCreator
from ftfy import fix_text


class Tesseract(Ocr):
    '''
    Runs tesseract on all images and reads the detection result
    If a bounding box is specified, the box is copied into a separate file before tesseract is executed
    '''
    
    procName = "tesseract"
    procPath = "tesseract"
    language = None
    
    def __init__(self, language):
        self.language = language
    
    def process(self, images):
        images = BoundingBoxExtraction().process(images)
        
        for image in images:
            path = image.boundingPath
            # Tesseract will automatically append the file ending ".txt", so we have to copy this behaviour
            resultFile = FileNameCreator.createFileNameWithoutExtension(path, [], self.procName, ".txt")
            self._runTesseract(path, resultFile, self.language)
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
