#!/usr/bin/python

# Usage: recognize.py <input file> <output file> [-language <Language>] [-pdf|-txt|-rtf|-docx|-xml]

import argparse
import base64
import getopt
import MultipartPostHandler
import os
import re
import sys
import time
import urllib2
import urllib

from AbbyyOnlineSdk import *
from slideocr.conf.Secrets import *

def process(sourceFile, language = 'English', outputFormat = 'txt'):
	processor = AbbyyOnlineSdk()
	processor.ApplicationId = Secrets.ABBYY_APP_ID
	processor.Password = Secrets.ABBYY_PWD
	
	# Proxy settings
	if "http_proxy" in os.environ:
		proxyString = os.environ["http_proxy"]
		print "Using proxy at %s" % proxyString
		processor.Proxy = urllib2.ProxyHandler( { "http" : proxyString })
	
	
	# Recognize a file at filePath and save result to resultFilePath
	def recognizeFile( filePath, language, outputFormat ):
		print "Uploading.."
		settings = ProcessingSettings()
		settings.Language = language
		settings.OutputFormat = outputFormat
		task = processor.ProcessImage( filePath, settings )
		if task == None:
			print "Error"
			return
		print "Id = %s" % task.Id
		print "Status = %s" % task.Status
	
		# Wait for the task to be completed
		sys.stdout.write( "Waiting.." )
		while True :
			task = processor.GetTaskStatus( task )
			if task.IsActive() == False:
				print
				break
			sys.stdout.write( "." )
			time.sleep( 4 )
	
		print "Status = %s" % task.Status
		
		if task.DownloadUrl != None:
			return processor.DownloadResult( task )
		else:
			return None
	
	
	if os.path.isfile( sourceFile ):
		return recognizeFile( sourceFile, language, outputFormat )
	else:
		print "File not found: %s" % sourceFile
		return None
