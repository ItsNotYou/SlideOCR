'''
Created on 17.12.2013

@author: hgessner
'''

import uuid
import cv2
import os
import copy
from slideocr.Handlers import Ocr
from slideocr.ocr.Tesseract import Tesseract
from slideocr.ocr.Abbyy import AbbyyCloud


class OcrEngines(Ocr):
    '''
    Combines several ocr engines
    '''
    
    engines = []
    
    def __init__(self, skipAbbyy = False):
        self.engines.append(Tesseract())
        if not skipAbbyy:
            self.engines.append(AbbyyCloud())
    
    
    def process(self, images):
        result = []
        for engine in self.engines:
            engineImages = copy.deepcopy(images)
            engineImages = engine.process(engineImages)
            result.extend(engineImages)
        return result
    

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
