import cv2
import zipfile

def validateArguments(args):
    if (args.sourceFile == None):
        print "Error: You have to specify a source file. Use --sourceFile=FILE."
        return False
    if (cv2.imread(args.sourceFile,0) == None and args.extraction == None and not args.isVideoId and not zipfile.is_zipfile(args.sourceFile)):
        print "Error: Corrupt image as source file or source file is a video but you did not define a extraction data file."
        return False
    if (args.workingDirectory == "."):
        print "Warning: It is recommended to use a working directory different from the execution directory."
    return True
