# checking which headwords in Johnson is missing in NWAD

with open('words.txt', encoding='utf8') as file:
    johnson = set(file.read().split())

with open('NWAD_words.txt', encoding='utf8') as file:
    nwad = set(file.read().lower().replace('-', '').split()) # remove hyphen in headwords

missing = [word for word in johnson if not word in nwad]

with open('missing.txt', 'w') as file:
    file.write('\n'.join(sorted(missing)))


# Spelling differences
# * -or/-our (colour, ardour, labour, ...) search: our\n
# * -ic/-ick (academick, tactick, ...) search: ick\n
# * -er/-re (fibre, centre, lustre, ...) search: [^aeioucr]re\n
# * -ise/-ize (modernise, ...)
# * offense/offence
# * connection/connexion
# * willful/wilful, skillful/skilful
# * spectacle/specktacle
# * ax/axe, pickax/pickaxe
# * skirr/skirre
# * ransom/ransome
# * racoon/rackoon

# Hyphenation (remove from NWAD)
# * afternoon/after-noon

# apply changes
import re

johnson_new = []
for word in johnson:
    word = re.sub(r'our$', 'or', word)
    word = re.sub(r'ick$', 'ic', word)
    word = re.sub(r'([^aeioucr])re$', r'\1er', word)
    word = re.sub(r'ise$', r'ize', word)
    johnson_new.append(word)

# TODO: make dict of spelling changes e.g. {'colour': 'color'} for tabulating purposes

nwad_new = [word.replace('-', '') for word in nwad]

missing = [word for word in johnson_new if not word in nwad_new]

with open('missing_new.txt', 'w') as file:
    file.write('\n'.join(sorted(missing)))


# find matches
## tokenization:
## remove articles
## capture 2+ subseq (as opposed to 3)


