import xml.etree.ElementTree as ET
import os
import re

directory=os.path.dirname(os.path.realpath(__file__))+r'\xml\mergefinal\American Express Platinum Credit Card.xml'
directory=directory.replace("/", "\"")
print directory
treeTemplate = ET.parse(directory)
rootTemplate = treeTemplate.getroot()






for childTemplate in rootTemplate:
    name = childTemplate.get('Name')
    if name == 'sc_gift_details':
        for eachFeature in childTemplate:
            a=replaceNewLineByNewFeature(eachFeature.text)
            for eacha in a:
                print eacha