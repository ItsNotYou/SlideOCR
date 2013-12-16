'''
Created on 08.12.2013

@author: hgessner
'''

import argparse
import os

parser = argparse.ArgumentParser( description="Recognize a file via web service" )
parser.add_argument( 'sourceFile' )
parser.add_argument( 'targetFile' )
args = parser.parse_args()

sourceFile = args.sourceFile
targetFile = args.targetFile

if os.path.isfile(sourceFile):
    print("Parse Datei")
    
else:
    print(sourceFile + " ist keine Datei")
    print("Vorgang abgebrochen")
