
'''
Created on 16.12.2013

@author: hgessner
'''

import time
import xml.etree.ElementTree as ET
import base64
import requests
from django.template import Template, Context
from django.conf import settings
from slideocr.conf.Secrets import Secrets
from slideocr.Handlers import Ocr
from slideocr.ocr.OcrCommons import BoundingBoxExtraction


class AbbyyCloud(Ocr):
    '''
    Uploads all images into the abbyy cloud and retreives the detection result
    If a bounding box is specified, the box is copied into a separate file before detection is executed
    '''
    
    def process(self, images):
        images = BoundingBoxExtraction().process(images)
        
        uploader = AbbyyUploader()
        for image in images:
            uploader.processImage(image)
        return images;


class AbbyyTask:
    
    id = None
    image = None
    status = None
    
    def IsActive(self):
        if self.status == "InProgress" or self.status == "Queued":
            return True
        else:
            return False
    
    
class AbbyyUploader:
    
    appId = None
    pwd = None
    processFieldsTemplate = """<?xml version="1.0" encoding="UTF-8"?>
<document xmlns="http://ocrsdk.com/schema/taskDescription-1.0.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://ocrsdk.com/schema/taskDescription-1.0.xsd http://ocrsdk.com/schema/taskDescription-1.0.xsd">

<fieldTemplates></fieldTemplates>

<page applyTo="0">
       <text id="myTextBlock" left="{{ task.image.bounding.left }}" top="{{ task.image.bounding.top }}" right="{{ task.image.bounding.right }}" bottom="{{ task.image.bounding.bottom }}">
       </text>
</page>
</document>"""
    
    def __init__(self):
        self.appId = Secrets.ABBYY_APP_ID
        self.pwd = Secrets.ABBYY_PWD
        
    def buildAuthInfo(self):
        # Because the data will be sent as a http header we have to remove the line break, otherwise the http network code breaks
        return {"Authorization" : "Basic %s" % base64.encodestring("%s:%s" % (self.appId, self.pwd)).replace('\n', '')}
    
    def callProcessImage(self, task):
        files = {'file': open(task.image.boundingPath, 'rb')}
        params = {"exportFormat": "xml"}
        headers = self.buildAuthInfo()
        
        res = requests.post("http://cloud.ocrsdk.com/processImage", files = files, params = params, headers = headers)
        root = ET.fromstring(res.text)
        for result in root.findall(".//task"):
            task.id = result.attrib.get("id")
        
    def waitForImageCompletion(self, task):
        self.readStatus(task)
        while task.IsActive():
            time.sleep(4)
            self.readStatus(task)
        
    def readStatus(self, task):
        headers = self.buildAuthInfo()
        res = requests.get("http://cloud.ocrsdk.com/getTaskStatus?taskId=%s" % task.id, headers = headers)
        root = ET.fromstring(res.text)
        for xmlTask in root.findall(".//task"):
            if xmlTask.attrib.get("id") == task.id:
                task.status = xmlTask.attrib.get("status")
        
    def downloadResult(self, task):
        headers = self.buildAuthInfo()
        res = requests.get("http://cloud.ocrsdk.com/getResult?taskId=%s" % task.id, headers = headers);
        task.image.text = res.text.encode("utf-8")
        
    def processImage(self, image):
        task = AbbyyTask()
        task.image = image
        self.callProcessImage(task)
        self.waitForImageCompletion(task)
        self.downloadResult(task)
        
    def processImages(self, images):
        for image in images:
            self.processImage(image)
        
    def callSubmitImage(self, task):
        files = {'file': open(task.image.path, 'rb')}
        headers = self.buildAuthInfo()
        
        res = requests.post("http://cloud.ocrsdk.com/submitImage", files = files, headers = headers)
        root = ET.fromstring(res.text)
        for result in root.findall(".//task"):
            task.id = result.attrib.get("id")
        
    def fillProcessFieldsTemplate(self, task):
        settings.configure()
        t = Template(self.processFieldsTemplate)
        c = Context({"task": task})
        return t.render(c)
        
    def callProcessFields(self, task):
        request = self.fillProcessFieldsTemplate(task)
        params = {"taskId": task.id}
        headers = self.buildAuthInfo()
        
        requests.post("http://cloud.ocrsdk.com/processFields", data = request, headers = headers, params = params)
        
    def callProcessTextField(self, task):
        b = task.image.bounding
        
        files = {'file': open(task.image.path, 'rb')}
        params = {}
        # params["region"] = "%s,%s,%s,%s" % (str(b.left), str(b.top), str(b.right), str(b.bottom))
        headers = self.buildAuthInfo()
        
        res = requests.post("http://cloud.ocrsdk.com/processTextField", files = files, headers = headers, params = params)
        root = ET.fromstring(res.text)
        for result in root.findall(".//task"):
            task.id = result.attrib.get("id")
    