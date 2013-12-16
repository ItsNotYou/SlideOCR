'''
Created on 16.12.2013

@author: hgessner
'''

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
    
    
    def readTable(self, pathToTable):
        return numpy.loadtxt(pathToTable)
    
    
    def readTimestamps(self, pathToTable, pathToVideo):
        '''
        Takes a path to a timestamp table and a video path and returns an array of frame timestamps
        '''
        table = self.readTable(pathToTable)
        timestamps = self.mapRowsToTimestamps(table)
        return { 'timestamps': timestamps, 'videoPath': pathToVideo}


class FrameExtractor:
    
    procPath = "ffmpeg"
    pathToWorkspace = None
    prefix = "%06d"
    prefixLength = 6
    
    def __init__(self, pathToWorkspace):
        self.pathToWorkspace = pathToWorkspace
        
        
    def mapTimestampsToFrames(self, timestamps):
        sourcePath = timestamps['videoPath']
        targetPath = self._createFileName(self.prefix, ".png")
        self.extractFrames(sourcePath, targetPath)
        
        results = []
        for timestamp in timestamps['timestamps']:
            seconds = timestamp.minutes * 60 + timestamp.seconds
            usedPath = self.replacePrefix(targetPath, str(int(seconds)));
            
            if not os.path.isfile(usedPath):
                raise Exception(usedPath + " could not be found")
            
            ocrImage = OcrImage()
            ocrImage.path = usedPath
            results.append(ocrImage)
        return results;
    
    
    def replacePrefix(self, fullPath, replaceWith):
        replaceLength = len(replaceWith)
        if replaceLength > self.prefixLength:
            raise Exception("PrefixLength must more longer that ReplaceLength")
        
        for count in range(0, self.prefixLength - replaceLength):
            replaceWith = "0" + replaceWith
        
        return fullPath.replace(self.prefix, replaceWith)
        
    
    def extractFrame(self, seconds, sourcePath, targetPath):
        subprocess.call([self.procPath, "-ss", str(seconds), "-i", sourcePath, "-ss", str(seconds), "-vframes", "1", targetPath]);
        
        
    def extractFrames(self, sourcePath, targetPath):
        subprocess.call([self.procPath, "-i", sourcePath, "-r", "1", targetPath]);
        
        
    # creates the file name of an output image        
    def _createFileName(self, prefix, extension):
        uniqueId = uuid.uuid4()
        return os.path.join(self.pathToWorkspace, prefix + "_" + str(uniqueId) + extension)
