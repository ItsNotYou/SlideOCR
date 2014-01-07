'''
Created on 19.12.2013

@author: wanko
'''

import argparse

class ParameterParser(object):
    
    def __init__(self):
        ''' Constructor '''
        self.__parser = argparse.ArgumentParser(description="Extract text from a video stream of lecture slides")
        
        main_group = self.__parser.add_argument_group("General")
        main_group.add_argument('--workingDirectory', dest='workingDirectory', action='store', default='.', help='Path to a directory that will be used as temporary workspace')   
        main_group.add_argument("--sourceFile", required=True, dest='sourceFile', action='store', help = "Path to an image or video file that will be processed. Video files require the option -e")
        main_group.add_argument("-e", "--extraction", dest='extraction', action='store', help = "Path to a file that contains the frame extraction data")
        main_group.add_argument("--videoId", dest='isVideoId', action='store_true', help = "Set if sourceFile is an ID of a video that contains the frame extraction data")
        main_group.add_argument("--skipAbbyy", dest='skipAbbyy', help="skips ABBYY Cloud OCR processing", action="store_true")
        main_group.add_argument("--skipTesseract", dest='skipTesseract', help="skips Tesseract OCR processing", action="store_true")
        main_group.add_argument('--preProcessingBounding', dest='preProcessingBounding', nargs='+', action='store', help='List of pre processing steps that are executed to enhance image quality for bounding box algorithms.')
        main_group.add_argument('--preProcessingOCR', dest='preProcessingOCR', nargs='+', action='store', help='List of pre processing steps that are executed to enhance image quality for OCR runs.')
        
        gauss_group = self.__parser.add_argument_group("gaussianBlurring")
        gauss_group.add_argument('--sigmaX', dest='sigmaX', type=float, action='store', default=0, help='Gaussian kernel standard deviation in X direction. The higher sigmaX, the stronger the blur effect. Should be a value between 0 and 3.')
        
        bil_group = self.__parser.add_argument_group("bilateralFiltering")
        bil_group.add_argument('--sigmaColor', dest='sigmaColor', type=float, action='store', default=75, help='Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood (see sigmaSpace ) will be mixed together, resulting in larger areas of semi-equal color.The higher sigmaColor, the stronger the blur effect.')
        
        thres_group = self.__parser.add_argument_group("simpleThresholding")
        thres_group.add_argument('--thresh', dest='thresh', type=float, action='store', default=120, help='threshold value.')
        
        adthres_group = self.__parser.add_argument_group("adaptiveThresholding")
        adthres_group.add_argument('--blockSize', dest='blockSize', type=int, action='store', default=11, help='Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.')
        adthres_group.add_argument('--C', dest='C', type=float, action='store', default=2, help='Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well. Reduces Noises.')
   
        opening_group = self.__parser.add_argument_group("opening")
        opening_group.add_argument('--px', dest='px', type=int, action='store', default=3, help='Discarded pixel.')
        
        interpol_group = self.__parser.add_argument_group("Interpolation")
        interpol_group.add_argument('--interpolationMode', dest='interpolationMode', default="nearest", choices=["nearest", "bicubic", "bilinear"], action='store', help='Discarded pixel.')
        
        bounding_group = self.__parser.add_argument_group("BoundingBoxes")
        bounding_group.add_argument('--minAreaSize', dest='minAreaSize', type=int, default=20, action='store', help='Minimal size of a text area. For detecting small characters use a small value, but you will get quite more boxes as result. ')
        bounding_group.add_argument('--maxAreaHeight', dest='maxAreaHeight', type=int, default=100, action='store', help='Maximal height of a text area. For detecting large characters, use a large value, but than lines with small characters will be combined in one box, if the sum of their heights is smaller than this maxAreaHeight. ')
        bounding_group.add_argument('--mergeThreshold', dest='mergeThreshold', type=int, default=50, action='store', help='Merging threshold to combine bounding boxes.')
        
   
   
    def parse(self, args):
        '''
            returns argparse object to parse command line arguments
            Args:
                args: _sys.argv[1:]
            Returns:
                argparese object
        '''
        return self.__parser.parse_known_args(args)
