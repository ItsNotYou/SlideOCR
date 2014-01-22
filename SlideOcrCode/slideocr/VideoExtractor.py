'''
Created on 16.12.2013

@author: hgessner
'''

import shutil
import subprocess
import uuid
import numpy
from slideocr.Data import OcrImage, FrameTimestamp
from slideocr.MySqlWrapper import MySqlTimestampReader, MySqlResultWriter
from slideocr.ZipWrapper import ZipWrapper
from slideocr.Helper import FileNameCreator
from slideocr.conf.Paths import Paths
import os


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


class Extractor:
    
    def extract(self):
        print "Nothing to extract since this is a stub. If you see this message then somebody didn't overwrite the extract() function correctly."
        
        
    def write(self, images):
        for image in images:
            print image.text + " (" + image.contentType + ")"
        
    
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
            uniqueId = uuid.uuid4()
            sourcePath = timestamp.videoPath
            targetPath = FileNameCreator._createFileName2(tag, uniqueId, '.png', self.pathToWorkspace)
            self.extractFrame(seconds, sourcePath, targetPath);
            
            ocrImage = OcrImage()
            ocrImage.tag = tag
            ocrImage.path = targetPath
            ocrImage.frameId = uniqueId
            results.append(ocrImage)
        return results;
    
    
    def extractFrame(self, seconds, sourcePath, targetPath):
        procPath = self.procPath
        if not Paths.isInstalled(procPath):
            # Try fallback directory
            procPath = os.path.join(Paths.ffmpegBinDir(), procPath)
        
        # Does a fast and accurate seeking for the specified timestamp. For details see https://trac.ffmpeg.org/wiki/Seeking%20with%20FFmpeg
        subprocess.call([procPath, "-loglevel", "warning", "-ss", str(seconds - self.slowSearchDelta), "-i", sourcePath, "-ss", str(self.slowSearchDelta), "-vframes", "1", targetPath]);


class ExtractionHelper:
    '''
    Combines several helper functions for easy frame creation or extraction. The helper functions always return an array of ocr images
    '''
    
    def convertSingleImage(self, imagePath, workingDirectory):
        targetFile = FileNameCreator.createFileNameFromPath(imagePath, workingDirectory)
        shutil.copyfile(imagePath, targetFile)
        
        images = [OcrImage()]
        images[0].tag = "01"
        images[0].path = targetFile
        images[0].frameId = uuid.uuid4()
        return images
    
    def convertVideoByTable(self, videoPath, tablePath, workingDirectory):
        timestamps = TableReader().readTimestamps(tablePath, videoPath)
        images = FrameExtractor(workingDirectory).mapTimestampsToFrames(timestamps)
        return images
    
    def convertVideoByDatabase(self, videoId, workingDirectory):
        timestamps = MySqlTimestampReader().readTimestamps(videoId)
        images = FrameExtractor(workingDirectory).mapTimestampsToFrames(timestamps)
        return images
    
    def convertZip(self, zipPath, workingDirectory):
        wrapper = ZipWrapper()
        zippedFiles = wrapper.extractFiles(zipPath, workingDirectory)
        zippedFiles = wrapper.renameFiles(zippedFiles, workingDirectory)
        images = wrapper.asImages(zippedFiles)
        return images
    

class MySqlVideoExtractor(Extractor):
    
    workingDirectory = None
    videoId = None
    
    def __init__(self, workingDirectory, videoId):
        self.workingDirectory = workingDirectory
        self.videoId = videoId
        
    def extract(self):
        return ExtractionHelper().convertVideoByDatabase(self.videoId, self.workingDirectory)
    
    def write(self, images):
        writer = MySqlResultWriter()
        writer.writeResults(images)
        
        
class VideoExtractor(Extractor):
    
    workingDirectory = None
    videoPath = None
    splitPath = None
    
    def __init__(self, workingDirectory, videoPath, splitPath):
        self.workingDirectory = workingDirectory
        self.videoPath = videoPath
        self.splitPath = splitPath
        
    def extract(self):
        return ExtractionHelper().convertVideoByTable(self.videoPath, self.splitPath, self.workingDirectory)
    
        
class ImageExtractor(Extractor):
    
    workingDirectory = None
    imagePath = None
    
    def __init__(self, workingDirectory, imagePath):
        self.workingDirectory = workingDirectory
        self.imagePath = imagePath
        
    def extract(self):
        return ExtractionHelper().convertSingleImage(self.imagePath, self.workingDirectory)
    
    
class ZipExtractor(Extractor):
    
    workingDirectory = None
    zipPath = None
    
    def __init__(self, workingDirectory, zipPath):
        self.workingDirectory = workingDirectory
        self.zipPath = zipPath
        
    def extract(self):
        return ExtractionHelper().convertZip(self.zipPath, self.workingDirectory)
    