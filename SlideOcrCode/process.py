'''
Created on 08.12.2013

@author: hgessner
'''

import sys
import slideocr.ArgumentValidator as Validator
from parameter_parser import ParameterParser
from slideocr.PreProcessors import PreProcessors
from slideocr.ocr.OcrEngines import OcrEngines
from slideocr.VideoExtractor import VideoExtractor, ImageExtractor, MySqlVideoExtractor,\
    ZipExtractor
from slideocr.BoundingBoxes import BoundingBoxing
from slideocr.TextClassificator import TextClassificator
import zipfile


def recognizeFile(extractor, skipAbbyy, skipTesseract, preProcessingBounding, preProcessingOCR, tesseractLanguage, args):
    
    '''
    Extract images
    '''
    images = extractor.extract();
    
    '''
    Save original paths for later OCR pre processing
    '''
    originalPaths = {}
    for image in images:
        originalPaths[image.frameId] = image.path
    
    '''
    Preprocessing for bounding
    '''
    pre = PreProcessors(args)
    if preProcessingBounding != None:
        images = executePreprocessing(pre.prepro_dict, preProcessingBounding, images)
    
    
    '''
    Bounding
    '''
    bound=BoundingBoxing(args.minAreaSize, args.maxAreaHeight, args.mergeThreshold)
    images=bound.process(images)
    
    
    '''
    Restore original paths for OCR pre processing
    '''
    for image in images:
        image.path = originalPaths[image.frameId]
    
    '''
    Preprocessing for OCR
    '''
    if preProcessingOCR != None:
        images = executePreprocessing(pre.prepro_dict, preProcessingOCR, images)
    
    '''
    OCR
    '''
    ocr = OcrEngines(skipAbbyy, skipTesseract, tesseractLanguage)
    images = ocr.process(images)
    
    '''
    Simple post filter process: Remove empty text
    '''
    nonEmptyImages = []
    for image in images:
        if image.text:
            nonEmptyImages.append(image)
            
    '''
    Text classification
    '''
    classificator = TextClassificator(args.heightOffset)
    classificator.classify(nonEmptyImages)
            
    '''
    Write result into source
    '''
    extractor.write(nonEmptyImages)
    
    
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
    isVideoId = args.isVideoId
    skipAbbyy = args.skipAbbyy
    skipTesseract=args.skipTesseract
    preProcessingBounding=args.preProcessingBounding
    preProcessingOCR=args.preProcessingOCR
    tesseractLanguage=args.tesseractLanguage
    
    extractor = None
    if isVideoId:
        extractor = MySqlVideoExtractor(workingDirectory, sourceFile)
    elif split != None:
        extractor = VideoExtractor(workingDirectory, sourceFile, split)
    elif zipfile.is_zipfile(sourceFile):
        extractor = ZipExtractor(workingDirectory, sourceFile)
    else:
        extractor = ImageExtractor(workingDirectory, sourceFile)
    
    recognizeFile(extractor, skipAbbyy, skipTesseract, preProcessingBounding, preProcessingOCR, tesseractLanguage, args)
