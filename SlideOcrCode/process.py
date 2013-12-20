'''
Created on 08.12.2013

@author: hgessner
'''

from parameter_parser import ParameterParser
from slideocr.PreProcessors import *
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor, ImageExtractor
from slideocr.BoundingBoxes import *

import sys

def recognizeFile(extractor, skipAbbyy, preProcessingBounding, preProcessingOCR, args):
    
    '''
    Extract images
    '''
    images = extractor.extract();
    
    
    
    '''
    Preprocessing for bounding
    '''
    pre = PreProcessors(args)
    if preProcessingBounding != None:
        images = executePreprocessing(pre.prepro_dict, preProcessingBounding, images)
    
    
    '''
    Bounding
    '''
        
    bound=BoundingBoxing(args.minAreaSize, args.maxAreaSize)
    images=bound.process(images)
    
    '''
    Preprocessing for OCR
    '''
    if preProcessingOCR != None:
        images = executePreprocessing(pre.prepro_dict, preProcessingOCR, images)
    
    
    
    '''
    OCR
    '''
    ocr = OcrEngines(skipAbbyy)
    images = ocr.process(images)
    for image in images:
        print image.text
        
        
def executePreprocessing(processors, steps, images):
    '''
    Method for chaining several preprocessing steps.
    Input:
        processors: Dictionary with preprocessor instances
        steps: String list with procnames of preprocessors to be used in order
        images: OCRimage objects to be processed
    Output:
        List of OCRimage objects after processing steps
    '''
    print steps
    
    for step in steps:
        if step in processors:
            images = processors[step].process(images)
        else:
            sys.stderr.write("Unknown preprocessor "+step+". Available preprocessors are: " + str(processors.keys())+"\n")
            sys.exit("Unknown input.\n")

parser = ParameterParser()

#parse parameter
(args,unknown_args) = parser.parse(sys.argv[1:])

workingDirectory = args.workingDirectory
sourceFile = args.sourceFile
split = args.extraction
skipAbbyy = args.skipAbbyy
preProcessingBounding=args.preProcessingBounding
preProcessingOCR=args.preProcessingOCR

extractor = None
if split == None:
    extractor = ImageExtractor(workingDirectory, sourceFile)
else:
    extractor = VideoExtractor(workingDirectory, sourceFile, split)

recognizeFile(extractor, skipAbbyy, preProcessingBounding, preProcessingOCR, args)
