# checking which headwords in Johnson is missing in NWAD

with open('words.txt', encoding='utf8') as file:
    johnson = set(file.read().split())

with open('NWAD_words.txt', encoding='utf8') as file:
    nwad = set(file.read().lower().replace('-', '').split()) # remove hyphen in headwords

missing = [word for word in johnson if not word in nwad]

with open('missing.txt', 'w') as file:
    file.write('\n'.join(sorted(missing)))
