'''
Effort to "fix" the spelling differences between Johnson and NWAD as much as possible
After building spelling adjustment dictionary, apply to Johnson and compile new json
'''
import os
from nwad import nwad

nwad_words = nwad.keys()

# johnson \ nwad
johnson_words = sorted(set([''.join(filename.split('-')[1:-1]) for filename in os.listdir('XMLs')]))

missing = {word for word in johnson_words if word not in nwad_words}

# write as file
with open('missing.txt', 'w') as file:
    file.write('\n'.join(sorted(missing)))
    # inspect missing.txt to pick up some morphemic differences, e.g. -ick vs. -ic

# compile morphemic differences as dictionary
import re

morph = { # lists subword replacements
    r'our$': 'or', # favour etc.
    r'ick$': 'ic', # magick etc.
    r'ack$': 'ac', # zodiack etc.
    r'([^aeioucr])re$': r'\1er', # lustre etc.
    r'ise$': 'ize', # equalise etc.
    r'eable$': 'able', # moveable etc.
    r'eably$': 'ably',

    # add more specific replacements as you examine `missing`
    r'ourabl': 'orabl', # favourable/favourably etc.
    r'alchym': 'alchim',
    r'lesly': 'lessly',
    r'lesness': 'lessness',
    r'^mould': 'mold',
    r'cloath': 'cloth',
    r'skeptic': 'sceptic',
}

# compile dict of {missing word: missing word but `morph` applied} --- "changes"
def apply_morph(word: str) -> str:
    for pattern, repl in morph.items():
        word = re.sub(pattern, repl, word)
    return word

# mainly for adjustment documentation purposes
changes = {} # lists whole-word changes, that can also be applied to inflected occurrences
for word in missing:
    new = apply_morph(word)
    if new != word:
        changes[word] = new

# add individual word differences to `changes`
changes['offence'] = 'offense'
changes['defence'] = 'defense'
changes['listner'] = 'listener'
changes['connexion'] = 'connection'
changes['wilful'] = 'willful'
changes['skilful'] = 'skillful'
changes['specktacle'] = 'spectacle'
# changes['axe'] = 'ax' # excluded due to concerns of "taxes" -> "taxs" etc. during apply_change
changes['pickaxe'] = 'pickax'
changes['skirre'] = 'skirr'
changes['ransome'] = 'ransom'
changes['rackoon'] = 'racoon'


with open('changes.csv', 'w') as file:
    for item in sorted(changes.items(), key=lambda p: p[0]):
        file.write(','.join(item) + '\n')


# apply `changes` to words in `missing` and compile new list
# words that either did not change or still not in NWAD after apply_morph
def apply_changes(string: str) -> str:
    for old, new in changes.items():
        string = string.replace(old, new)
    return string

missing_new = {apply_changes(word) for word in missing if apply_changes(word) not in nwad_words}


for word in missing:
    if apply_changes(word) == 'monks':
        print(word)

# write as file
with open('missing_new.txt', 'w') as file:
    file.write('\n'.join(sorted(missing_new)))

# look for close neighbors 
# from rapidfuzz import distance

# close = {}
# for word_j in missing_new:
#     for word_n in nwad_words:
#         if word_n[0] == word_j[0]: # only search same first letter to save on computation
#             if distance.DamerauLevenshtein.distance(word_j, word_n) < 2:
#                 close.setdefault(word_j, []).append(word_n)

# with open('close.csv', 'w') as file:
#     file.write('JOHNSON,NWAD\n')
#     for j in sorted(close.keys()):
#         for n in close[j]:
#             if n not in johnson_words:
#                 file.write(','.join((j, n)) + '\n')

# with open('close_mult.csv', 'w') as file:
#     file.write('JOHNSON,NWAD\n')
#     for j in sorted(close.keys()):
#         if len(close[j]) > 1:
#             for n in close[j]:
#                 if n not in johnson_words:
#                     file.write(','.join((j, n)) + '\n')
#             file.write('\n')
from xml_extract import getdefs

johnson = {}
for word in johnson_words:
    print(word)
    johnson[apply_changes(word)] = [apply_changes(d) for d in getdefs(word)]

import json
with open('johnson.json', 'w') as file:
    json.dump(johnson, file)
