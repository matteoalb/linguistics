# TODO:
# TF/IDF analysis ?
# custom units (words->morphemes/tokens)
# multiple LCS choices, backtracking w/ match scores and global score (% corpus covered)


# Transcendental algebra
# ⪪⬃♡⌓
# İᐄᐲ⧊⩑i
# ✉
# ⊢
#
# \left( {{ᐲᐄi⧊}\over{ᐄi⧊}} + {{i⧊}\over{⧊}} \right)^{⪪}
# n(>İ)^{⊢⬃}=✉
#

import numpy as np

def LCS(strings, masks=None):
    strings = list(strings)
    if not strings:
        return ""
    if masks is None:
        masks = [[True] * len(s) for s in strings]
    else:
        masks = [list(m) for m in masks]
    if len(masks) != len(strings) or any( len(s) != len(m) for s, m in zip(strings, masks) ):
        raise ValueError("Each string must have a matching mask.")
    base, mod = 257, (1 << 61) - 1
    def hashes(s, mask, length):
        result = {}
        h = valid = 0
        power = pow(base, length, mod)
        for i, c in enumerate(s):
            h = (h * base + ord(c)) % mod
            if i >= length:
                h = (h - ord(s[i - length]) * power) % mod
            valid += mask[i]
            if i >= length:
                valid -= mask[i - length]
            if i >= length - 1 and valid == length:
                result.setdefault(h, []).append(i - length + 1)
        return result
    def check(length):
        first = hashes(strings[0], masks[0], length)
        others = [ hashes(s, m, length) for s, m in zip(strings[1:], masks[1:]) ]
        for h, positions in first.items():
            for pos in positions:
                candidate = strings[0][pos:pos + length]
                if all( any(s[p:p + length] == candidate for p in hs.get(h, [])) for s, hs in zip(strings[1:], others) ):
                    return candidate
        return None
    low, high = 1, min(map(len, strings))
    answer = ""
    while low <= high:
        mid = (low + high) // 2
        result = check(mid)
        if result is not None:
            answer = result
            low = mid + 1
        else:
            high = mid - 1
    return answer

def KMP (str):
    k = 0
    arr = [0]*len(str)
    i = 1
    while i<len(str):
        if str[i]== str[k]:
            k += 1
            arr[i] = k
            i += 1
        else:
            if k>0:
                k = arr[k-1]
            else:
                arr[i] = 0
                i += 1
    return arr

def KMP_occ (substr, str):
    arr = KMP(substr+"\0"+str)
    for i,v in enumerate(arr[2*len(substr):]):
        if v==len(substr):
            yield i

SENTENCES_RAW = [
    ("Ko nakonako ŋkoe","you are walking"),
    ("E nakonako te aiine","a woman is walking"),
    ("I takaakaro ŋai","I am playing"),
    ("E nakonako nakon te titooa Meeri","Mary is walking to the store"),
    ("A tekateka irarikin te auti aiine","women are sitting next to the house"),
    ("A tebotebo nakekei n te bong aei","people are bathing today"),
    ("I tebotebo inanon te auti ŋai","I am bathing in the house"),
    ("A takaakaro inanon te titooa ataei","children are playing in the store"),
    ("Ko tekateka ŋkoe ningaabong","you will sit tomorrow")
]

# PRE PROCESS UNITS (here words)

SENTENCES = []
for uk_str,k_str in SENTENCES_RAW:
    # here units are words
    k_str_units = [*map(lambda x : x.lower(), k_str.replace(".","").split(" "))] 
    SENTENCES += [ (uk_str, k_str_units, [(i!=" ") for i in uk_str]) ]

print(SENTENCES)


# for evaluating match likelihood
# todo higher TF/IDF => higher score ?
# what params to give ?
def score_function ( uk_guess_len, nb_intersect_sentences ):
    return .5 * np.log(uk_guess_len) + .3 * np.log(nb_intersect_sentences)

# "unit" refers to word/morpheme/token

# sentences : [
#          (
#               unknow language: str,
#               known language units: set/list(str),       -> or set(anything) eg set(int) for units
#               unknown_language_mask: list(bool)
#          )
#   ]
# known_matches : [                                Maybe not necessary ? if the masks are well defined
#       (
#           unknow language: str,
#           known language unit: str,              or anything
#       )
#   ]
def find_best_match ( sentences, known_matches ):

    all_units = set()
    for uk_str, units, uk_mask in sentences:
        all_units = all_units.union(units)

    possible_matches = []

    for unit in all_units:

        unit_uk_candidates = []
        possible_units = all_units.copy()
        for uk_str, units, uk_mask in sentences:
            
            if unit in units:
                possible_units = possible_units.intersection(units)
                unit_uk_candidates.append((uk_str,uk_mask))

        if len(possible_units)==1:
            # print(unit_uk_candidates)
            uk_guess = LCS(*zip(*unit_uk_candidates)).strip()
            if uk_guess != "":
                score = score_function( len(uk_guess), len(unit_uk_candidates) )
                possible_matches += [ (-score, uk_guess, unit) ] # score first for sort lol

    possible_matches.sort()

    if len(possible_matches)==0:
        return None

    print("Top 3 matches:")
    for score, uk_guess, unit in possible_matches[:3]:
        print(f"{-score:.2f} : {uk_guess} -> {unit}")

    _, uk_unit, unit = possible_matches[0]
    known_matches += [ (uk_unit, unit) ]

    for i, (uk_str, units, uk_mask) in enumerate(sentences):
        if unit in units:
            units.remove(unit)
            for s in KMP_occ(uk_unit, uk_str):
                for j in range(s,s+len(uk_unit)):
                    uk_mask[j] = False
        sentences[i] = uk_str, units, uk_mask

    return (uk_unit,unit) # new match


print()
matches = []
new_match = True
while new_match!=None:
    print()
    new_match = find_best_match(SENTENCES, matches)
print(matches)