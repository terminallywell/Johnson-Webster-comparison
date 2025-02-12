import json
import os


nwad = json.load(open('nwad.json'))


with open('NWAD_words.txt', encoding='utf8') as file:
    nwad_list = set(file.read().lower().splitlines()) # remove hyphen in headwords


with open('NWAD_words.txt', encoding='utf8') as file:
    nwad_list2 = set(file.read().lower().replace('-', '').replace('’', '').splitlines()) # remove hyphen in headwords


{word for word in nwad_list2 if word not in nwad_list}

# nwad is 27 words shorter after removing hyphen and apostrophe --- find words in nwad_list that are hyphenated/apostrophed version of another

{word for word in nwad_list if ('-' in word or '’' in word) and (word.replace('-', '').replace('’', '') in nwad_list)}

nwad['LONG-SUFFERING']


words = sorted(set([filename.split('-')[1] for filename in os.listdir('XMLs')]))
# check if any johnson headword contains non-alphabet
{word for word in words if not word.isalpha()}
