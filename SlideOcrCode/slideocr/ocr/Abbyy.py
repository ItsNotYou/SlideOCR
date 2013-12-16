'''
Created on 16.12.2013

@author: hgessner
'''

from slideocr.Handlers import Ocr
from abbyy.process import process


class AbbyyCloud(Ocr):
    '''
    Uploads all images into the abbyy cloud and retreives the detection result
    '''
    
    def process(self, images):
        for image in images:
            image.text = process(image.path)
        return images;
