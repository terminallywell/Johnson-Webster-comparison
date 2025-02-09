# checking which headwords in Johnson is missing in NWAD

with open('words.txt', encoding='utf8') as file:
    johnson = set(file.read().split())

with open('NWAD_words.txt', encoding='utf8') as file:
    nwad = set(file.read().lower().replace('-', '').replace('’', '').split()) # remove hyphen in headwords

missing = {word for word in johnson if not word in nwad}

# words in johnson that are not in nwad
with open('missing.txt', 'w') as file:
    file.write('\n'.join(sorted(missing)))




# apply changes and make new list
# 1. identify words in johnson missing in nwad -> "missing"
# 2. identify spelling differences, compile dictionary
# 3. apply spelling correction on "missing"
# 4. now you have "old: new" for lemma
# 5. rewrite johnson so it catches inflected versions (e.g. "antagonise" -> "antagonize" in "antagonised")
import re

# morpheme differences
diff = {
    r'our$': 'or', # favour etc.
    r'ourabl': 'orabl', # favourable/favourably etc.
    r'ick$': 'ic', # magick etc.
    r'ack$': 'ac', # zodiack etc.
    r'([^aeioucr])re$': r'\1er',
    r'ise$': 'ize',
    r'eable$': 'able',
    r'eably$': 'ably',
    r'alchym': 'alchim',
}

def apply_diff(s: str) -> str:
    for old, new in diff.items():
        s = re.sub(old, new, s)
    return s


changes = {} # why is 'micmik:mimic' not in this?
for word in missing:
    new = apply_diff(word)
    if word != new:
        changes[word] = new

# add individual word differences to changes
changes['offence'] = 'offense'
changes['listner'] = 'listener'
changes['connexion'] = 'connection'
changes['wilful'] = 'willful'
changes['skilful'] = 'skillful'
changes['specktacle'] = 'spectacle'
changes['axe'] = 'ax'
changes['pickaxe'] = 'pickax'
changes['skirre'] = 'skirr'
changes['ransome'] = 'ransom'
changes['rackoon'] = 'racoon'
changes['cloath'] = 'cloth'


# apply changes and compile new missing list
# words that either didn't change or still not in nwad after changes applied
# missing_new = {changes.get(word, word) for word in missing if changes.get(word, word) not in nwad}
# missing_new = set()
# for word in missing:
#     new = apply_diff(changes, word)
#     if new not in nwad:
#         missing_new.add(new)

# with open('missing_new.txt', 'w') as file:
#     file.write('\n'.join(sorted(missing_new)))



###
# '''maybe run fuzzy match/distance search?'''
# from rapidfuzz import distance

# close = {}
# for word_j in missing_new:
#     for word_n in nwad:
#         if word_n[0] == word_j[0]: # only search same first letter to save on computation
#             if distance.DamerauLevenshtein.distance(word_j, word_n) < 2:
#                 close.setdefault(word_j, []).append(word_n)

# with open('close.csv', 'w') as file:
#     file.write('JOHNSON,NWAD\n')
#     for j in sorted(close.keys()):
#         for n in close[j]:
#             if n not in johnson:
#                 file.write(','.join((j, n)) + '\n')

# with open('close_mult.csv', 'w') as file:
#     file.write('JOHNSON,NWAD\n')
#     for j in sorted(close.keys()):
#         if len(close[j]) > 1:
#             for n in close[j]:
#                 if n not in johnson:
#                     file.write(','.join((j, n)) + '\n')
#             file.write('\n')


###
# Rewrite Johnson using `changes`
def apply_changes(s: str) -> str:
    for old, new in changes.items():
        s = s.replace(old, new)
    return s



