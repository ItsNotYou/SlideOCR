'''
Created on 16.12.2013

@author: hgessner
'''

import time
import xml.etree.ElementTree as ET
import base64
import requests
from slideocr.conf.Secrets import Secrets


def getStatus(taskId, headers):
    res = requests.get("http://cloud.ocrsdk.com/getTaskStatus?taskId=%s" % taskId, headers = headers)
    root = ET.fromstring(res.text)
    for task in root.findall(".//task"):
        if task.attrib.get("id") == taskId:
            return task.attrib.get("status")


def getDownloadUrl(taskId, headers):
    res = requests.get("http://cloud.ocrsdk.com/getResult?taskId=%s" % taskId, headers = headers);
    print res.text.encode("utf-8")


source = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\img1.png"
workspace = "C:\\Users\\hgessner\\workspace\\SlideOCR\\workspace"

headers = {}
headers["Authorization"] = "Basic %s" % base64.encodestring( "%s:%s" % (Secrets.ABBYY_APP_ID, Secrets.ABBYY_PWD) )

files = {'file': open(source, 'rb')}

res = requests.post("http://cloud.ocrsdk.com/processImage?exportFormat=txt", files = files, headers = headers)

root = ET.fromstring(res.text)
for result in root.findall(".//task"):
    taskId = result.attrib.get("id")
    while getStatus(taskId, headers) != "Completed":
        time.sleep(4)
    getDownloadUrl(taskId, headers)
