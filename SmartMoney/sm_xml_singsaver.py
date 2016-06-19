from xml.etree.ElementTree import XML, fromstring, ElementTree, Element
import xml.etree.ElementTree as ET
import os
import re
from os import walk
import re
import lxml.etree

# moneysmart list and match
list_moneysmart = ['Air Miles', 'Cash Back', 'Dining', 'Entertainment', 'Petrol', 'Grocery', 'Rewards', 'Shopping', 'Student'];
def matchKeywords_moneysmart(tag):
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

# singsaver list and match
list_singasaver_oneinput = ['sc_promotion_end',
                            'sc_gift_end',
                            'sc_card_name',
                            'sc_cashback_percent',
                            'sc_airmile_per_sgd',
                            'sc_promotion_end',
                            'sc_gift_end',
                            'sc_annual_fee',
                            'sc_sup_annual_fee',
                            'sc_fc_trans_fee',
                            'sc_local_income',
                            'sc_foreigner_income',
                            'sc_main_card_age',
                            'sc_sup_card_age',
                            'sc_airmiles_rating',
                            'sc_cashback_rating',
                            'sc_dining_rating',
                            'sc_entertainment_rating',
                            'sc_grocery_rating',
                            'sc_petrol_rating',
                            'sc_rewards_rating',
                            'sc_shopping_rating',
                            'sc_student_rating',
                            'sc_main_image'
                             ];


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


# get number
# def getNumber(str):
#     if ',' in str:
#         return re.sub("[^0-9]", "", str)
#     else:
#         if len(re.findall("\d+\.\d+", str))>0:
#             return re.findall("\d+\.\d+", str)[0]

def getNumber(str):
    # head, sep, tail = str.partition('(')
    # return re.sub("[^%.0-9]", "", head)
    a=re.findall("[-]?\d+[\.,]?\d*[%]?", str)
    if len(a)>0:
        return a[0]
    else:
        return '-'


def getOnlyNumber(str):
    return re.sub("[^0-9]", "", str)


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

def readandwrite_moneysmart(pathNameOut,pathNameIn):
    treeIn = ET.parse(pathNameIn)
    rootIn = treeIn.getroot()
    for child in rootIn:
        name = child.get('Name')
        if name in list_moneysmart:
            # print name
            # print getRatingAndFeature(child)[0]
            # print matchKeywords(name) + '_rating'
            writeNode(pathNameOut, rootTemplate, matchKeywords_moneysmart(name) + '_rating', getRatingAndFeature(child)[0])
            # writeNode(pathNameOut, rootTemplate, matchKeywords(name) + '_details', getRatingAndFeature(child)[])
            for eachFeature in getRatingAndFeature(child)[1]:
                writeNode(pathNameOut, rootTemplate, matchKeywords_moneysmart(name) + '_details', eachFeature)
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

def combineStringInOtherFee(feature):
    for valuefeature in feature:
        if valuefeature.text != None and valuefeature.text != '-' and getOnlyNumber(valuefeature.text) != None and getOnlyNumber(valuefeature.text) != '':
            return feature.text + ': ' + valuefeature.text
            break
        else:
            return feature.text

def isFeatureExisting(feature,text):
    isExisting=False
    for valuefeature in feature:
        if text==valuefeature:
            isExisting = True
            break
    return isExisting


# write card information
def getCardInformation_singsaver(child):
    otherFee = []
    principalFee = 'N/A'
    supplementaryFee = 'N/A'
    transFee = 'N/A'
    name = child.get('Name')
    if 'Card Information' == name:
        for feature in child:
            # print feature.text
            if 'Additional Card Annual Fee' in feature.text:
                for valuefeature in feature:
                    if getNumber(valuefeature.text) != None and supplementaryFee == 'N/A':
                        supplementaryFee = getNumber(valuefeature.text)
            else:
                if 'Annual Fee' in feature.text:
                    for valuefeature in feature:
                        if getNumber(valuefeature.text) != None and principalFee == 'N/A':
                            principalFee = getNumber(valuefeature.text)
                else:
                    if 'Transaction Fee' in feature.text:
                        for valuefeature in feature:
                            if getNumber(valuefeature.text) != None and transFee == 'N/A':
                                transFee = getNumber(valuefeature.text)
                    else:
                        if feature.text!=combineStringInOtherFee(feature) and \
                                not isFeatureExisting(feature,combineStringInOtherFee(feature)):
                            otherFee.append(combineStringInOtherFee(feature))
    return (principalFee, supplementaryFee, otherFee, transFee)

