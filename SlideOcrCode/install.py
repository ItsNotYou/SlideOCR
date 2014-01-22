'''
Created on 21.01.2014

@author: hgessner
'''

import os
import subprocess
import sys
import shutil
from zipfile import ZipFile
from slideocr.conf.Paths import Paths


def call(params):
    result =  subprocess.call(params)
    if result != 0:
        sys.exit(result)


if not os.path.exists(Paths.pythonPath()):
    # python wasn't found, that can't be good
    print "%s isn't a python install directory. Please set the python install directory in the script and try again." % Paths.pythonInstallDir
    sys.exit(-1)

if not os.path.exists(Paths.pipPath()):
    # pip isn't installed yet, let's change that
    ez_setup = os.path.join(Paths.installPath, "ez_setup.py")
    get_pip = os.path.join(Paths.installPath, "get-pip.py")
    call([Paths.pythonPath(), ez_setup])
    call([Paths.pythonPath(), get_pip])

call([Paths.pipPath(), "-q", "install", "requests"])
call([Paths.pipPath(), "-q", "install", "ftfy"])
call([Paths.pipPath(), "-q", "install", "django"])

shutil.copyfile(os.path.join(Paths.installPath, "cv2.pyd"), os.path.join(Paths.pythonInstallDir, "Lib\site-packages", "cv2.pyd"))

call([os.path.join(Paths.installPath, "PIL-1.1.7.win32-py2.7.exe")])
call([os.path.join(Paths.installPath, "numpy-1.8.0-win32-superpack-python2.7.exe")])
call([os.path.join(Paths.installPath, "python-dateutil-2.2.win32-py2.7.exe")])
call([os.path.join(Paths.installPath, "MySQL-python-1.2.5.win32-py2.7.exe")])

if not Paths.isInstalled("ffmpeg"):
    # install ffmpeg
    ffmpeg = os.path.join(Paths.installPath, "ffmpeg.zip")
    ZipFile(ffmpeg, 'r').extractall(Paths.unzipPath)

if not Paths.isInstalled("tesseract"):
    # install tesseract
    tesseract = os.path.join(Paths.installPath, "tesseract-ocr-setup-3.02.02.exe")
    call([tesseract])
