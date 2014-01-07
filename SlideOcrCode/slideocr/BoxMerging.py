'''
Created on 07.01.2014

@author: Matthias
'''

import math
from slideocr.BoundingBoxes import *
from slideocr.Data import *
import copy

class Merging():
    
    def process(self,images,threshold):
    
        currentBoundingArray = []
    
        for image in images:
            
            newBoundingArray = []
            
            flag = True
            
            for currentBounding in currentBoundingArray:
                
                if (_nextTo(currentBounding,image.bounding,threshold) and _ifSameLine(currentBounding,image.bounding)):
                    
                    newBoundingBox = BoundingBox()
                    newBoundingBox.left = min(currentBounding.left,image.bounding.left)
                    newBoundingBox.right = max(currentBounding.right,image.bounding.right)
                    newBoundingBox.top = min(currentBounding.top,image.bounding.top)
                    newBoundingBox.bottom = max(currentBounding.bottom,image.bounding.bottom)
                    
                    newBoundingArray.append(newBoundingBox)
                    flag = False
                    
                else:
                    newBoundingArray.append(currentBounding)
            
            if (flag):
                newBoundingArray.append(copy.deepcopy(image.bounding))
                
                
            currentBoundingArray = newBoundingArray
            flag = True
            
        inImage = cv2.imread("C:\\Users\\Matthias\\Documents\\Workspace\\Python\\SlideOCR\\samples\\working\\first_slide.png", 1)
        
        for b in currentBoundingArray:
            
            cv2.rectangle(inImage, (b.left, b.top), (b.right, b.bottom), (0, 0, 255), 2) 
            
        cv2.imwrite("C:\\Users\\Matthias\\Documents\\Workspace\\Python\\SlideOCR\\samples\\working\\bllaaaaass.png",inImage)
        
        
            
                
 
def _nextTo(bounding1,bounding2,threshold):
    
    if (math.fabs(bounding1.right - bounding2.left) < threshold or \
        math.fabs(bounding2.right - bounding1.left) < threshold ):
        
        return True;
    
    return False               


def _ifSameLine(bounding1,bounding2):
    
    if (bounding1.top >= bounding2.top and bounding1.top <= bounding2.bottom or \
        bounding2.top >= bounding1.top and bounding2.top <= bounding1.bottom):
        
        return True;
    
    return False;
        
        
    
    
    
                
        