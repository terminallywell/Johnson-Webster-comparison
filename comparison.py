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
# * -er/-re (fibre, centre, lustre, ...) search: [^aeiou]re\n
# * offense/offence
# * connection/connexion
# * willful/wilful, skillful/skilful
# * spectacle/specktacle
# * ax/axe, pickax/pickaxe

# Hyphenation (remove from NWAD)
# * afternoon/after-noon
