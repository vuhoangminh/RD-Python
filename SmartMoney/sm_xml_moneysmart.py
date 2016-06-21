from xml.etree.ElementTree import XML, fromstring, ElementTree, Element
import xml.etree.ElementTree as ET
import os
import re
from os import walk
import re
import lxml.etree


list = ['Air Miles', 'Cash Back', 'Dining', 'Entertainment', 'Petrol', 'Grocery', 'Rewards', 'Shopping', 'Student'];


def matchKeywords(tag):
    return {
        'Air Miles': 'sc_airmiles',
        'Cash Back': 'sc_cashback',
        'Dining': 'sc_dining',
        'Entertainment': 'sc_entertainment',
        'Grocery': 'sc_grocery',
        'Petrol': 'sc_petrol',
        'Rewards': 'sc_rewards',
        'Shopping': 'sc_shopping',
        'Student': 'sc_students',
    }[tag]


def readFile(filePath):
    with open(filePath, 'r', encoding="utf8") as content_file:
        return content_file.read()


def writeFile(content, filePath):
    f = open(filePath, 'wb')
    f.write(content)
    f.close()


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


# get card name
def getCardName(pathName):
    text = os.path.basename(pathName)
    head, sep, tail = text.partition('.')
    return head


# get image path
def getImagePath(pathName):
    text = os.path.basename(pathName)
    head, sep, tail = text.partition('.')
    return './images/' + head + '.png'


# # get number
# def getNumber(str):
#     if ',' in str:
#         return re.sub("[^0-9]", "", str)
#     else:
#         if len(re.findall("\d+\.\d+", str))>0:
#             return re.findall("\d+\.\d+", str)[0]

def getNumber(str):
    head, sep, tail = str.partition('(')
    return re.sub("[^%.0-9]", "", head)



# get local & foreign income
def getEligibilityIncome(child):
    name = child.get('Name')
    if 'Eligibility' == name:
        for feature in child:
            # print feature.text
            if 'Non-Singaporean' in feature.text:
                for valuefeature in feature:
                    if getNumber(valuefeature.text)!= None:
                        foreignIncome = getNumber(valuefeature.text)
            else:
                for valuefeature in feature:
                    if getNumber(valuefeature.text) != None:
                        localIncome = getNumber(valuefeature.text)
    # if foreignIncome is None:
    #     foreignIncome='N/A'
    # if localIncome is None:
    #     localIncome = 'N/A'
    return (localIncome, foreignIncome)


def getCardInformation(child):
    otherFee = []
    principalFee = 'N/A'
    supplementaryFee = 'N/A'
    name = child.get('Name')
    if 'Card Information' == name:
        for feature in child:
            # print feature.text
            if 'Principal' in feature.text:
                for valuefeature in feature:
                    if getNumber(valuefeature.text) != None:
                        principalFee = getNumber(valuefeature.text)
            else:
                if 'Supplementary' in feature.text:
                    for valuefeature in feature:
                        if getNumber(valuefeature.text) != None:
                            supplementaryFee = getNumber(valuefeature.text)
                else:
                    otherFee.append(feature.text)
    # if principalFee is None:
    #     principalFee='N/A'
    # if supplementaryFee is None:
    #     supplementaryFee = 'N/A'
    # if otherFee is None:
    #     otherFee = 'N/A'
    return (principalFee, supplementaryFee, otherFee)


def getRatingAndFeature(child):
    featureList = []
    rating = child.get('Rating')
    for feature in child:
        featureList.append(feature.text)
    return (rating, featureList)

# doc = lxml.etree.parse(xml)
# count = doc.xpath('count(//author)')

def writeNode(pathNameOut,rootTemplate,tagName,content):
    newNodeStr = 'Feature'
    iCount=0
    for child in rootTemplate:
        if rootTemplate[iCount].get('Name') == tagName:
            newNode = ET.Element(newNodeStr)
            newNode.text = content
            rootTemplate[iCount].insert(len(child), newNode)
            treeTemplate.write(pathNameOut)
        iCount=iCount+1


def readandwrite(pathNameOut,pathNameIn):
    treeIn = ET.parse(pathNameIn)
    rootIn = treeIn.getroot()
    for child in rootIn:
        name = child.get('Name')
        if name in list:
            writeNode(pathNameOut, rootTemplate, matchKeywords(name) + '_rating', getRatingAndFeature(child)[0])
            for eachFeature in getRatingAndFeature(child)[1]:
                writeNode(pathNameOut, rootTemplate, matchKeywords(name) + '_details', eachFeature)
        else:
            if 'Card Information' == name:
                writeNode(pathNameOut, rootTemplate, 'sc_annual_fee', getCardInformation(child)[0])
                writeNode(pathNameOut, rootTemplate, 'sc_sup_annual_fee', getCardInformation(child)[1])
                for eachFeature in getCardInformation(child)[2]:
                    writeNode(pathNameOut, rootTemplate, 'sc_other_fee', eachFeature)
            else:
                if 'Eligibility' == name:
                    writeNode(pathNameOut, rootTemplate, 'sc_local_income', getEligibilityIncome(child)[0])
                    writeNode(pathNameOut, rootTemplate, 'sc_foreigner_income', getEligibilityIncome(child)[1])
    writeNode(pathNameOut, rootTemplate, 'sc_main_image', './images/'+ getCardName(pathNameIn)+'.png')
    writeNode(pathNameOut, rootTemplate, 'sc_card_name', getCardName(pathNameIn))


pathNameTemplate =  'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/template.xml'



for file in os.listdir("D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/moneysmart"):
    treeTemplate = ET.parse(pathNameTemplate)
    rootTemplate = treeTemplate.getroot()
    pathNameOut = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/moneysmart_out/' + file
    # print pathNameOut
    pathNameIn = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/moneysmart/' + file
    readandwrite(pathNameOut, pathNameIn)
