from xml.etree.ElementTree import XML, fromstring, tostring
import xml.etree.ElementTree as ET
from os import walk
import re

def readFile(filePath):
    with open(filePath, 'r', encoding="utf8") as content_file:
        return content_file.read()

def writeFile(content, filePath):
    f = open(filePath, 'wb')
    f.write(content)
    f.close()

# def writeClass(content, class, filePath):
#     f = open(filePath, 'wb')

# def matchID()
#     return



def printIterables(obj, spaces):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print('%s%s' % (spaces, k))
                printIterables(v, '  %s' % spaces)
            else:
                print('%s%s : %s' % (spaces, k, v))
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                printIterables(v, '  %s' % spaces)
            else:
                print('%s%s' % (spaces, v))
    elif type(obj) == set:
        for v in obj:
            if hasattr(v, '__iter__'):
                printIterables(v, '  %s' % spaces)
            else:
                print('%s%s' % (spaces, v))
    else:
        print('%s%s' % (spaces, obj))

def convertOneFile(inFilePath, outFilePath):
    xmlText = readFile(inFilePath)
    eleLvl0 = XML(xmlText)

def isRating(string):
    if "Rating" in string:
        return True
    else:
        return False

def findRating(string):
    if isRating(string):
        return int(filter(str.isdigit, string))
    else:
        return 0

def matchKeywords(tag):
    return{
        'Air Miles' : 'sc_airmiles',
        'Cash Back' : 'sc_cashback',
        'Dining' : 'sc_dining',
        'Entertainment' : 'sc_entertainment',
        'Grocery' : 'sc_grocery',
        'Petrol' : 'sc_petrol',
        'Rewards' : 'sc_rewards',
        'Shopping' : 'sc_shopping',
    }[tag]

def insertCardName(fileName):




# # Convert logic here
# outputXml = eleLvl0
# # End
#
# text = tostring(outputXml)
# writeFile(text, outFilePath)
#
#
# rootStructure = {}
# tmpSet = set()
#
# convertOneFile('C:\\Users\\Huy\\Desktop\\hungbo\\MT\\singsaver\\xx.xml', 'C:\\Users\\Huy\\Desktop\\hungbo\\MT\\singsaver\\out.xml')

tree = ET.parse('C:/Users/Admin/Desktop/SmartMoney/moneysmart/american-express-personal-card.xml')
root = tree.getroot()
print matchKeywords('Air Miles')
for child in root:
    print child.tag, child.attrib



