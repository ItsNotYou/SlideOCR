'''
Created on 21.01.2014

@author: hgessner
'''

import os
import subprocess
import sys

# Adjust according to system
pythonInstallDir = "C:\\Python27\\"

pythonExe = "python.exe"
pipExe = "Scripts\\pip.exe"
installPath = "..\\install\\"
pythonPath = os.path.join(pythonInstallDir, pythonExe)
pipPath = os.path.join(pythonInstallDir, pipExe)

def call(params):
    result =  subprocess.call(params)
    if result != 0:
        sys.exit(result)

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

