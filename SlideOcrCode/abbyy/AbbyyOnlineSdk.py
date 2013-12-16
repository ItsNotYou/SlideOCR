#!/usr/bin/python

# Usage: recognize.py <input file> <output file> [-language <Language>] [-pdf|-txt|-rtf|-docx|-xml]

import argparse
import base64
import getopt
import abbyy.MultipartPostHandler
import os
import re
import sys
import time
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import xml.dom.minidom

class ProcessingSettings:
	Language = "English"
	OutputFormat = "docx"


class Task:
	Status = "Unknown"
	Id = None
	DownloadUrl = None
	def IsActive( self ):
		if self.Status == "InProgress" or self.Status == "Queued":
			return True
		else:
			return False

class AbbyyOnlineSdk:
	ServerUrl = "http://cloud.ocrsdk.com/"
	ApplicationId = "user"
	Password = "password"
	Proxy = None
	enableDebugging = 0

	def ProcessImage( self, filePath, settings ):
		urlParams = urllib.parse.urlencode({
			"language" : settings.Language,
			"exportFormat" : settings.OutputFormat
			})
		requestUrl = self.ServerUrl + "processImage?" + urlParams

		bodyParams = { "file" : open( filePath, "rb" )  }
		request = urllib.request.Request( requestUrl, None, self.buildAuthInfo() )
		response = self.getOpener().open(request, bodyParams).read()
		if response.find( '<Error>' ) != -1 :
			return None
		# Any response other than HTTP 200 means error - in this case exception will be thrown

		# parse response xml and extract task ID
		task = self.DecodeResponse( response )
		return task

	def GetTaskStatus( self, task ):
		urlParams = urllib.parse.urlencode( { "taskId" : task.Id } )
		statusUrl = self.ServerUrl + "getTaskStatus?" + urlParams
		request = urllib.request.Request( statusUrl, None, self.buildAuthInfo() )
		response = self.getOpener().open( request ).read()
		task = self.DecodeResponse( response )
		return task

	def DownloadResult( self, task, outputPath ):
		getResultParams = urllib.parse.urlencode( { "taskId" : task.Id } )
		getResultUrl = self.ServerUrl + "getResult?" + getResultParams
		request = urllib.request.Request( getResultUrl, None, self.buildAuthInfo() )
		fileResponse = self.getOpener().open( request ).read()
		resultFile = open( outputPath, "wb" )
		resultFile.write( fileResponse )


	def DecodeResponse( self, xmlResponse ):
		""" Decode xml response of the server. Return Task object """
		dom = xml.dom.minidom.parseString( xmlResponse )
		taskNode = dom.getElementsByTagName( "task" )[0]
		task = Task()
		task.Id = taskNode.getAttribute( "id" )
		task.Status = taskNode.getAttribute( "status" )
		if task.Status == "Completed":
			task.DownloadUrl = taskNode.getAttribute( "resultUrl" )
		return task


	def buildAuthInfo( self ):
		return { "Authorization" : "Basic %s" % base64.encodestring( "%s:%s" % (self.ApplicationId, self.Password) ) }

	def getOpener( self ):
		if self.Proxy == None:
			self.opener = urllib.request.build_opener( abbyy.MultipartPostHandler.MultipartPostHandler,
			urllib.request.HTTPHandler(debuglevel=self.enableDebugging))
		else:
			self.opener = urllib.request.build_opener( 
				self.Proxy, 
				abbyy.MultipartPostHandler.MultipartPostHandler,
				urllib.request.HTTPHandler(debuglevel=self.enableDebugging))
		return self.opener


