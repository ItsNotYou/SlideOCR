'''
Created on 22.01.2014

@author: hgessner
'''

import os
import subprocess


class Paths:
    
    # Adjust according to system
    pythonInstallDir = "C:\\Python27\\"
    
    # These should be fine, no adjusting necessary
    pythonExe = "python.exe"
    pipExe = "Scripts\\pip.exe"
    installPath = "..\\install\\"
    unzipPath = ".."
    
    @staticmethod
    def ffmpegBinDir():
        return os.path.join(Paths.unzipPath, "ffmpeg\\bin")
    
    @staticmethod
    def pythonPath():
        return os.path.join(Paths.pythonInstallDir, Paths.pythonExe)
    
    @staticmethod
    def pipPath():
        return os.path.join(Paths.pythonInstallDir, Paths.pipExe)
    
    @staticmethod
    def isInstalled(executable):
        try:
            subprocess.call([executable])
            return True
        except:
            return False
        