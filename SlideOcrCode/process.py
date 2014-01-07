'''
Created on 08.12.2013

@author: hgessner
'''

from parameter_parser import ParameterParser
from slideocr.PreProcessors import PreProcessors
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor, ImageExtractor
from slideocr.BoundingBoxes import *
import slideocr.ArgumentValidator as Validator

import sys

def recognizeFile(extractor, skipAbbyy, skipTesseract, preProcessingBounding, preProcessingOCR, args):
    
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
        
    bound=BoundingBoxing(args.minAreaSize, args.maxAreaHeight)
    images=bound.process(images)
    
    
    '''
    Preprocessing for OCR
    '''
    if preProcessingOCR != None:
        images = executePreprocessing(pre.prepro_dict, preProcessingOCR, images)
    
    '''
    OCR
    '''
    ocr = OcrEngines(skipAbbyy, skipTesseract)
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
    for step in steps:
        if step in processors:
            images = processors[step].process(images)
        else:
            sys.stderr.write("Unknown preprocessor "+step+". Available preprocessors are: " + str(processors.keys())+"\n")
            sys.exit("Unknown input.\n")
    
    return images  

            

parser = ParameterParser()

#parse parameter
(args,unknown_args) = parser.parse(sys.argv[1:])

if (Validator.validateArguments(args)):
    workingDirectory = args.workingDirectory
    sourceFile = args.sourceFile
    split = args.extraction
    skipAbbyy = args.skipAbbyy
    skipTesseract=args.skipTesseract
    preProcessingBounding=args.preProcessingBounding
    preProcessingOCR=args.preProcessingOCR
    
    extractor = None
    if split == None:
        extractor = ImageExtractor(workingDirectory, sourceFile)
    else:
        extractor = VideoExtractor(workingDirectory, sourceFile, split)
    
    recognizeFile(extractor, skipAbbyy, skipTesseract, preProcessingBounding, preProcessingOCR, args)
