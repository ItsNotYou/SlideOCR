'''
Created on 08.12.2013

@author: hgessner
'''

class OcrImage:
    '''
    Represents an image on the file system
    May contain properties like position (for bounding boxes), tag (for identification across different ocr engines) or byteRepresentation (for content representation)
    '''
    
    # Dictionary containing a history of operations that were executed on this instance
    metaHistory = {}
    # Path to the image
    path = None
    # Ocr detected text
    text = None
    # Bounding box
    bounding = None


class BoundingBox:
    
    left = 0
    right = 0
    top = 0
    bottom = 0
    