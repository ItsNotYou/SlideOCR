'''
Created on 08.12.2013

@author: hgessner
'''

class OcrImage:
    '''
    Represents an image. It doesn't matter whether it is stored as a stream timestamp, an in memory object or a file
    May contain properties like position (for bounding boxes), tag (for idetification across different ocr engines) or byteRepresentation (for content representation)
    '''
    
    def __init__(self):
        # Dictionary containing a history of operations that were executed on this instance
        self.metaHistory = {};
    
    def asBytes(self):
        '''
        Image content as byte array
        '''
