from xml.etree.ElementTree import XML, fromstring, ElementTree, Element
import xml.etree.ElementTree as ET
import os
import re

list_bankname_upper = ['ANZ',
                       'CIMB',
                       'DBS',
                       'HSBC',
                       'ICBC',
                       'NTUC',
                       'OCBC',
                       'POSB',
                       'UOB'];
list_bankname_sentence = ['Citibank',
                          'Maybank'];
list_bankname_other = ['American Express',
                       'Standard Chartered'];

def getSentenceCase(string):
    return string.title()

def getRestName(fileName,numStart):
    head, sep, tail = fileName.partition('.')
    a=head.split('-')
    restName=''
    iCount=0
    for string in a:
        if iCount>numStart-1:
            restName=restName+' '+getSentenceCase(string)
        iCount=iCount+1
    return restName

def getCardName(fileName):
    head, sep, tail = fileName.partition('.')
    a=head.split('-')
    cardName=''
    if len(a)>0:
        if a[0].upper() in list_bankname_upper:
            cardName = a[0].upper() + getRestName(fileName,1)
        else:
            if a[0].capitalize() in list_bankname_sentence:
                cardName = a[0].title() + getRestName(fileName, 1)
            else:
                cardName = a[0].title() + ' ' + a[1].title() + getRestName(fileName, 2)
    return cardName.replace("'S", "'s")

def getCardNameOnly(pathName):
    text = os.path.basename(pathName)
    head, sep, tail = text.partition('.')
    return head

def getFilePathName(cardName):
    return cardName+'.xml'

def isMergeable(fileName1,fileName2):
    if fileName1 in fileName2:
        return '1'
    else:
        if fileName2 in fileName1:
            return '2'
        else:
            return '0'

def writeNode(pathNameOut,rootTemplate,tagName,content):
    newNodeStr = 'Feature'

    splittedContent=replaceNewLineByNewFeature(content)
    for eachLine in splittedContent:
        iCount = 0
        for child in rootTemplate:
            if rootTemplate[iCount].get('Name') == tagName:
                newNode = ET.Element(newNodeStr)
                newNode.text = eachLine
                rootTemplate[iCount].insert(len(child), newNode)
                treeTemplate.write(pathNameOut)
            iCount=iCount+1

def replaceNewLineByNewFeature(string):
    splittedString=[]
    if "\n""" in string:
        a = string.split("\n""")
        for abc in a:
            # print abc
            # print abc.lstrip()
            splittedString.append(abc.lstrip())
    else:
        splittedString.append(string.lstrip())
    return splittedString

def mergeTwoXML(rootTemplate, pathNameIn1, pathNameIn2, pathNameOut,cardName):
    treeIn1 = ET.parse(pathNameIn1)
    rootIn1 = treeIn1.getroot()
    treeIn2 = ET.parse(pathNameIn2)
    rootIn2 = treeIn2.getroot()
    for childTemplate in rootTemplate:
        name = childTemplate.get('Name')
        if name=='sc_card_name':
            writeNode(pathNameOut, rootTemplate, name, cardName)
        else:
            if name=='sc_main_image':
                writeNode(pathNameOut, rootTemplate, name, './images/'+ cardName + '.png')
            else:
                for childIn1 in rootIn1:
                    if childIn1.get('Name')==name:
                        if len(childIn1)>0:
                            for eachFeature in childIn1:
                                content=eachFeature.text
                                writeNode(pathNameOut, rootTemplate, name, content)
                        else:
                            for childIn2 in rootIn2:
                                if childIn2.get('Name') == name:
                                    if len(childIn2) > 0:
                                        for eachFeature in childIn2:
                                            content = eachFeature.text
                                            writeNode(pathNameOut, rootTemplate, name, content)


# for file in os.listdir("D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver"):
pathNameTemplate = 'C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/template.xml'


iCount=0
for fileName1 in os.listdir("C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/merge"):
    treeTemplate = ET.parse(pathNameTemplate)
    rootTemplate = treeTemplate.getroot()
    found=False
    for fileName2 in os.listdir("C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/merge"):
        pathNameIn1 = "C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/merge/" + fileName1
        pathNameIn2 = "C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/merge/" + fileName2
        pathNameOut = "C:/Users/Admin/Documents/GitHub/RD-Python/SmartMoney/xml/mergefinal/" + getCardName(fileName1) + '.xml'
        # print getCardName(fileName1)
        if fileName1!=fileName2:
            if isMergeable(getCardNameOnly(fileName1).lower(),getCardNameOnly(fileName2).lower())=='1':
                mergeTwoXML(rootTemplate, pathNameIn1, pathNameIn2, pathNameOut,getCardName(fileName1))
                found=True
            else:
                if isMergeable(getCardNameOnly(fileName1).lower(),getCardNameOnly(fileName2).lower())=='2':
                    found=True
    if not found:
        mergeTwoXML(rootTemplate, pathNameIn1, pathNameIn1, pathNameOut, getCardName(fileName1))