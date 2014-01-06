'''
Created on 06.01.2014

@author: hgessner
'''

import uuid
import cv2
import os


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
