'''
Preporcessing NWAD

We have JSON of NWAD from the M-W project.
For comparison purposes, we want to remove all non-alphabet characters (i.e. hyphens, apostrophes, spaces) from headwords
Also, make headwords lowercase while we're at it

+ Remove short PoS entries (artifact of PDF extraction)
'''

# load NWAD
import json

nwad_old = json.load(open('nwad_old.json'))

# Merge definition list if removing hyphen/apostrophe results in identical headword in NWAD
from collections import defaultdict

nwad = defaultdict(list)

for word, deflist in nwad_old.items():
    nwad[word.lower().replace('-', '').replace('’', '').replace(' ', '')].extend([d for d in deflist if len(d) > 5])

# check
# print(len(nwad_old['RE-FORM']) + len(nwad_old['REFORM']) == len(nwad['reform']))
