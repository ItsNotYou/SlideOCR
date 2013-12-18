'''
Created on 16.12.2013

@author: hgessner
'''

import uuid
import cv2
import subprocess
import os
from slideocr.Handlers import Ocr


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


class BoundingBoxExtraction:
    
    
    def process(self, images):
        for image in images:
            image.boundingPath = self.createSubImage(image.path, image.bounding)
        return images
    
    def createSubImage(self, srcPath, bounding):
        if bounding == None:
            return srcPath
        
        dstPath = self._createFileName(srcPath, "bounding")
        
        src = cv2.imread(srcPath)
        dst = self.getRectSubPix(src, bounding)        
        cv2.imwrite(dstPath, dst)
        
        return dstPath
    
    def getRectSubPix(self, image, bounding):
        patchSize = (bounding.right - bounding.left, bounding.bottom - bounding.top)
        center = ((bounding.left + bounding.right) / 2, (bounding.top + bounding.bottom) / 2)
        return cv2.getRectSubPix(image, patchSize, center)
    
    def _createFileName(self, path, prefix):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        uniqueId = uuid.uuid4()
        return os.path.join(head, name + "_%s_%s" % (prefix, str(uniqueId)) + ext)
    