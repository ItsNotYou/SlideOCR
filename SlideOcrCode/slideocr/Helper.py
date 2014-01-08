'''
Created on 08.01.2014

@author: Matthias
'''

import os

class FileNameCreator():
    
    @staticmethod
    def createFileName(path,argList,procName):
        (head, tail) = os.path.split(path)
        (name, ext) = os.path.splitext(tail)
        add = ""
        for arg in argList:
            add += "_" + str(arg)
        return os.path.join(head,name + "_%s%s" % (procName,add) + ext)