import os
import xml.etree.ElementTree as ET


words = [filename.split('-')[1] for filename in os.listdir('XMLs')]


def getheadword(filepath: str) -> str:
    return filepath.split('-')[1]

def getxml(word: str) -> ET.Element: # TODO: merge multiple files for one word
    with open(f'XMLs/f1755-{word}-1.xml') as file:
        return ET.parse(file).getroot()

def extract_text(element: ET.Element) -> str:
    text = element.text
    for child in element:
        text += extract_text(child) # type: ignore
        text += child.tail # type: ignore
    return text.strip() # type: ignore

def getdefs(element: ET.Element) -> list[str]:
    return list(map(extract_text, element.findall('.//tei:def', {'tei': 'http://www.tei-c.org/ns/1.0'})))


for d in getdefs(getxml('weapon')): # need to account for redirects
    print(d + '\n')

# TODO: spelling and hyphenation differences (offense/offence)
