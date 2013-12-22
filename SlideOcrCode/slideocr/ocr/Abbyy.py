'''
Created on 16.12.2013

@author: hgessner
'''

import time
import xml.etree.ElementTree as ET
import base64
import requests
from slideocr.conf.Secrets import Secrets
from slideocr.Handlers import Ocr


class AbbyyCloud(Ocr):
    '''
    Uploads all images into the abbyy cloud and retreives the detection result
    '''
    
    def process(self, images):
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
    
    def __init__(self):
        self.appId = Secrets.ABBYY_APP_ID
        self.pwd = Secrets.ABBYY_PWD
        
    def buildAuthInfo(self):
        return { "Authorization" : "Basic %s" % base64.encodestring("%s:%s" % (self.appId, self.pwd)) }
    
    def callProcessImage(self, task):
        files = {'file': open(task.image.path, 'rb')}
        headers = self.buildAuthInfo()
        
        res = requests.post("http://cloud.ocrsdk.com/processImage?exportFormat=txt", files = files, headers = headers)
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
        