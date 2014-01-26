'''
Created on 08.01.2014

@author: Matthias
'''

'''
This class provides a methode to classify text snippets 

Argument Hints:
    heightOffset: Defines the Offset specifying the distance of caption and footing to the average text height
        Example: Offset = 10 and average height = 40 than text with a text height greater than 50 is declared 
                 as caption and text with a text height less then 30 is declared as footing. (Default = 10)
'''
class TextClassificator(object):
    
    def __init__(self,heightOffset):
        self.heightOffset = heightOffset
        
    # methode to classify text snippets into caption, footing and content
    def classify(self,images):
        self.classifyPerSlideSet(images)
        #self.classifyPerSlide(images)
        
    # classify text by calculating average height over complete slide set
    def classifyPerSlideSet(self,images):
        
        # calculate average height
        heightSum = 0
        for image in images:
            currentHeight = image.bounding.bottom - image.bounding.top
            heightSum += currentHeight
        averageHeight = heightSum / len(images)
        
        # classify text
        for image in images:
            currentHeight = image.bounding.bottom - image.bounding.top
                
            if currentHeight > averageHeight + self.heightOffset:
                image.contentType = "caption"
                
            elif currentHeight < averageHeight - self.heightOffset:
                image.contentType = "footing"
                
            else:
                image.contentType = "content"
    
    # classify text by calculating average height over every single slide
    def classifyPerSlide(self,images):
        
        # put frames belonging to the same image in an array
        imageDic = {}
        for image in images:
            if image.frameId not in imageDic:
                imageDic[image.frameId] = [image]
            else:
                imageDic[image.frameId].append(image)
                
        # calculate the average height of the text in an image and classify the text
        for _,Dicmages in imageDic.iteritems():
        
            heightSum = 0
            
            for image in Dicmages:
                currentHeight = image.bounding.bottom - image.bounding.top
                heightSum += currentHeight
               
            averageHeight = heightSum / len(Dicmages)
            
            for image in Dicmages:
                currentHeight = image.bounding.bottom - image.bounding.top
                
                if currentHeight > averageHeight + self.heightOffset:
                    image.contentType = "caption"
                    
                elif currentHeight < averageHeight - self.heightOffset:
                    image.contentType = "footing"
                    
                else:
                    image.contentType = "content"
            
        