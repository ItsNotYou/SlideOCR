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
        '''
        Execute database specific code here
        '''
        print "Nothing to do"
        print "Overwrite method in subclasses to do specific database stuff"


class MySqlTimestampReader(DbConnection):
    '''
    Reads the timestamps for a given video id.
    '''
    
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
        
        
class MySqlResultWriter(DbConnection):
    '''
    Writes recognition results into the database.
    '''
    
    images = []
    fallbackContentType = "undefined"
    
    def doRun(self, cursor):
        ocrDict = self.__readAvailableOcrTypes(cursor)
        availableSegmentIds = self.__readAvailableSegmentIds(cursor)
        
        for image in self.images:
            print image.tag, image.text
            self.__safelyWriteRow(cursor, image, availableSegmentIds, ocrDict)
            
    def __safelyWriteRow(self, cursor, image, availableSegmentIds, ocrDict):
        if int(image.tag) in availableSegmentIds:
            ocrTypeId = self.__findMatchingKey(ocrDict, image.contentType)
            self.__writeRow(cursor, image, ocrTypeId)
            
    def __findMatchingKey(self, ocrDict, contentType):
        if contentType and contentType in ocrDict:
            return ocrDict[contentType]
        else:
            return ocrDict[self.fallbackContentType]
        
    def __writeRow(self, cursor, image, ocrTypeId):
        '''
        Beware the SQL injection?
        '''
        if ocrTypeId == None:
            cursor.execute("INSERT INTO ocrresult (segment_id, kord_lt_x, kord_lt_y, kord_rb_x, kord_rb_y, content) VALUES (%s, %f, %f, %f, %f, '%s')" % (image.tag, float(image.bounding.left), float(image.bounding.top), float(image.bounding.right), float(image.bounding.bottom), MySQLdb.escape_string(image.text)))
        else:
            cursor.execute("INSERT INTO ocrresult (segment_id, kord_lt_x, kord_lt_y, kord_rb_x, kord_rb_y, content, type) VALUES (%s, %f, %f, %f, %f, '%s', %d)" % (image.tag, float(image.bounding.left), float(image.bounding.top), float(image.bounding.right), float(image.bounding.bottom), MySQLdb.escape_string(image.text), ocrTypeId))
        
    def __readAvailableOcrTypes(self, cursor):
        ocrDict = {}
        
        cursor.execute("SELECT id, description FROM ocrtype")
        for row in cursor.fetchall():
            ocrDict[row[1]] = row[0]
            
        if not self.fallbackContentType in ocrDict:
            ocrDict[self.fallbackContentType] = None
            
        return ocrDict
    
    def __readAvailableSegmentIds(self, cursor):
        availableSegments = []
        
        cursor.execute("SELECT id FROM segment")
        for row in cursor.fetchall():
            availableSegments.append(row[0])
            
        return availableSegments
        
    def writeResults(self, images):
        '''
        Writes results into database
        '''
        self.images = images
        self.run()
        