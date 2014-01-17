'''
Created on 16.01.2014

@author: hgessner
'''

import os
import uuid
from zipfile import ZipFile
from slideocr.Data import OcrImage


class ZipWrapper:
    
    def extractFiles(self, zipPath, workspacePath):
        zipFile = ZipFile(zipPath, 'r')
        zippedFiles = zipFile.infolist();
        zipFile.extractall(workspacePath, zippedFiles)
        return zippedFiles
    
    def renameFiles(self, zippedFiles, workspacePath):
        results = []
        for zippedFile in zippedFiles:
            oldFile = os.path.join(workspacePath, zippedFile.filename);
            renamedFile = self._createFileName(oldFile, str(uuid.uuid4()))
            os.rename(oldFile, renamedFile)
            
            result = OcrImage()
            result.tag = self._getName(oldFile)
            result.path = renamedFile
            results.append(result)
        return results
    
    def asImages(self, images):
        for image in images:
            image.frameId = uuid.uuid4()
        return images
    
    def _createFileName(self, path, uniqueId):
        # creates the file name of an output image        
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        return os.path.join(head,name + "_%s" % uniqueId + ext)
    
    def _getName(self, path):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        return name
    