'''
Created on 07.01.2014

@author: hgessner
'''

from slideocr.conf.Secrets import Secrets
import MySQLdb
from slideocr.Data import FrameTimestamp


class DbConnection:
    
    def run(self):
        db = MySQLdb.connect(host="localhost", user=Secrets.MYSQL_USER, passwd=Secrets.MYSQL_PWD, db="mydb")
        with db:
            cur = db.cursor()
            self.doRun(cur)
            
    def doRun(self, cursor):
        print "Nothing to do"


class MySqlTimestampReader(DbConnection):
    
    timestamps = []
    videoId = None
    
    def doRun(self, cursor):
        '''
        Beware the SQL injection?
        '''
        cursor.execute("SELECT s.id, s.best_index, v.url FROM segment s JOIN video v ON s.video_id = v.id WHERE s.video_id = %s" % self.videoId)
        
        result = []
        for row in cursor.fetchall():
            frame = FrameTimestamp()
            frame.tag = str(int(row[0]))
            frame.minutes = 0
            frame.seconds = row[1].seconds
            frame.videoPath = row[2]
            result.append(frame)
        self.timestamps = result
        
    def readTimestamps(self, videoId):
        '''
        Reads timestamps from database
        '''
        self.videoId = videoId
        self.run()
        return self.timestamps
        