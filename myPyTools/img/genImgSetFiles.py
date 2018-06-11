'''
Created on 7 May 2018

@author: darenas
'''
from random import randint
from os import listdir, path, makedirs
from os.path import join, isdir, isfile, splitext
import shutil, sys
from PIL import Image

sourceDir = 'C:\\Users\\darenas\\home\\tmp\\SIARA-DATA\\Panto_new2_fixExp'
destDir = 'C:\\Users\\darenas\\home\\tmp\\SIARA-DATA\\PantoDet_stdFormat_fixExpInc'

#TODO: Allow to set all the parameters from command line
#sourceDir = sys.argv[1]            # Use full path
#destDir = sys.argv[2]            # Use full path
# Exemple: py genPascalVocStdDataset.py C:\Users\darenas\home\tmp\SIARA-DATA\Panto_new2 C:\Users\darenas\home\pantoDatasetVOCformat

traSetPerc = 90                    # Percentage of images to the training set
tstSetPecc = 0                    # Percentage of images to the test set
# The percentage for the Validation wiil be set to : 100 - traSetPerc - tstSetPecc  

imgSetName = 'Main'             # Just the name of the dataset (so multiples dataset may be created for the same images
copyFiles = True                # If true, images and annotation files from the source will be copied 
cleanDest = True                # If true, all contents will be deleted from the the destination folder before the execution of this script
onlyAnnotated = True           # If true, only the images with an .xml annotation file (same name) will be taken into account
transformPNGtoJPG = True        # If true, converts the PNG format of any source image to JPG in the destination folder

## Defining some functions
'''
returns: 
    0 -> training
    1 -> validation (trainval)
    2 -> test (val)
'''
def chooseSet(traProb, testProb): 
    theRandomValue = randint(0, 99)
    if theRandomValue <= traProb:
        return 0
    if testProb <= 0:
        return 1
    else:
        if theRandomValue <= (traProb + testProb):
            return 2
        else:
            return 1 

## Defining some variables
imgExts = ('.png', '.jpg', '.jpeg')
fileSuffix = ['train', 'trainval', 'val']

destImgSetDir = join(destDir, 'ImageSets', imgSetName)
destImgDir = join(destDir, 'JPEGImages')
destLabDir = join(destDir, 'Annotations')

theListOfFiles = [{} for _ in range(3)]


## The script starts here.. TODO add a nice main function
if cleanDest and path.exists(destDir): shutil.rmtree(destDir)
if path.exists(destImgSetDir):
    print('The specified destination path (%s) is not empty, removing all contents..' % destImgSetDir)
    shutil.rmtree(destImgSetDir)
makedirs(destImgSetDir)
if not path.exists(destImgDir): makedirs(destImgDir)
if not path.exists(destLabDir): makedirs(destLabDir)
    
imgCount = 0
labCount = 0
totCount = 0    
copCount = 0
for elmnt in listdir(sourceDir):
    elmntPath = join(sourceDir, elmnt)
    if isdir(elmntPath):
        theListOfFiles[0][elmnt] = []
        theListOfFiles[1][elmnt] = []
        theListOfFiles[2][elmnt] = []
        for file in listdir(elmntPath):
            fileFullPath = join(elmntPath,file)
            if isfile(fileFullPath):
                filename, file_extension = splitext(file)
                totCount += 1
                if file_extension in imgExts:
                    correspLabFile = join(elmntPath, filename + '.xml')
                    hasLabel = isfile(correspLabFile)
#                     filename = filename.replace(" ", "_") ## This may be unnecessary
#                     filename = filename.replace("(", "") ## This may be unnecessary             
#                     filename = filename.replace(")", "") ## This may be unnecessary
                    if (onlyAnnotated and hasLabel) or not onlyAnnotated:
                        setChoice = chooseSet(traSetPerc, tstSetPecc)
                        theListOfFiles[setChoice][elmnt].append(filename)                          
                        imgCount += 1   
                        if copyFiles: 
                            if transformPNGtoJPG and file_extension == '.png':
                                im = Image.open(fileFullPath)
                                rgb_im = im.convert('RGB')
                                rgb_im.save(join(destImgDir, filename + '.jpg'))
                            else:
                                shutil.copyfile(fileFullPath, join(destImgDir, (filename + '.png')) ) 
                            copCount += 1
                          
                    if hasLabel:
                        labCount += 1
                        if copyFiles: 
                            shutil.copyfile( correspLabFile, join(destLabDir, filename + '.xml') )
                            copCount += 1
                
                sys.stdout.write("Processed Files : %d (%d images and %d labels). Currently processing \"%s\" folder...        \r" % (totCount, imgCount, labCount, elmnt) )
                sys.stdout.flush()
print('\nAll files processed! %d files were copied' % copCount)                
for c in range(3):
    cuMainFile = open(join(destImgSetDir, (fileSuffix[c] + '.txt') ), 'w')
            
    for cuClass in theListOfFiles[c]:
        cuClassFile = open(join(destImgSetDir, (cuClass + '_' + fileSuffix[c] + '.txt') ), 'w')
         
        for elmnt in theListOfFiles[c][cuClass]:
            cuMainFile.write("%s\n" % elmnt)
            cuClassFile.write("%s\n" % elmnt)
    
    cuTot = sum(len(lis) for lis in theListOfFiles[c].values())   
    print('Total number of images in the %s set: %d (%3.2f %%)' % (fileSuffix[c], cuTot, cuTot*100/imgCount) )
    
                
print ('The script has ended')        
