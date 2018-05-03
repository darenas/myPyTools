'''
Created on 2 May 2018

@author: darenas
'''
import sys
from os import listdir
from os.path import join, isdir
from lxml import html
import requests
import json

# Parsing params
if len(sys.argv) != 3:
    print("Two arguments are required: origin path (local or remote http) and destination file path (local)")
    exit()
originPath = sys.argv[1]
destFile = sys.argv[2]

## Some global vars
imgExts = ('.png', '.jpg', '.jpeg')
setsNames = ["train", "val"] # This is because of the names given by Deepomatic for these sets 
statsDict = {}
jsonData = {}
jsonData["tags"] = []
jsonData["images"] = []
local = False if originPath.startswith('http') else True

## Some functions
def explorePath(thePath):
    files = []
    folders = [] 
    
    if local:
        for elmnt in listdir(thePath):
            elmntPath = myPathJoin(thePath, elmnt)
            if isdir(elmntPath):
                folders.append(elmnt)
            elif elmnt.endswith(imgExts) :
                files.append(elmnt)
    else:
        page = requests.get(thePath)
        tree = html.fromstring(page.content)
        allLinks = tree.xpath('//a/@href')
        for cuLink in allLinks:
            if cuLink.endswith('/') and not cuLink.startswith('/'):
                folders.append(cuLink[:-1])
            elif cuLink.endswith(imgExts) :
                files.append(cuLink)
    
    return folders, files

def getImgsOfClass(classFol, classPath, datasetFol):
    statsDict[datasetFol][classFol] = 0
    _, imgFils = explorePath(classPath)
    for imf in imgFils:
        imgPath = myPathJoin(classPath, imf)
                  
        imgDict = {}
        imgDict["location"] = imgPath 
        if datasetFol != "all" : 
            imgDict["stage"] = datasetFol
        imgDict["annotations"] = [{"tag" : classFol}]   # for the tagging problem an image can have more than one tags
        
        jsonData["images"].append(imgDict)
        statsDict[datasetFol][classFol] += 1  
            
    if sum(statsDict[datasetFol].values()) == 0:
        del statsDict[datasetFol]
    else:
        if classFol not in jsonData["tags"]:
            jsonData["tags"].append(classFol)

def myPathJoin(base, ending):
    if local:
        return join(base, ending)
    else:
        return base + ending if base.endswith('/') else base + '/' + ending
        
## The script starts here really (TODO: replace this with a nice main)
fols, fils = explorePath(originPath)
for cuFol in fols:
    cuFolPath = myPathJoin(originPath, cuFol)
    if cuFol in setsNames:
        print("Found a dataset (stage): <<" + cuFol + ">>, all images on this directory will be assigned to this dataset")
        statsDict[cuFol] = {}
        classFols,_ = explorePath( cuFolPath )
        for cuClassFol in classFols:
            getImgsOfClass(cuClassFol, myPathJoin(cuFolPath, cuClassFol), cuFol)
    else:
        if "all" not in statsDict: 
            statsDict["all"] = {}
        getImgsOfClass(cuFol, cuFolPath, "all")
                        
with open(destFile, 'w') as outfile:  
    json.dump(jsonData, outfile, indent=2, sort_keys=True)
print("JSON file created!!")
print(str(len(statsDict.keys()))+" datasets:")
for k,v in statsDict.items(): 
    print(k + " -> " + str(sum(v.values())) + " images in " + str(len(v.items())) + " classes: " + str(v.items()))
