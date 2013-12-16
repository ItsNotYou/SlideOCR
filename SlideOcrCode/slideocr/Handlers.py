'''
Created on 08.12.2013

@author: hgessner
'''

class ImageExtraction:
    '''
    Retreives images out of a video stream
    '''

    def process(self, stream, timestamp):
        '''
        Returns a ocr image
        Adds a property keyframe to the image
        '''

class PreProcessing:
    '''
    Pre processing includes edge detection, bounding box detection etc
    '''
    
    def process(self, images):
        '''
        We get multiple ocr images here and return multiple ocr images
        Documents the processing by adding an entry to the images metaHistory property
        '''

class Ocr:
    '''
    Detects the text within each image
    '''
    
    def process(self, images):
        '''
        We get multiple ocr images here and return the images extended by the detected text
        Adds a property text to the image
        '''
    
class PostProcessing:
    '''
    Post processing includes text semantic detection
    '''
    
    def process(self, images):
        '''
        We get all images and return all images extended by some info
        '''
