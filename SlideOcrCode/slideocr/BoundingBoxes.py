import cv2
import os
import copy
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
    
    def __init__(self,minAreaSize,maxAreaHeight):
        self.minAreaSize = minAreaSize
        self.maxAreaHeight = maxAreaHeight
    
    procName = "boundingBoxing"

    # processing method
    def process(self,images):

        results = []
        for image in images:
            print "Working on", image.path
            
            # apply grayscale filter
            inImage = cv2.imread(image.path)
            grayScale = cv2.cvtColor(inImage, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(image.path, grayScale)
            
            # apply gauss filter
            inImage = cv2.imread(image.path, 0)
            blurImage = cv2.GaussianBlur(inImage, (5, 5), 0)
            cv2.imwrite(image.path, blurImage)
            
            # binarize to white on black
            inImage = cv2.imread(image.path)
            binImage = cv2.adaptiveThreshold(inImage, 255,1,1, 11, 2)
            cv2.imwrite(image.path, binImage)
            
            
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

                        # draw the bounding box on the image
                        cv2.rectangle(inImage, (x, y), (x+width, y+height), (0, 0, 255), 2)
                        
                        # create filename
                        newPath = _createFileName(image.path, ["spaaaaaaaaaaace",self.minAreaSize,self.maxAreaHeight], self.procName)
                        
                        # write image
                        cv2.imwrite(newPath,inImage)
                        
                    boundedImage = copy.deepcopy(image)
                    boundedImage.bounding = BoundingBox()
                    boundedImage.bounding.left = x
                    boundedImage.bounding.top = y
                    boundedImage.bounding.right = x + width
                    boundedImage.bounding.bottom = y + height
                    results.append(boundedImage)
                    
                    print boundedImage.bounding.left, boundedImage.bounding.top, boundedImage.bounding.right, boundedImage.bounding.bottom

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
            
        return results
            
            
# creates the file name of an output image        
def _createFileName(path,argList,procName):
    (head, tail) = os.path.split(path)
    (name, ext) = os.path.splitext(tail)
    add = ""
    for arg in argList:
        add += "_" + str(arg)
    return os.path.join(head,name + "_%s%s" % (procName,add) + ext)
    
   