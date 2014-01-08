import cv2
import copy
import math
from slideocr.Data import BoundingBox
from slideocr.Helper import FileNameCreator

'''
Processor class providing a method to a apply bounding boxes on text areas. The algorithm works best on canny edge outputs, 
which are binarized as white-on-black images. It is based on finding all contours and combining them like the min and max area size tresholds allows.
As result you get only the external boxes, which have no superset.

Sources: 
http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#findcontours
http://docs.opencv.org/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#boundingrect
http://docs.opencv.org/modules/core/doc/drawing_functions.html#rectangle

Additional Informations: 
http://stackoverflow.com/questions/9413216/simple-digit-recognition-ocr-in-opencv-python
http://opencvpython.blogspot.de/2012/04/contour-features.html


Argument Hints:
    minAreaSize: Minimal size of a text area. For detecting small characters use a small value, but you will get quite more boxes as result. 
        (Standard = 20)
    maxAreaHeight: Maximal height of a text area. For detecting large characters, use a large value, but than lines with small characters 
        will be combined in one box, if the sum of their heights is smaller than this maxAreaHeight. (Standard = 100)
    mergeTreshold: Defines how close a bounding boxes has to be to each other to be merged. (Standard = 50)
        
'''
class BoundingBoxing(object):
    
    def __init__(self,minAreaSize,maxAreaHeight,mergeTreshold):
        self.minAreaSize = minAreaSize
        self.maxAreaHeight = maxAreaHeight
        self.mergeTreshold = mergeTreshold
    
    procName = "boundingBoxing"

    # processing method
    def process(self,images):

        results = []
        for image in images:
            # find external contours with simple approximation
            inImage = cv2.imread(image.path, 0)
            contours, hierarchy = cv2.findContours(inImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # for every contour
            for contour in contours:

                # if the area is larger than a threshold of minAreaSize
                if cv2.contourArea(contour) > self.minAreaSize:

                    # get coordinates, width and height of this contour
                    [x, y, width, height] = cv2.boundingRect(contour)

                    # if the contour is smaller than the maxAreaHeight threshold
                    if height < self.maxAreaHeight:
                        
                        # create new image for every bounding box
                        boundedImage = copy.deepcopy(image)
                        boundedImage.bounding = BoundingBox()
                        boundedImage.bounding.left = x
                        boundedImage.bounding.top = y
                        boundedImage.bounding.right = x + width
                        boundedImage.bounding.bottom = y + height
                        results.append(boundedImage)
        
        # merge the resulting bounding boxes and return them
        return self.merge(results)
    
    '''
    This method merges bounding boxes in the same image, if they are close to each other
    '''
    def merge(self,images):
        
        # return if images is empty or has no value
        if len(images) == 0 or len == None:
            return images
        
        # dictionary for mapping a frame id to a list of bounding boxes found in the corresponding image
        oldBoundingsDic = {}
        # dictionary mapping a frame id to one OcrImage instances with this id
        imageDic = {}
        
        # fill dictionaries
        for image in images:
            if image.frameId not in oldBoundingsDic:
                oldBoundingsDic[image.frameId] = [image.bounding]
                imageDic[image.frameId] = image
            else:
                oldBoundingsDic[image.frameId].append(image.bounding)
        
        # dictionary for mapping a frame id to a new list of bounding boxes found in the corresponding image        
        newBoundingsDic = {}
                
        # iterate over all images and there boundings
        for frameid,currentBoundings in oldBoundingsDic.iteritems():
            
            # variables to compare the count of bounding boxes before and after a merge call
            oldSize = 0
            newSize = len(currentBoundings)
            
            # merge until the number of bounding boxes does not change
            while (newSize != oldSize):
                oldSize = newSize
                currentBoundings = _mergeHelp(currentBoundings,self.mergeTreshold)
                newSize = len(currentBoundings)
              
            # add new bounding boxes  
            newBoundingsDic[frameid] = currentBoundings
        
        # array for the images with the new boundings    
        newImages = []
        
        # add images with new boundings to list and create a file for each image
        for frameid, newBoundings in newBoundingsDic.iteritems():
            # get the image
            image = imageDic[frameid]
            # read the current image
            boundIm = cv2.imread(image.path,1)
            # modify path
            image.path = FileNameCreator.createFileName(image.path, [self.minAreaSize,self.maxAreaHeight,self.mergeTreshold], self.procName)
            # add meta informations
            image.metaHistory.append("%s(minAreaSize=%s,maxAreaHeight=%s,mergeTreshold=%s)" % (self.procName,self.minAreaSize,self.maxAreaHeight,self.mergeTreshold))
            
            # create new image for each bound and draw the bounds on the image
            for newBounding in newBoundings:
                newImage = copy.deepcopy(image)
                newImage.bounding = newBounding
                newImages.append(newImage)
              
                # draw the bounding box on the image
                cv2.rectangle(boundIm, (newBounding.left, newBounding.top), (newBounding.right, newBounding.bottom), (0, 0, 255), 2)
                
            # write the new image
            cv2.imwrite(image.path,boundIm)
         
        # return the images with the new bounds   
        return newImages

'''
This method merges a bounding box if it is close enough to another bounding box.
'''
def _mergeHelp(oldBoundings,threshold):
    
    # current bounding boxes
    currentBoundingArray = []

    # iterate through all old bounding boxes 
    for oldBounding in oldBoundings:
        
        # reset array of new bounding boxes
        newBoundingArray = []
        
        # flag to indicate whether boxes where merged 
        merged = False
        
        # iterate through all current boundings
        for currentBounding in currentBoundingArray:
            
            # check if two bounding boxes are next to each other
            if ((_nextTo(currentBounding,oldBounding,threshold) or _overlaps(currentBounding,oldBounding)) and _inSameLine(currentBounding,oldBounding)):
                
                # calculate new bounding box (merge)
                newBoundingBox = BoundingBox()
                newBoundingBox.left = min(currentBounding.left,oldBounding.left)
                newBoundingBox.right = max(currentBounding.right,oldBounding.right)
                newBoundingBox.top = min(currentBounding.top,oldBounding.top)
                newBoundingBox.bottom = max(currentBounding.bottom,oldBounding.bottom)
                
                # append new bounding box
                newBoundingArray.append(newBoundingBox)
                
                # indicate that boxes where merged
                merged = True
            
            # if there is no box close enough, add current bounding without merging  
            else:
                newBoundingArray.append(currentBounding)
        
        # if boxes are not merged append also old bounding
        if (not merged):
            newBoundingArray.append(copy.deepcopy(oldBounding))
            
        # replace current boundings with new boundings    
        currentBoundingArray = newBoundingArray;
        # reset flag
        merged = False     
        
    # return new boundings
    return currentBoundingArray         
                
'''
checks whether to bounding boxes are close according to a threshold value and the x coordinates
'''
def _nextTo(bounding1,bounding2,threshold):
    
    if (math.fabs(bounding1.right - bounding2.left) < threshold or \
        math.fabs(bounding2.right - bounding1.left) < threshold ):
        
        return True
    
    return False               

'''
checks whether to bounding boxes a close to each other according to the y coordinates
'''
def _inSameLine(bounding1,bounding2):
    
    if (bounding1.top >= bounding2.top and bounding1.top <= bounding2.bottom or \
        bounding2.top >= bounding1.top and bounding2.top <= bounding1.bottom):
        
        return True
    
    return False

'''
checks whether to bounding boxes overlapping each other
'''
def _overlaps(bounding1,bounding2):
    if (bounding1.left >= bounding2.left and bounding1.left <= bounding2.right or \
        bounding1.right >= bounding2.left and bounding1.right <= bounding2.right or \
        bounding2.left >= bounding1.left and bounding2.left <= bounding1.right or \
        bounding2.right >= bounding1.left and bounding2.right <= bounding1.right):
        
        return True
    
    return False
    