def writeCardInformation_singsaver(cardInformation,pathNameOut,rootTemplate):
    writeNode(pathNameOut, rootTemplate, 'sc_annual_fee', cardInformation[0])
    writeNode(pathNameOut, rootTemplate, 'sc_sup_annual_fee', cardInformation[1])
    for feature in cardInformation[2]:
        writeNode(pathNameOut, rootTemplate, 'sc_other_fee', feature)
    writeNode(pathNameOut, rootTemplate, 'sc_fc_trans_fee', cardInformation[3])


# write eligibility
def getEligibility_singsaver(child):
    mainCardAge='N/A'
    supCardAge='N/A'
    localIncome='N/A'
    foreignIncome='N/A'
    name = child.get('Name')
    if 'Eligibility' == name:
        for feature in child:
            if 'Citizen' in feature.text:
                for valuefeature in feature:
                    if getNumber(valuefeature.text) != None and localIncome == 'N/A':
                        localIncome = getNumber(valuefeature.text)
            else:
                if 'Foreigner' in feature.text:
                    for valuefeature in feature:
                        if getNumber(valuefeature.text) != None and foreignIncome == 'N/A':
                            foreignIncome = getNumber(valuefeature.text)
                else:
                    if 'Supplementrary' in feature.text:
                        for valuefeature in feature:
                            if getNumber(valuefeature.text) != None and supCardAge == 'N/A':
                                supCardAge = getNumber(valuefeature.text)
                    else:
                        if 'Minimum Age' in feature.text:
                            for valuefeature in feature:
                                if getNumber(valuefeature.text) != None and mainCardAge == 'N/A':
                                    mainCardAge = getNumber(valuefeature.text)
    return (mainCardAge,supCardAge,localIncome,foreignIncome)

def writeEligibility_singsaver(eligibilityInformation,pathNameOut,rootTemplate):
    writeNode(pathNameOut, rootTemplate, 'sc_main_card_age', eligibilityInformation[0])
    writeNode(pathNameOut, rootTemplate, 'sc_sup_card_age', eligibilityInformation[1])
    writeNode(pathNameOut, rootTemplate, 'sc_local_income', eligibilityInformation[2])
    writeNode(pathNameOut, rootTemplate, 'sc_foreigner_income', eligibilityInformation[3])


# write main benefit
def getMainBenefit_singsaver(child):
    name = child.get('Name')
    mainBenefit=[]
    if 'GreateFor' == name:
        for feature in child:
            mainBenefit.append(feature.text)
    return mainBenefit

def writeMainBenefit_singsaver(mainBenefit,pathNameOut,rootTemplate):
    for feature in mainBenefit:
        writeNode(pathNameOut, rootTemplate, 'sc_main_benefit', feature)


# write disclosure
def getSmallprint_singsaver(child):
    name = child.get('Name')
    disClosure = []
    if 'SmallPrint' == name:
        for feature in child:
            disClosure.append(feature.text)
    return disClosure

def writeSmallprint_singsaver(disClosure,pathNameOut,rootTemplate):
    for feature in disClosure:
        writeNode(pathNameOut, rootTemplate, 'sc_disclosure', feature)


