'''
Created on 17.12.2013

@author: hgessner
'''

import copy
from slideocr.Handlers import Ocr
from slideocr.ocr.Tesseract import Tesseract
from slideocr.ocr.Abbyy import AbbyyCloud


class OcrEngines(Ocr):
    '''
    Combines several ocr engines
    '''
    
    engines = []
    
    def __init__(self, skipAbbyy = False):
        self.engines.append(Tesseract())
        if not skipAbbyy:
            self.engines.append(AbbyyCloud())
    
    
    def process(self, images):
        result = []
        for engine in self.engines:
            engineImages = copy.deepcopy(images)
            engineImages = engine.process(engineImages)
            result.extend(engineImages)
        return result
    