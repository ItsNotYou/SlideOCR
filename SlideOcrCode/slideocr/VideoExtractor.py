'''
Created on 16.12.2013

@author: hgessner
'''

import shutil
import subprocess
import uuid
import os
import numpy
from slideocr.Data import OcrImage


class FrameTimestamp:
    
    tag = None
    minutes = 0.
    seconds = 0.
    videoPath = None


class TableReader:
    
    def mapRowsToTimestamps(self, rows):
        result = []
        for row in rows:
            frame = FrameTimestamp()
            frame.tag = str(int(row[0]))
            frame.minutes = row[1]
            frame.seconds = row[2]
            result.append(frame)
        return result
    
    
    def appendVideoPath(self, timestamps, videoPath):
        for timestamp in timestamps:
            timestamp.videoPath = videoPath
        return timestamps
    
    
    def readTable(self, pathToTable):
        return numpy.loadtxt(pathToTable, skiprows = 1)
    
    
    def readTimestamps(self, pathToTable, pathToVideo):
        '''
        Takes a path to a timestamp table and a video path and returns an array of frame timestamps
        '''
        table = self.readTable(pathToTable)
        timestamps = self.mapRowsToTimestamps(table)
        return self.appendVideoPath(timestamps, pathToVideo)


class FrameExtractor:
    
    procPath = "ffmpeg"
    pathToWorkspace = None
    slowSearchDelta = 10
    
    def __init__(self, pathToWorkspace):
        self.pathToWorkspace = pathToWorkspace
        
        
    def mapTimestampsToFrames(self, timestamps):
        results = []
        for timestamp in timestamps:
            seconds = timestamp.minutes * 60 + timestamp.seconds
            tag = timestamp.tag
            sourcePath = timestamp.videoPath
            targetPath = self._createFileName(tag, '.png')
            self.extractFrame(seconds, sourcePath, targetPath);
            
            ocrImage = OcrImage()
            ocrImage.path = targetPath
            results.append(ocrImage)
        return results;
    
    
    def extractFrame(self, seconds, sourcePath, targetPath):
        # Does a fast and accurate seeking for the specified timestamp. For details see https://trac.ffmpeg.org/wiki/Seeking%20with%20FFmpeg
        subprocess.call([self.procPath, "-loglevel", "warning", "-ss", str(seconds - self.slowSearchDelta), "-i", sourcePath, "-ss", str(self.slowSearchDelta), "-vframes", "1", targetPath]);
        
        
    def _createFileName(self, prefix, extension):
        # creates the file name of an output image        
        uniqueId = uuid.uuid4()
        return os.path.join(self.pathToWorkspace, prefix + "_" + str(uniqueId) + extension)


class ExtractionHelper:
    '''
    Combines several helper functions for easy frame creation or extraction. The helper functions always return an array of ocr images
    '''
    
    def convertSingleImage(self, imagePath, workingDirectory):
        targetFile = os.path.join(workingDirectory, os.path.basename(imagePath));
        shutil.copyfile(imagePath, targetFile)
        
        images = [OcrImage()]
        images[0].path = targetFile
        return images
    
    
    def convertVideoByTable(self, videoPath, tablePath, workingDirectory):
        timestamps = TableReader().readTimestamps(tablePath, videoPath)
        images = FrameExtractor(workingDirectory).mapTimestampsToFrames(timestamps)
        return images
    

class VideoExtractor:
    
    workingDirectory = None
    videoPath = None
    splitPath = None
    
    def __init__(self, workingDirectory, videoPath, splitPath):
        self.workingDirectory = workingDirectory
        self.videoPath = videoPath
        self.splitPath = splitPath
        
    def extract(self):
        return ExtractionHelper().convertVideoByTable(self.videoPath, self.splitPath, self.workingDirectory)
    
    
class ImageExtractor:
    
    workingDirectory = None
    imagePath = None
    
    def __init__(self, workingDirectory, imagePath):
        self.workingDirectory = workingDirectory
        self.imagePath = imagePath
        
    def extract(self):
        return ExtractionHelper().convertSingleImage(self.imagePath, self.workingDirectory)
    