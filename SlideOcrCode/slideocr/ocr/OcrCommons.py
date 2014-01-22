'''
Created on 06.01.2014

@author: hgessner
'''

import cv2
from slideocr.Helper import FileNameCreator


class BoundingBoxExtraction:
    
    
    def process(self, images):
        for image in images:
            image.boundingPath = self.createSubImage(image.path, image.bounding)
        return images
    
    def createSubImage(self, srcPath, bounding):
        if bounding == None:
            return srcPath
        
        dstPath = FileNameCreator._createFileName(srcPath, "bounding")
        
        src = cv2.imread(srcPath)
        dst = self.getRectSubPix(src, bounding)        
        cv2.imwrite(dstPath, dst)
        
        return dstPath
    
    def getRectSubPix(self, image, bounding):
        patchSize = (bounding.right - bounding.left, bounding.bottom - bounding.top)
        center = ((bounding.left + bounding.right) / 2, (bounding.top + bounding.bottom) / 2)
        return cv2.getRectSubPix(image, patchSize, center)
