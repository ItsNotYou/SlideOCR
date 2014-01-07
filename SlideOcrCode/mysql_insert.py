'''
Created on 07.01.2014

@author: hgessner
'''

import MySQLdb
from slideocr.VideoExtractor import TableReader
from slideocr.conf.Secrets import Secrets


videoUrl = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\desktop.mp4"
splitTable = "C:\\Users\\hgessner\\workspace\\SlideOCR\\samples\\slide-timestamps.txt"

splits = TableReader().readTimestamps(splitTable, videoUrl)

db = MySQLdb.connect(host="localhost", user=Secrets.MYSQL_USER, passwd=Secrets.MYSQL_PWD, db="mydb")

with db:
    cur = db.cursor()
    
    cur.execute("DELETE FROM segment")
    cur.execute("DELETE FROM video")
    cur.execute("DELETE FROM videotype")
    cur.execute("DELETE FROM lecture")
    cur.execute("DELETE FROM series")
    
    cur.execute("INSERT INTO series (id, name) VALUES (1, 'Extraktion von Meta-Daten')")
    cur.execute("INSERT INTO lecture (id, name, series) VALUES (10, 'Erster Gruppenvortrag OCR-Gruppe', 1)")
    cur.execute("INSERT INTO videotype (id, description) VALUES (100, 'Studentenvortrag')")
    cur.execute("INSERT INTO video (id, lecture, videotype, url) VALUES (1000, 10, 100, '%s')" % videoUrl.replace("\\", "\\\\"))
    
    idValue = 10001
    for split in splits:
        cur.execute("INSERT INTO segment (id, video_id, start, best_index) VALUES (%d, 1000, '0:%d:%d', '0:%d:%d')" % (idValue, split.minutes, split.seconds, split.minutes, split.seconds))
        idValue += 1
    
    cur.execute("SELECT id, url FROM video")
    rows = cur.fetchall()
    for row in rows:
        print row[0], row[1]
        