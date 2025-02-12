import os
import xml.etree.ElementTree as ET

def getxmls(word: str) -> list[ET.Element]:
    xmls = []

    n = 1
    while True:
        try:
            with open(f'XMLs/f1755-{word}-{n}.xml', encoding='utf8') as file:
                xmls.append(ET.parse(file).getroot())
                n += 1
        except FileNotFoundError:
            break

    return xmls


def extract_text(element: ET.Element) -> str:
    text = element.text or ''
    for child in element:
        text += extract_text(child)
        if child.tail:
            text += child.tail
    return text.strip()


# function to look up definitions of word from files
def getdefs(word: str) -> list[str]:
    defs = []
    
    for element in getxmls(word):
        for raw in element.findall('.//tei:def', {'tei': 'http://www.tei-c.org/ns/1.0'}):
            defs.append(extract_text(raw))

    return defs

# apply `changes` to headwords and definitions and compile into json

