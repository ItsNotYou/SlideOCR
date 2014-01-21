'''
Created on 08.01.2014

@author: Matthias
'''

import os
import uuid


class FileNameCreator():
    
    @staticmethod
    def createFileName(path,argList,procName):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        add = ""
        for arg in argList:
            add += "_" + str(arg)
        return os.path.join(head,name + "_%s%s" % (procName,add) + ext)
    
    @staticmethod
    def _createFileName(path, prefix):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        uniqueId = uuid.uuid4()
        return os.path.join(head, name + "_%s_%s" % (prefix, str(uniqueId)) + ext)

    @staticmethod
    def _createFileName2(prefix, uniqueId, extension, pathToWorkspace):
        # creates the file name of an output image
        return os.path.join(pathToWorkspace, prefix + "_" + str(uniqueId) + extension)

    @staticmethod
    def _createFileName3(path, uniqueId):
        # creates the file name of an output image        
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        return os.path.join(head,name + "_%s" % uniqueId + ext)
    