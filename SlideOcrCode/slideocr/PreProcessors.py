import numpy as np
import cv2
from slideocr.Handlers import PreProcessing
from slideocr.Helper import FileNameCreator

class PreProcessors(PreProcessing):
    '''
    Combines all pre processing steps
    '''
    
    prepro_dict={}
    
    def __init__(self,args):
        self.gaussianBlurring = GaussianBlurring(args.sigmaX)
        self.prepro_dict[self.gaussianBlurring.procName] = self.gaussianBlurring
        
        self.bilateralFiltering = BilateralFiltering(args.sigmaColor)
        self.prepro_dict[self.bilateralFiltering.procName] = self.bilateralFiltering
        
        self.simpleThresholding = SimpleThresholding(args.thresh)
        self.prepro_dict[self.simpleThresholding.procName] = self.simpleThresholding
        
        self.adaptiveThresholding = AdaptiveThresholding(args.blockSize, args.C)
        self.prepro_dict[self.adaptiveThresholding.procName] = self.adaptiveThresholding
        
        self.opening = Opening(args.px)
        self.prepro_dict[self.opening.procName] = self.opening
        
        self.nearestInterpolation = NearestInterpolation()
        self.prepro_dict[self.nearestInterpolation.procName] = self.nearestInterpolation
        
        self.bicubicInterpolation = BicubicInterpolation()
        self.prepro_dict[self.bicubicInterpolation.procName] = self.bicubicInterpolation
        
        self.bilinearInterpolation = BilinearInterpolation()
        self.prepro_dict[self.bilinearInterpolation.procName] = self.bilinearInterpolation
        
        self.antialiasInterpolation = AntialiasInterpolation()
        self.prepro_dict[self.antialiasInterpolation.procName] = self.antialiasInterpolation
        
        self.interpolation = Interpolation(args.interpolationMode)
        self.prepro_dict[self.interpolation.procName] = self.interpolation
        
        self.grayscaleFilter = GrayscaleFilter()
        self.prepro_dict[self.grayscaleFilter.procName] = self.grayscaleFilter
    
    def process(self, images):
        if self.bilateralFiltering:
            images = self.bilateralFiltering.process(images)
        return images
    

