'''
Created on 24 Apr 2018

@author: darenas
'''

import os
import sys
from PIL import Image

consideredExtensions = ('.png', '.jpg', '.jpeg')
currPath = os.path.dirname(os.path.abspath(__file__))
theFolder = os.path.join(currPath,sys.argv[1])

count = valid = corrupted = 0
toDelete = []
for path, subdirs, files in os.walk(theFolder):
    for name in files:
        currInnerFilePath = os.path.join(path, name)
        if currInnerFilePath.lower().endswith(consideredExtensions):
            try:
                img = Image.open(currInnerFilePath)
                img.verify() 
                valid+=1
            except (IOError, SyntaxError) as e:
                toDelete.append(currInnerFilePath)
                corrupted+=1
            count+=1
            sys.stdout.write("Images Processed: %d   \r" % (count) )
            sys.stdout.flush()
            
for file in toDelete:
    os.remove(file)
            
print("A total of " + str(valid) + " valid images were found, and " + str(corrupted) + " corrupted images were deleted!")
