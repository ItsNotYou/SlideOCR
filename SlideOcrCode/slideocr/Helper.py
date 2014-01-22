'''
Created on 08.01.2014

@author: Matthias
'''

import os
import uuid


class FileNameCreator():
    
    rememberedFilenames = [];
    
    @staticmethod
    def createFileName(path,argList,procName):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        add = ""
        for arg in argList:
            add += "_" + str(arg)
        result = os.path.join(head,name + "_%s%s" % (procName,add) + ext)
        FileNameCreator.rememberedFilenames.append(result)
        return result
    
    @staticmethod
    def createFileNameWithoutExtension(path,argList,procName, rememberExtension):
        '''
        Creates a filename, but doesn't add the rememberExtension. The extension is remembered for automated deletion, though.
        '''
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        add = ""
        for arg in argList:
            add += "_" + str(arg)
        result = os.path.join(head,name + "_%s%s" % (procName,add) + ext)
        FileNameCreator.rememberedFilenames.append(result + rememberExtension)
        return result
    
    @staticmethod
    def _createFileName(path, prefix):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        uniqueId = uuid.uuid4()
        result = os.path.join(head, name + "_%s_%s" % (prefix, str(uniqueId)) + ext)
        FileNameCreator.rememberedFilenames.append(result)
        return result

    @staticmethod
    def _createFileName2(prefix, uniqueId, extension, pathToWorkspace):
        # creates the file name of an output image
        result = os.path.join(pathToWorkspace, prefix + "_" + str(uniqueId) + extension)
        FileNameCreator.rememberedFilenames.append(result)
        return result

    @staticmethod
    def _createFileName3(path, uniqueId):
        # creates the file name of an output image        
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        result = os.path.join(head,name + "_%s" % uniqueId + ext)
        FileNameCreator.rememberedFilenames.append(result)
        return result
    
    @staticmethod
    def createFileNameFromPath(sourcePath, targetDirectory):
        result = os.path.join(targetDirectory, os.path.basename(sourcePath));
        FileNameCreator.rememberedFilenames.append(result)
        return result
    