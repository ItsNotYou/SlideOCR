import cv2
import os
import copy
import math
from slideocr.Data import BoundingBox

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
            # find external contorus with simple approximation
            inImage = cv2.imread(image.path, 0)
            contours, hierarchy = cv2.findContours(inImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # for every contour
            for contour in contours:

                # if the area is larger than a threshold of minAreaSize
                if cv2.contourArea(contour) > self.minAreaSize:

                    # get coords, width and height of this contour
                    [x, y, width, height] = cv2.boundingRect(contour)

                    # if the contour is smaller than the maxAreaHeight threshold
                    if height < self.maxAreaHeight:
                        
                        '''
                        boundIm = cv2.imread(image.path,1)

                        # draw the bounding box on the image
                        cv2.rectangle(boundIm, (x, y), (x+width, y+height), (0, 0, 255), 2)
                        
                        # write image
                        cv2.imwrite(image.path,boundIm)
                        '''
                        
                        boundedImage = copy.deepcopy(image)
                        boundedImage.bounding = BoundingBox()
                        boundedImage.bounding.left = x
                        boundedImage.bounding.top = y
                        boundedImage.bounding.right = x + width
                        boundedImage.bounding.bottom = y + height
                        results.append(boundedImage)

            '''
            # create filename
            newPath = _createFileName(image.path, [self.minAreaSize,self.maxAreaHeight], self.procName)
            
            # write image
            cv2.imwrite(newPath,inImage)
            
            # add meta informations
            image.metaHistory.append("%s(minAreaSize=%s,maxAreaHeight=%s)" % (self.procName,self.minAreaSize,self.maxAreaHeight))
            
            # modify path
            image.path = newPath
            '''
        
        return self.merge(results)
    
    def merge(self,images):
        
        if len(images) == 0 or len == None:
            return images
        
        oldBoundingsDic = {}
        imageDic = {}
        
        for image in images:
            if image.frameId not in oldBoundingsDic:
                oldBoundingsDic[image.frameId] = [image.bounding]
                imageDic[image.frameId] = image
            else:
                oldBoundingsDic[image.frameId].append(image.bounding)
                
        newBoundingsDic = {}
                
        for frameid,currentBoundings in oldBoundingsDic.iteritems():
                
            newSize = 0
            newBoundings = _mergeHelp(currentBoundings,self.mergeTreshold)
            oldSize = len(newBoundings)
            while (newSize != oldSize):
                oldSize = newSize
                newBoundings = _mergeHelp(newBoundings,self.mergeTreshold)
                newSize = len(newBoundings)
                
            newBoundingsDic[frameid] = newBoundings
            
        newImages = []
        
        for frameid, newBoundings in newBoundingsDic.iteritems():
            image = imageDic[frameid]
            boundIm = cv2.imread(image.path,1)
            for newBounding in newBoundings:
                newImage = copy.deepcopy(image)
                newImage.bounding = newBounding
                newImages.append(newImage)
              
                # draw the bounding box on the image
                cv2.rectangle(boundIm, (newBounding.left, newBounding.top), (newBounding.right, newBounding.bottom), (0, 0, 255), 2)
                
            cv2.imwrite(image.path,boundIm)
            
        return newImages
            
# creates the file name of an output image        
def _createFileName(path,argList,procName):
    (head, tail) = os.path.split(path)
    (name, ext) = os.path.splitext(tail)
    add = ""
    for arg in argList:
        add += "_" + str(arg)
    return os.path.join(head,name + "_%s%s" % (procName,add) + ext)


def _mergeHelp(oldBoundings,threshold):
    
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
    
   