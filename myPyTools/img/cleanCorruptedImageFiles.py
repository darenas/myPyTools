'''
Created on 24 Apr 2018

@author: darenas
'''

import os
import sys
from PIL import Image 
import shutil

## TODO: read params from command line

#currPath = os.path.dirname(os.path.abspath(__file__))
#theFolder = os.path.join(currPath,sys.argv[1])

theFolder = '/media/administrateur/Transcend/CAFEINE/Shootings trains/' #this must have a '/' at the end (TODO fix this later)
targetFolder = '/home/administrateur/SIARA_DATA/Shooting'

consideredExtensions = ('.png', '.jpg', '.jpeg')
cleanDestFolder = False
copyImages = False
copyOtherFiles = True
deleteErrors = False
resize = True
conserveRatio = True
newWidth = 1920             # 1920 x 1080 (HD 1080), 1280 x 720 (HD720)  
newHeight = 0               # only necessary if conserveRatio = False

if cleanDestFolder and os.path.exists(targetFolder):
    shutil.rmtree(targetFolder)
    
compDel = '' if deleteErrors else ' corrupted images will be deleted'
count = valid = corrupted = others = 0
toDelete = []
for path, subdirs, files in os.walk(theFolder):
    for name in files:
        currInnerFilePath = os.path.join(path, name)
        if copyImages or copyOtherFiles:
            innerPath = path.replace(theFolder, '')
            newFilePath = os.path.join(targetFolder, innerPath)
            if not os.path.exists(newFilePath):
                os.makedirs(newFilePath)
            newFilePath = os.path.join(newFilePath, name)
        if currInnerFilePath.lower().endswith(consideredExtensions):
            try:
                img = Image.open(currInnerFilePath)
                img.verify() 
                valid+=1
                if copyImages:
                    img = Image.open(currInnerFilePath)         # the image must be re-opened because of verify()
                    if resize:
                        if conserveRatio:
                            wpercent = (newWidth / float(img.size[0]))
                            newHeight = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((newWidth, newHeight), Image.ANTIALIAS)
                    img.save(newFilePath)
                    #img.close()    
            except (IOError, SyntaxError) as e:
                #print('ERROR OCCURRED while reading the image %s' % (currInnerFilePath) )
                toDelete.append(currInnerFilePath)
                corrupted+=1
            count+=1
        else:
            others += 1 
            if copyOtherFiles:
                shutil.copyfile(currInnerFilePath, newFilePath)               
        sys.stdout.write("Files Processed: %d images and %d other files     \r" % (count, others) )
        sys.stdout.flush()

print('The following list of images are corrupted %s..' % (compDel))             
for file in toDelete:
    print (file)
    if deleteErrors:
        os.remove(file)
            
print("A total of " + str(valid) + " valid images were found, and " + str(corrupted) + " corrupted images!")
