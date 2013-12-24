import cv2

def validateArguments(args):
    if (args.sourceFile == None):
        print "Error: You have to specify a source file. Use --sourceFile=FILE."
        return False
    if (cv2.imread(args.sourceFile,0) == None and args.extraction == None):
        print "Error: Corrupt image as source file or source file is a video but you did not define a extraction data file."
        return False
    if (args.workingDirectory == "."):
        print "Warning: It is recommended to use an working directory different to the execution directory."
    return True