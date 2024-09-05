import os
import xml.etree.ElementTree as ET


words = [filename.split('-')[1] for filename in os.listdir('XMLs')]

# Spelling differences
# * -or/-our (colour, ardour, labour, ...) search: our\n
# * -ic/-ick (academick, tactick, ...) search: ick\n
# * -er/-re (fibre, centre, lustre, ...) search: [^aeiou]re\n
# * offense/offence
# * connection/connexion
# * willful/wilful, skillful/skilful
# * spectacle/specktacle
# * ax/axe, pickax/pickaxe
# Hyphenation (remove from NWAD)
# * afternoon/after-noon

def getxmls(word: str) -> list[ET.Element]:
    xmls = []

    n = 1
    while True:
        try:
            with open(f'XMLs/f1755-{word}-{n}.xml') as file:
                xmls.append(ET.parse(file).getroot())
                n += 1
        except FileNotFoundError:
            break

    return xmls


def extract_text(element: ET.Element) -> str:
    text = element.text
    for child in element:
        text += extract_text(child) # type: ignore
        text += child.tail # type: ignore
    return text.strip() # type: ignore


def getdefs(word: str) -> list[str]:
    defs = []
    
    for element in getxmls(word):
        for raw in element.findall('.//tei:def', {'tei': 'http://www.tei-c.org/ns/1.0'}):
            defs.append(extract_text(raw))

    return defs

for d in getdefs('match'):
    print(d + '\n')

############

for filename in os.listdir('XMLs'):
    with open('XMLs/' + filename, encoding='utf8') as file:
        if 'ref target' in file.read():
            print(filename)
