'''
Created on 3 May 2018

@author: darenas
'''

from lxml import html
import requests

theSite = "put here http site" #TODO: next version should use params
imgExts = ('.png', '.jpg', '.jpeg')

def exploreUrl(theUrl):
    print("Exploring " + theUrl)
    page = requests.get(theUrl)
    tree = html.fromstring(page.content)
 
    files = []
    folders = [] 
    allLinks = tree.xpath('//a/@href')
    for cuLink in allLinks:
        if cuLink.endswith('/') and not cuLink.startswith('/'):
            folders.append(cuLink)
        elif cuLink.endswith(imgExts) :
            files.append(cuLink)
    return folders, files



if not theSite.endswith('/'): theSite+='/'
toExplore = [theSite]
explored = []

while len(toExplore) != 0 :
    nextOne = toExplore.pop(0)
    if nextOne not in explored :
        explored.append(nextOne)
        fols, fils = exploreUrl(nextOne)
        
        print(fols)
        print(fils)
        
        toExplore.extend( [nextOne + s for s in fols] )
  
print("This is the end")
