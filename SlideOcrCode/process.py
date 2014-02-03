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
from ConfigParser import ConfigParser
import zipfile
import shlex
import argparse
from slideocr.Helper import FileNameCreator
import os
import warnings


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
    bound=BoundingBoxing(args.minAreaSize, args.maxAreaHeight, args.mergeThreshold,args.boxWideningValue)
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
    ocr = OcrEngines(skipAbbyy, skipTesseract, tesseractLanguage, args.abbyyBatchSize)
    images = ocr.process(images)
    
    '''
    Simple post filter process: Remove empty text
    '''
    nonEmptyImages = []
    for image in images:
        if image.text.strip():
            nonEmptyImages.append(image)
    
    '''
    Text classification
    '''
    classificator = TextClassificator(args.heightOffset)
    classificator.classify(nonEmptyImages)
     
    '''
    Sort List
    '''
    sortedNonEmptyImages = sorted(nonEmptyImages,cmp=compare)
            
    '''
    Write result into source
    '''
    extractor.write(sortedNonEmptyImages)
    
    '''
    Clean up workspace
    '''
    if not args.skipCleanup:
        for created in FileNameCreator.rememberedFilenames:
            if os.path.exists(created):
                os.remove(created)
    
    
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

def compare(ocrImage1,ocrImage2):
    if (ocrImage1.tag < ocrImage2.tag):
        return -1
    elif (ocrImage1.tag > ocrImage2.tag):
        return 1
    else:
        if (ocrImage1.bounding.top < ocrImage2.bounding.top):
            return -1
        elif (ocrImage1.bounding.top > ocrImage2.bounding.top):
            return 1
        else:
            if (ocrImage1.bounding.left < ocrImage2.bounding.left):
                return -1
            elif (ocrImage1.bounding.left > ocrImage2.bounding.left):
                return 1
            else:
                return 0
        
            


#determine source of arguments
#parse parameter to check for config file
parser = argparse.ArgumentParser(description="Extract text from a video stream of lecture slides", add_help=False)
ParameterParser.add_config_file(parser)
(args, unknown_args) = parser.parse_known_args(sys.argv[1:])

argument_list=[]

#if config file is given append options from config file
if args.configFile != None:
    config = ConfigParser()
    config.read(args.configFile)
    config_value = config.get('config', 'options')
    argument_list.extend(shlex.split(config_value))

#append arguments from commandline    
argument_list.extend(sys.argv[1:])

parser = ParameterParser()

(args, unknown_args)=parser.parse(argument_list)

#warn of unknown args
for arg in unknown_args:
    warnings.warn("Unknown command line argument %s" % arg)

#assign parameters and execute program if arguments are validated
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
