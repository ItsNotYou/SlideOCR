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
            currentBoundingArray.append(image.bounding)
            
        newBounding = _merge(currentBoundingArray,threshold)
        
        newSize = 0
        keks = _merge(newBounding,threshold)
        oldSize = len(keks)
        while (newSize != oldSize):
            oldSize = newSize
            keks = _merge(keks,threshold)
            newSize = len(keks)
            
        inImage = cv2.imread("C:\\Users\\Matthias\\Documents\\Workspace\\Python\\SlideOCR\\samples\\working\\first_slide.png", 1)
    
        for b in keks:
        
            cv2.rectangle(inImage, (b.left, b.top), (b.right, b.bottom), (0, 0, 255), 2) 
        
        cv2.imwrite("C:\\Users\\Matthias\\Documents\\Workspace\\Python\\SlideOCR\\samples\\working\\bllaaaaass.png",inImage)
        
        
def _merge(oldBoundings,threshold):
    
    currentBoundingArray = []

    for oldBounding in oldBoundings:
        
        newBoundingArray = []
        
        flag = True
        
        for currentBounding in currentBoundingArray:
            
            if ((_nextTo(currentBounding,oldBounding,threshold) or _inIt(currentBounding,oldBounding)) and _ifSameLine(currentBounding,oldBounding)):
                
                newBoundingBox = BoundingBox()
                newBoundingBox.left = min(currentBounding.left,oldBounding.left)
                newBoundingBox.right = max(currentBounding.right,oldBounding.right)
                newBoundingBox.top = min(currentBounding.top,oldBounding.top)
                newBoundingBox.bottom = max(currentBounding.bottom,oldBounding.bottom)
                
                newBoundingArray.append(newBoundingBox)
                flag = False
                
            else:
                newBoundingArray.append(currentBounding)
        
        if (flag):
            newBoundingArray.append(copy.deepcopy(oldBounding))
            
            
        currentBoundingArray = newBoundingArray;
        flag = True     
        
    return currentBoundingArray         
                
 
def _nextTo(bounding1,bounding2,threshold):
    
    if (math.fabs(bounding1.right - bounding2.left) < threshold or \
        math.fabs(bounding2.right - bounding1.left) < threshold ):
        
        return True
    
    return False               


def _ifSameLine(bounding1,bounding2):
    
    if (bounding1.top >= bounding2.top and bounding1.top <= bounding2.bottom or \
        bounding2.top >= bounding1.top and bounding2.top <= bounding1.bottom):
        
        return True
    
    return False

def _inIt(bounding1,bounding2):
    if (bounding1.left >= bounding2.left and bounding1.left <= bounding2.right or \
        bounding1.right >= bounding2.left and bounding1.right <= bounding2.right or \
        bounding2.left >= bounding1.left and bounding2.left <= bounding1.right or \
        bounding2.right >= bounding1.left and bounding2.right <= bounding1.right):
        
        return True
    
    return False

def _checkForNewMerges(boundingBox,boundingBoxArray,threshold):
    
    flag = True
    
    newBoundingArray = []
    newBoundingBox = BoundingBox()
    
    for currentBoundingBox in boundingBoxArray:
        
        if ((_nextTo(currentBoundingBox,boundingBox,threshold) or _inIt(currentBoundingBox,boundingBox)) and _ifSameLine(currentBoundingBox,boundingBox) and flag):
        
            newBoundingBox.left = min(currentBoundingBox.left,boundingBox.left)
            newBoundingBox.right = max(currentBoundingBox.right,boundingBox.right)
            newBoundingBox.top = min(currentBoundingBox.top,boundingBox.top)
            newBoundingBox.bottom = max(currentBoundingBox.bottom,boundingBox.bottom)
            
            newBoundingArray.append(newBoundingBox)
            flag = False
    
        else:
            newBoundingArray.append(currentBoundingBox)
            
    if (flag):
        newBoundingArray.append(copy.deepcopy(boundingBox))
        return newBoundingArray
    
    else:
        return _checkForNewMerges(newBoundingBox,newBoundingArray,threshold)
        
    
    
                
        