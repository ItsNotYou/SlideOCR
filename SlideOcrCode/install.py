'''
Created on 21.01.2014

@author: hgessner
'''

import os
import subprocess
import sys
import shutil
from zipfile import ZipFile

# Adjust according to system
pythonInstallDir = "C:\\Python27\\"

pythonExe = "python.exe"
pipExe = "Scripts\\pip.exe"
installPath = "..\\install\\"
unzipPath = ".."
pythonPath = os.path.join(pythonInstallDir, pythonExe)
pipPath = os.path.join(pythonInstallDir, pipExe)

def call(params):
    result =  subprocess.call(params)
    if result != 0:
        sys.exit(result)
        
def isInstalled(executable):
    try:
        subprocess.call([executable])
        return True
    except:
        return False

if not os.path.exists(pythonPath):
    # python wasn't found, that can't be good
    print "%s isn't a python install directory. Please set the python install directory in the script and try again." % pythonInstallDir
    sys.exit(-1)

if not os.path.exists(pipPath):
    # pip isn't installed yet, let's change that
    ez_setup = os.path.join(installPath, "ez_setup.py")
    get_pip = os.path.join(installPath, "get-pip.py")
    call([pythonPath, ez_setup])
    call([pythonPath, get_pip])

call([pipPath, "-q", "install", "requests"])
call([pipPath, "-q", "install", "ftfy"])
call([pipPath, "-q", "install", "django"])

shutil.copyfile(os.path.join(installPath, "cv2.pyd"), os.path.join(pythonInstallDir, "Lib\site-packages", "cv2.pyd"))

call([os.path.join(installPath, "PIL-1.1.7.win32-py2.7.exe")])
call([os.path.join(installPath, "numpy-1.8.0-win32-superpack-python2.7.exe")])
call([os.path.join(installPath, "python-dateutil-2.2.win32-py2.7.exe")])
call([os.path.join(installPath, "MySQL-python-1.2.5.win32-py2.7.exe")])

if not isInstalled("ffmpeg"):
    # install ffmpeg
    ffmpeg = os.path.join(installPath, "ffmpeg.zip")
    ffmpeg_bin_dir = os.path.join(unzipPath, "ffmpeg\\bin")
    ZipFile(ffmpeg, 'r').extractall(unzipPath)
    os.environ["PATH"] += os.pathsep + ffmpeg_bin_dir
    
if not isInstalled("tesseract"):
    # install tesseract
    tesseract = os.path.join(installPath, "tesseract-ocr-setup-3.02.02.exe")
    call([tesseract])