# write promotion
def getPromotion_singsaver(child):
    promotionCondition='N/A'
    promotionDetail = 'N/A'
    giftCondition='N/A'
    giftDetail = 'N/A'
    expireDate = 'N/A'
    name = child.get('Name')
    if 'Promotion' == name:
        for feature in child:
            if 'Online' in feature.get('Name'):
                for valuefeature in feature:
                    if 'Details' in valuefeature.get('Name'):
                        if valuefeature.text != None and promotionDetail == 'N/A':
                            promotionDetail = valuefeature.text
                    else:
                        if 'Conditions' in valuefeature.get('Name'):
                            if valuefeature.text != None and valuefeature.text != None \
                                    and promotionCondition == 'N/A':
                                promotionCondition = valuefeature.text
            else:
                if 'Gift' in feature.get('Name'):
                    for valuefeature in feature:
                        if 'Details' in valuefeature.get('Name'):
                            if valuefeature.text != None and giftDetail == 'N/A':
                                giftDetail = valuefeature.text
                        else:
                            if 'Conditions' in valuefeature.get('Name'):
                                if valuefeature.text != None and valuefeature.text != None \
                                        and giftCondition == 'N/A':
                                    giftCondition = valuefeature.text
                else:
                    if 'Expiry' in feature.get('Name'):
                        if feature.text != None and expireDate == 'N/A':
                            expireDate = feature.text
    return (promotionCondition,promotionDetail,giftCondition,giftDetail,expireDate)

def writePromotion_singsaver(promotionInformation,pathNameOut,rootTemplate):
    writeNode(pathNameOut, rootTemplate, 'sc_promotion_cond', promotionInformation[0])
    writeNode(pathNameOut, rootTemplate, 'sc_promotion_details', promotionInformation[1])
    writeNode(pathNameOut, rootTemplate, 'sc_gift_cond', promotionInformation[2])
    writeNode(pathNameOut, rootTemplate, 'sc_gift_details', promotionInformation[3])
    writeNode(pathNameOut, rootTemplate, 'sc_promotion_end', promotionInformation[4])
    writeNode(pathNameOut, rootTemplate, 'sc_gift_end', promotionInformation[4])


def readandwrite_singsaver(pathNameOut,pathNameIn):
    treeIn = ET.parse(pathNameIn)
    rootIn = treeIn.getroot()
    for child in rootIn:
        name = child.get('Name')
        if name == 'Card Information':
            # print getCardInformation_singsaver(child)
            writeCardInformation_singsaver(getCardInformation_singsaver(child), pathNameOut, rootTemplate)
        else:
            if name == 'Eligibility':
                # print getEligibility_singsaver(child)
                writeEligibility_singsaver(getEligibility_singsaver(child), pathNameOut, rootTemplate)
            else:
                if name == 'GreateFor':
                    # print getMainBenefit_singsaver(child)
                    writeMainBenefit_singsaver(getMainBenefit_singsaver(child), pathNameOut, rootTemplate)
                else:
                    if name == 'SmallPrint':
                        # print getSmallprint_singsaver(child)
                        writeSmallprint_singsaver(getSmallprint_singsaver(child), pathNameOut, rootTemplate)
                    else:
                        if name == 'Promotion':
                            writePromotion_singsaver(getPromotion_singsaver(child), pathNameOut, rootTemplate)
    writeNode(pathNameOut, rootTemplate, 'sc_main_image','./images/' + getCardName(pathNameIn) + '.png')
    writeNode(pathNameOut, rootTemplate, 'sc_card_name', getCardName(pathNameIn))

# for file in os.listdir("D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver"):
#     treeTemplate = ET.parse(pathNameTemplate)
#     rootTemplate = treeTemplate.getroot()
#     pathNameOut = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver_out/' + file
#     # print pathNameOut
#     pathNameIn = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver/' + file
#     # print pathNameIn
#     # readandwrite(pathNameOut, pathNameIn)



# for testing
pathNameTemplate =  'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/template.xml'
treeTemplate = ET.parse(pathNameTemplate)
rootTemplate = treeTemplate.getroot()
pathNameOut = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver_out/American-Express-Platinum-Credit-Card.xml'
# print pathNameOut
pathNameIn = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver/American-Express-Platinum-Credit-Card.xml'

for file in os.listdir("D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver"):
    treeTemplate = ET.parse(pathNameTemplate)
    rootTemplate = treeTemplate.getroot()
    pathNameOut = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver_out/' + file
    # print pathNameOut
    pathNameIn = 'D:/Users/RD/Documents/GitHub/RD-Python/SmartMoney/xml/singsaver/' + file
    # print pathNameIn
    print file
    readandwrite_singsaver(pathNameOut, pathNameIn)

# ss = ["apple-12.34 ba33na fanc-14.23yapple+45+67,56"]
# for s in ss:
#     print re.findall("[-]?\d+[\.,]?\d*", s)[0]