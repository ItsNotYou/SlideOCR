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
    metaHistory = []
    # Path to the image
    path = None
    # Ocr detected text
    text = None
    # Bounding box
    bounding = None
    # Globally unique frame id that identifies an image or subimage of a video frame
    frameId = None
    # Human understandble description of the type of the detected text (caption, footer etc.)
    contentType = None
    
    def __str__(self):
        return 'FrameId: %s Path: "%s" Bounding: %s' % (self.frameId, self.path, self.bounding)


class BoundingBox:
    
    left = 0
    right = 0
    top = 0
    bottom = 0
    
    def __str__(self):
        return "[%d %d %d %d]" % (self.left, self.top, self.right, self.bottom)
    
    
class FrameTimestamp:
    
    tag = None
    minutes = 0.
    seconds = 0.
    videoPath = None
    