#TODO: Dateinamen werden sehr lang bei langer kette
'''
Processor class providing a method to a apply the gaussian filter.

Source: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_filtering/py_filtering.html#gaussian-blurring
Additional Informations: http://docs.opencv.org/modules/imgproc/doc/filtering.html?#gaussianblur

Argument Hints: 
    sigmaX: Gaussian kernel standard deviation in X direction. The higher sigmaX, the stronger the blur effect. 
        Should be a value between 0 and 3. (Standard = 0)
'''
class GaussianBlurring(object):
    
    def __init__(self,sigmaX):
        self.sigmaX = sigmaX
        
    procName = "gaussianBlurring"
    
    # processing method
    def process(self,images): 
        
        for image in images:
            # read in image
            inImage = cv2.imread(image.path)
        
            # apply filter
            outImage = cv2.GaussianBlur(inImage,(5,5),self.sigmaX)
        
            # create filename
            newPath = FileNameCreator.createFileName(image.path, [self.sigmaX], self.procName)
        
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
            newPath = FileNameCreator.createFileName(image.path, [self.sigmaColor], self.procName)
            
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
            newPath = FileNameCreator.createFileName(image.path, [self.thresh], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
        
            # add meta informations
            image.metaHistory.append("%s(thresh=%s)" % (self.procName,self.thresh))
            
            # modify path
            image.path = newPath
            
        return images


class GrayscaleFilter(object):
    
    procName = "grayscaleFilter"

    # processing method
    def process(self,images):
        
        for image in images:
            # create filename
            newPath = FileNameCreator.createFileName(image.path, [], self.procName)
            
            # apply grayscale filter
            inImage = cv2.imread(image.path)
            outImage = cv2.cvtColor(inImage, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(newPath, outImage)

            # add meta informations
            image.metaHistory.append("%s" % self.procName)
            
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
            outImage = cv2.adaptiveThreshold(inImage,255,1,1,self.blockSize,self.C)
            
            # create filename
            newPath = FileNameCreator.createFileName(image.path, [self.blockSize,self.C], self.procName)
            
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
            newPath = FileNameCreator.createFileName(image.path, [self.px], self.procName)
            
            # write image
            cv2.imwrite(newPath,outImage)
            
            # add meta informations
            image.metaHistory.append("%s(px=%s)" % (self.procName,self.px))
            
            # modify path
            image.path = newPath
            
        return images
    
        

'''
Processor class providing a method to apply different interpolation. Interpolation is used to smooth edges and reduce noise.

Additional Informations: http://matplotlib.org/users/image_tutorial.html?highlight=set_interpolation

Argument Hints:
    interpolationMode: Type of interpolation used on the images.
'''

import Image
import sys

class Interpolation(object):
    
    procName = "interpolation"
    interpolationMode = ""
    modes=["nearest", "bicubic", "bilinear", "antialias"]
    
    def __init__(self, interpolationMode):
        if interpolationMode not in self.modes:
            sys.stderr.write("Unknown image interpolation mode.\n")
            sys.exit("Unknown input.\n")
        self.interpolationMode = interpolationMode

    # processing method
    def process(self,images):
        
        for image in images:
            # read in image and apply interpolation
            im = Image.open(image.path)
            width = im.size[0]/2
            height = im.size[1]/2
            
            if self.interpolationMode == "nearest":
                im = im.resize((width, height), Image.NEAREST)
                im = im.resize((width*2, height*2), Image.NEAREST)
            elif self.interpolationMode == "bicubic":
                im = im.resize((width, height), Image.BICUBIC)
                im = im.resize((width*2, height*2), Image.BICUBIC)
            elif self.interpolationMode == "bilinear":
                im = im.resize((width, height), Image.BILINEAR)
                im = im.resize((width*2, height*2), Image.BILINEAR)
            elif self.interpolationMode == "antialias":
                im = im.resize((width, height), Image.ANTIALIAS)
                im = im.resize((width*2, height*2), Image.ANTIALIAS)
            
            # create filename
            newPath = FileNameCreator.createFileName(image.path, [self.interpolationMode], self.procName)
            
            # write image 
            im.save(newPath)    
            
            # add meta informations
            image.metaHistory.append("%s(interpolationMode=%s)" % (self.procName,self.interpolationMode))
            
            # modify path
            image.path = newPath

            
        return images
    

class NearestInterpolation(object):
    
    procName = "nearestInterpolation"
    _subprocessor=None
    
    def __init__(self):
        self._subprocessor=Interpolation("nearest")

    # processing method
    def process(self,images):      
        return self._subprocessor.process(images)
        

class BicubicInterpolation(object):
    
    procName = "bicubicInterpolation"
    _subprocessor=None
    
    def __init__(self):
        self._subprocessor=Interpolation("bicubic")

    # processing method
    def process(self,images):      
        return self._subprocessor.process(images)
        

class BilinearInterpolation(object):
    
    procName = "bilinearInterpolation"
    _subprocessor=None
    
    def __init__(self):
        self._subprocessor=Interpolation("bilinear")

    # processing method
    def process(self,images):      
        return self._subprocessor.process(images)
    
    
class AntialiasInterpolation(object):
    
    procName = "antialiasInterpolation"
    _subprocessor=None
    
    def __init__(self):
        self._subprocessor=Interpolation("antialias")

    # processing method
    def process(self,images):      
        return self._subprocessor.process(images)
    
    
    
'''
Reflection maybe needed for later usage.
Discarded because of varying parameters.
'''        
   
import inspect

def print_preprocessors():
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "procName"):
            print obj.procName
            
def get_preprocessors():
    prepro_list=[]
    for _, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "procName"):
            prepro_list.append(obj)
    return prepro_list

  
        