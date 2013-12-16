import numpy as np
import cv2
import os


#TODO: Dateinamen werden sehr lang bei langer kette
'''
Processor class providing a method to a apply the gaussian filter.

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_filtering/py_filtering.html#gaussian-blurring
Additional Informations: http://docs.opencv.org/modules/imgproc/doc/filtering.html?#gaussianblur

Argument Hints: 
    sigmaX: Gaussian kernel standard deviation in X direction. The higher sigmaX, the stronger the blur effect. 
        Should be a value between 1 and 3. (Standard = 1)
'''
class GaussianBlurring(object):
    
    def __init__(self,sigmaX):
        self.sigmaX = sigmaX
        
    procName = "gaussianBlurring"
    
    # processing method
    def process(self,images): 
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path,1)
        
            # apply filter
            outImage = cv2.GaussianBlur(inImage,(0,0),self.sigmaX)
        
            # create filename
            newPath = _createFileName(image.path, [self.sigmaX], self.procName)
        
            # write image
            cv2.imwrite(newPath,outImage)
            
            # add meta informations
            image.metaHistory.append("%s(sigmaX=%s)" % (self.procName,self.sigmaX))
            
            # modify path
            image.path = newPath
            
        return images
            
            
        
        
        
'''
Processor class providing a method to a apply the bilateral filter. The bilateral filter can reduce unwanted 
noise very well while keeping edges fairly sharp. However, it is very slow compared to most filters.

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_filtering/py_filtering.html#bilateral-filtering
Additional Informations: http://docs.opencv.org/modules/imgproc/doc/filtering.html?#bilateralfilter

Argument Hints:
    sigmaColor: Filter sigma in the color space. A larger value of the parameter means that farther colors within 
        the pixel neighborhood (see sigmaSpace ) will be mixed together, resulting in larger areas of semi-equal color.
        The higher sigmaColor, the stronger the blur effect. (Standard = 75)
'''
class BilateralFiltering(object):
    
    def __init__(self,sigmaColor):
        self.sigmaColor = sigmaColor
    
    procName = "bilateralFiltering"

    # processing method
    def process(self,images):
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path,1)
            
            # apply filter
            outImage = cv2.bilateralFilter(inImage,9,self.sigmaColor,75)
            
            # create filename
            newPath = _createFileName(image.path, [self.sigmaColor], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
            
            # add meta informations
            image.metaHistory.append("%s(sigmaColor=%s)" % (self.procName,self.sigmaColor))
            
            # modify path
            image.path = newPath
            
        return images
        
        
'''
Processor class providing a method to a apply the Simple Thresholding (Binarization). If pixel value is greater than a 
threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#simple-thresholding
Additional Informations: http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html#threshold

Argument Hints:
    thresh: threshold value. (Standard = 120)
'''
class SimpleThresholding(object):
    
    def __init__(self,thresh):
        self.thresh = thresh
    
    procName = "simpleThresholding"

    # processing method
    def process(self,images):
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path,0)
            
            # apply filter
            _,outImage = cv2.threshold(inImage,self.thresh,255,cv2.THRESH_BINARY)
            
            # create filename
            newPath = _createFileName(image.path, [self.thresh], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
        
            # add meta informations
            image.metaHistory.append("%s(thresh=%s)" % (self.procName,self.thresh))
            
            # modify path
            image.path = newPath
            
        return images

        
'''
Processor class providing a method to a apply the Adaptive Thresholding (Adaptive Binarization). The algorithm calculate 
the threshold for a small regions of the image. So we get different thresholds for different regions of the same image 
and it gives us better results for images with varying illumination

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html#adaptive-thresholding
Additional Informations: http://docs.opencv.org/modules/imgproc/doc/miscellaneous_transformations.html#adaptivethreshold

Argument Hints:
    blockSize: Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on. 
        (Standard = 11)
    C: Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero 
        or negative as well. Reduces Noises. (Standard = 2)
'''
class AdaptiveThresholding(object):
    
    def __init__(self,blockSize,C):
        self.blockSize = blockSize
        self.C = C
    
    procName = "adaptiveThresholding"

    # processing method
    def process(self,images):
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path,0)
            
            # apply filter
            outImage = cv2.adaptiveThreshold(inImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blockSize,self.C)
            
            # create filename
            newPath = _createFileName(image.path, [self.blockSize,self.C], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
            
            # add meta informations
            image.metaHistory.append("%s(blockSize=%s,C=%s)" % (self.procName,self.blockSize,self.C))
            
            # modify path
            image.path = newPath
            
        return images
        

'''
Processor class providing a method to a apply the Opening operator. Opening is just another name of erosion followed by 
dilation. It is useful in removing noise. 

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#opening

Argument Hints:
    px: Discarded pixel. (standard = 3)
'''
class Opening(object):
    
    def __init__(self,px):
        self.px = px
    
    procName = "opening"

    # processing method
    def process(self,images):
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path,0)
            
            # apply filter
            kernel = np.ones((self.px,self.px),np.uint8)
            outImage = cv2.morphologyEx(inImage, cv2.MORPH_OPEN, kernel)
            
            # create filename
            newPath = _createFileName(image.path, [self.px], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
            
            # add meta informations
            image.metaHistory.append("%s(px=%s)" % (self.procName,self.px))
            
            # modify path
            image.path = newPath
            
        return images
            

# creates the file name of an output image        
def _createFileName(path,argList,procName):
    (head, tail) = os.path.split(path)
    (name, ext) = os.path.splitext(tail)
    add = ""
    for arg in argList:
        add += "_" + str(arg)
    return os.path.join(head,name + "_%s%s" % (procName,add) + ext)
    
        
        
        
        