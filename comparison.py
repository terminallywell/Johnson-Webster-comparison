import re
import json
from difflib import SequenceMatcher

## tokenization:
## remove articles
## capture 2+ subseq (as opposed to 3)
def tokenize(string):
    # split, lower, remove article, strip punct & number
    return [word for word in re.findall(r'\b[a-zA-Z]+\b', string.lower()) if word not in {"a", "an", "the"}]


nwad = json.load(open('nwad.json'))
# remove POS entries from nwad
for word in nwad:
    old = nwad[word]
    new = [d for d in old if len(d) > 5]
    nwad[word] = new

johnson = json.load(open('johnson.json'))


junk = {'(the)', 'of', 'to', 'or', 'and', 'in', 'by', 'that', 'as', 'for', 'from'}
def nonjunklen(seq):
    return sum(1 for word in seq if word not in junk)


matches = []
for word in nwad:
    for sense_nw in nwad[word]:
        tn = tokenize(sense_nw)
        for sense_johnson in johnson.get(word.lower(), []):
            tj = tokenize(sense_johnson)
            sm = SequenceMatcher(None, tn , tj).get_matching_blocks()
            blocks = [tn[a:a+size] for a, b, size in sm if nonjunklen(tn[a:a+size]) > 0] # minimum block length = 1
            if (matchlen := sum(map(len, blocks))) > 2: # minimum total length = 3
                matches.append((
                    word,
                    sense_nw,
                    sense_johnson,
                    ' [...] '.join(' '.join(block) for block in blocks),
                    matchlen,
                    max(map(len, blocks))
                    ))

for i, t in enumerate(sorted(matches, key = lambda t: t[5])):
    print(f'{i+1}. {t[0]}: ... {t[3]} ...')

# match format: word/M-W sense/1812 sense/matching subsequence/total match length/longest contiguous match length
with open('johnson_matches.tsv', 'w', encoding='utf8') as file:
    file.write('word\tNWAD sense\tJohnson sense\tmatching subsequence\ttotal match length\tlongest contiguous match length\n')
    for match in matches:
        file.write('\t'.join((str(c).replace('\n', ' ') for c in match)) + '\n')



# from rapidfuzz import fuzz, utils, distance

# fuzz.ratio('aft', 'after')

# distance.DamerauLevenshtein.distance('connexion', 'connection')

# a1 = 'definition string with lovesick colour difference willfully ignorant.'
# a2 = 'this is a dummy string trying to throw off the fuzz definition string lovesic some color difference wilfully ignorant. '

# a1 = 'what if i added even more one matching string this is long this is a dummy string; followed by'
# a2 = 'one matching string this is long you are not supposed to be the same'

# fuzz.partial_ratio(a1, a2, processor=utils.default_process, score_cutoff=30)

# matches = []
# for word in nwad:
#     for sense_nw in nwad[word]:
#         if len(sense_nw) < 4:
#             continue
#         for sense_johnson in getdefs(word):
#             ratio = fuzz.partial_ratio(
#                 sense_nw,
#                 sense_johnson,
#                 processor=utils.default_process,
#                 score_cutoff=30
#             )
#             if ratio:
#                 matches.append(
#                     (
#                         word,
#                         sense_nw,
#                         sense_johnson,
#                         ratio
#                     )
#                 )

# for i, t in enumerate(sorted(matches, key = lambda t: t[3])):
#     print('\t'.join(map(str, t)))

# # match format: word/M-W sense/1812 sense/matching subsequence/total match length/longest contiguous match length
# with open('matches.tsv', 'w', encoding='utf8') as file:
#     file.write('word\tM-W sense\t1812 sense\tmatching subsequence\ttotal match length\tlongest contiguous match length\n')
#     for match in matches:
#         file.write('\t'.join(map(str, match)) + '\n')
