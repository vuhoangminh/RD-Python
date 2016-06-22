import xml.etree.ElementTree as ET
import os
import re

directory=os.path.dirname(os.path.realpath(__file__))+r'\xml\mergefinal\American Express Platinum Credit Card.xml'
directory=directory.replace("/", "\"")
# print directory
treeTemplate = ET.parse(directory)
rootTemplate = treeTemplate.getroot()

def isIncluded(fileName1,fileName2):
    isIncluded=True
    for word in fileName2:
        if word not in fileName1:
            isIncluded=False
            break
    return isIncluded

def splitFileName(fileName):
    fileNameLowerCase=fileName.lower()
    headFileName, sep, tail = fileNameLowerCase.partition('.')
    fileNamesplit = headFileName.split(' ')
    return fileNamesplit

def splitImageName(imageName):
    fileNameLowerCase=imageName.lower()
    headFileName, sep, tail = fileNameLowerCase.partition('.')
    fileNamesplit = headFileName.split('-')
    return fileNamesplit

def isSimilarName(imageName,fileName):
    fileNamesplit = splitFileName(fileName)
    imageNamesplit = splitImageName(imageName)
    if isIncluded(fileNamesplit,imageNamesplit) or isIncluded(imageNamesplit,fileNamesplit):
        return True
    else:
        return False

# def renameFile(fileName,newFileName):


# print splitString('American Express Personal Card.xml')

for fileName in os.listdir("C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/mergefinal"):
    headFileName, sep, tail = fileName.partition('.')
    abc=False
    for imageName in os.listdir("C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/images"):
        headImageName, sep, tail = imageName.partition('.')
        # print imageName
        if headFileName==headImageName:
            abc=True
            # print 'Matching'
            # print fileName
            # print imageName
    if not abc:
        print headFileName
        print 'not found'