'''
Created on 16.12.2013

@author: hgessner
'''

from abbyy.process import *

parser = argparse.ArgumentParser( description="Recognize a file via web service" )
parser.add_argument( 'sourceFile' )

parser.add_argument( '-l', '--language', default='English', help='Recognition language (default: %(default))' )
group = parser.add_mutually_exclusive_group()
group.add_argument( '-txt', action='store_const', const='txt', dest='format', default='txt' )
group.add_argument( '-pdf', action='store_const', const='pdfSearchable', dest='format' )
group.add_argument( '-rtf', action='store_const', const='rtf', dest='format' )
group.add_argument( '-docx', action='store_const', const='docx', dest='format' )
group.add_argument( '-xml', action='store_const', const='xml', dest='format' )

args = parser.parse_args()

sourceFile = args.sourceFile
language = args.language
outputFormat = args.format

result = process(sourceFile);
print result
