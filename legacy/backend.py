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

SENTENCES_RAW = [
    ('Hello.', 'こんにちは。'),
    ('Good morning.', 'おはようございます。'),
    ('Good night.', 'おやすみなさい。'),
    ('Thank you.', 'ありがとうございます。'),
    ("I'm sorry.", 'すみません。'),
    ('Yes.', 'はい。'),
    ('No.', 'いいえ。'),
    ('My name is Ken.', '私の名前はケンです。'),
    ('Nice to meet you.', 'はじめまして。'),
    ('See you tomorrow.', 'また明日。'),
    ('I eat the apple.', '私はりんごを食べます。'),
    ('You eat the cake.', 'あなたはケーキを食べます。'),
    ('He eats the bread.', '彼はパンを食べます。'),
    ('She eats the apple.', '彼女はりんごを食べます。'),
    ('We eat the cake.', '私たちはケーキを食べます。'),
    ('They eat the bread.', '彼らはパンを食べます。'),
    ('I drink the water.', '私は水を飲みます。'),
    ('You drink the tea.', 'あなたはお茶を飲みます。'),
    ('He drinks the coffee.', '彼はコーヒーを飲みます。'),
    ('She drinks the water.', '彼女は水を飲みます。'),
    ('We drink the tea.', '私たちはお茶を飲みます。'),
    ('They drink the coffee.', '彼らはコーヒーを飲みます。'),
    ('I buy the book.', '私は本を買います。'),
    ('You buy the car.', 'あなたは車を買います。'),
    ('He buys the house.', '彼は家を買います。'),
    ('She buys the phone.', '彼女は電話を買います。'),
    ('We buy the newspaper.', '私たちは新聞を買います。'),
    ('They buy the movie.', '彼らは映画を買います。'),
    ('I see the movie.', '私は映画を見ます。'),
    ('You see the car.', 'あなたは車を見ます。'),
    ('He sees the house.', '彼は家を見ます。'),
    ('She sees the book.', '彼女は本を見ます。'),
    ('We see the picture.', '私たちは写真を見ます。'),
    ('They see the movie.', '彼らは映画を見ます。'),
    ('I read the book.', '私は本を読みます。'),
    ('You read the newspaper.', 'あなたは新聞を読みます。'),
    ('He reads the letter.', '彼は手紙を読みます。'),
    ('She reads the book.', '彼女は本を読みます。'),
    ('We read the newspaper.', '私たちは新聞を読みます。'),
    ('They read the letter.', '彼らは手紙を読みます。'),
    ('I make the cake.', '私はケーキを作ります。'),
    ('You make the bread.', 'あなたはパンを作ります。'),
    ('He makes the house.', '彼は家を作ります。'),
    ('She makes the picture.', '彼女は写真を作ります。'),
    ('We make the letter.', '私たちは手紙を作ります。'),
    ('They make the cake.', '彼らはケーキを作ります。'),
    ('I use the car.', '私は車を使います。'),
    ('You use the house.', 'あなたは家を使います。'),
    ('He uses the phone.', '彼は電話を使います。'),
    ('She uses the pen.', '彼女はペンを使います。'),
    ('We use the bag.', '私たちはかばんを使います。'),
    ('They use the car.', '彼らは車を使います。'),
    ('I write the letter.', '私は手紙を書きます。'),
    ('You write the book.', 'あなたは本を書きます。'),
    ('He writes the picture.', '彼は写真を書きます。'),
    ('She writes the letter.', '彼女は手紙を書きます。'),
    ('We write the book.', '私たちは本を書きます。'),
    ('They write the picture.', '彼らは写真を書きます。'),
    ('I like the book.', '私は本が好きです。'),
    ('I like the water.', '私は水が好きです。'),
    ('I like the tea.', '私はお茶が好きです。'),
    ('I like the coffee.', '私はコーヒーが好きです。'),
    ('I like the apple.', '私はりんごが好きです。'),
    ('I like the car.', '私は車が好きです。'),
    ('You like the house.', 'あなたは家が好きです。'),
    ('You like the phone.', 'あなたは電話が好きです。'),
    ('You like the newspaper.', 'あなたは新聞が好きです。'),
    ('You like the movie.', 'あなたは映画が好きです。'),
    ('You like the cake.', 'あなたはケーキが好きです。'),
    ('You like the bread.', 'あなたはパンが好きです。'),
    ('He likes the pen.', '彼はペンが好きです。'),
    ('He likes the bag.', '彼はかばんが好きです。'),
    ('He likes the letter.', '彼は手紙が好きです。'),
    ('He likes the picture.', '彼は写真が好きです。'),
    ('He likes the book.', '彼は本が好きです。'),
    ('He likes the water.', '彼は水が好きです。'),
    ('She likes the tea.', '彼女はお茶が好きです。'),
    ('She likes the coffee.', '彼女はコーヒーが好きです。'),
    ('She likes the apple.', '彼女はりんごが好きです。'),
    ('She likes the car.', '彼女は車が好きです。'),
    ('She likes the house.', '彼女は家が好きです。'),
    ('She likes the phone.', '彼女は電話が好きです。'),
    ('We like the newspaper.', '私たちは新聞が好きです。'),
    ('We like the movie.', '私たちは映画が好きです。'),
    ('We like the cake.', '私たちはケーキが好きです。'),
    ('We like the bread.', '私たちはパンが好きです。'),
    ('We like the pen.', '私たちはペンが好きです。'),
    ('We like the bag.', '私たちはかばんが好きです。'),
    ('They like the letter.', '彼らは手紙が好きです。'),
    ('They like the picture.', '彼らは写真が好きです。'),
    ('They like the book.', '彼らは本が好きです。'),
    ('They like the water.', '彼らは水が好きです。'),
    ('They like the tea.', '彼らはお茶が好きです。'),
    ('They like the coffee.', '彼らはコーヒーが好きです。'),
    ('I want the coffee.', '私はコーヒーが欲しいです。'),
    ('I want the apple.', '私はりんごが欲しいです。'),
    ('I want the car.', '私は車が欲しいです。'),
    ('I want the house.', '私は家が欲しいです。'),
    ('I want the phone.', '私は電話が欲しいです。'),
    ('You want the newspaper.', 'あなたは新聞が欲しいです。'),
    ('You want the movie.', 'あなたは映画が欲しいです。'),
    ('You want the cake.', 'あなたはケーキが欲しいです。'),
    ('You want the bread.', 'あなたはパンが欲しいです。'),
    ('You want the pen.', 'あなたはペンが欲しいです。'),
    ('He wants the bag.', '彼はかばんが欲しいです。'),
    ('He wants the letter.', '彼は手紙が欲しいです。'),
    ('He wants the picture.', '彼は写真が欲しいです。'),
    ('He wants the book.', '彼は本が欲しいです。'),
    ('He wants the water.', '彼は水が欲しいです。'),
    ('She wants the tea.', '彼女はお茶が欲しいです。'),
    ('She wants the coffee.', '彼女はコーヒーが欲しいです。'),
    ('She wants the apple.', '彼女はりんごが欲しいです。'),
    ('She wants the car.', '彼女は車が欲しいです。'),
    ('She wants the house.', '彼女は家が欲しいです。'),
    ('We want the phone.', '私たちは電話が欲しいです。'),
    ('We want the newspaper.', '私たちは新聞が欲しいです。'),
    ('We want the movie.', '私たちは映画が欲しいです。'),
    ('We want the cake.', '私たちはケーキが欲しいです。'),
    ('We want the bread.', '私たちはパンが欲しいです。'),
    ('They want the pen.', '彼らはペンが欲しいです。'),
    ('They want the bag.', '彼らはかばんが欲しいです。'),
    ('They want the letter.', '彼らは手紙が欲しいです。'),
    ('They want the picture.', '彼らは写真が欲しいです。'),
    ('They want the book.', '彼らは本が欲しいです。'),
    ('The book is big.', '本は大きいです。'),
    ('The water is small.', '水は小さいです。'),
    ('The tea is new.', 'お茶は新しいです。'),
    ('The coffee is old.', 'コーヒーは古いです。'),
    ('The apple is red.', 'りんごは赤いです。'),
    ('The car is blue.', '車は青いです。'),
    ('The house is good.', '家は良いです。'),
    ('The phone is beautiful.', '電話は美しいです。'),
    ('The newspaper is expensive.', '新聞は高いです。'),
    ('The movie is cheap.', '映画は安いです。'),
    ('This is a big book.', 'これは大きい本です。'),
    ('This is a big water.', 'これは大きい水です。'),
    ('This is a small tea.', 'これは小さいお茶です。'),
    ('This is a small coffee.', 'これは小さいコーヒーです。'),
    ('This is a new apple.', 'これは新しいりんごです。'),
    ('This is a new car.', 'これは新しい車です。'),
    ('This is an old house.', 'これは古い家です。'),
    ('This is an old phone.', 'これは古い電話です。'),
    ('This is a red newspaper.', 'これは赤い新聞です。'),
    ('This is a red movie.', 'これは赤い映画です。'),
    ('This is a blue cake.', 'これは青いケーキです。'),
    ('This is a blue bread.', 'これは青いパンです。'),
    ('This is a good pen.', 'これは良いペンです。'),
    ('This is a good bag.', 'これは良いかばんです。'),
    ('This is a beautiful letter.', 'これは美しい手紙です。'),
    ('This is a beautiful picture.', 'これは美しい写真です。'),
    ('This is an expensive book.', 'これは高い本です。'),
    ('This is an expensive water.', 'これは高い水です。'),
    ('This is a cheap tea.', 'これは安いお茶です。'),
    ('This is a cheap coffee.', 'これは安いコーヒーです。'),
    ('I go to Tokyo.', '私は東京に行きます。'),
    ('I go to school.', '私は学校に行きます。'),
    ('I go to the park.', '私は公園に行きます。'),
    ('I go to the station.', '私は駅に行きます。'),
    ('I go to Japan.', '私は日本に行きます。'),
    ('I go to the office.', '私は会社に行きます。'),
    ('I go to the library.', '私は図書館に行きます。'),
    ('I go to the restaurant.', '私はレストランに行きます。'),
    ('You go to Tokyo.', 'あなたは東京に行きます。'),
    ('You go to school.', 'あなたは学校に行きます。'),
    ('You go to the park.', 'あなたは公園に行きます。'),
    ('You go to the station.', 'あなたは駅に行きます。'),
    ('You go to Japan.', 'あなたは日本に行きます。'),
    ('You go to the office.', 'あなたは会社に行きます。'),
    ('You go to the library.', 'あなたは図書館に行きます。'),
    ('You go to the restaurant.', 'あなたはレストランに行きます。'),
    ('He goes to Tokyo.', '彼は東京に行きます。'),
    ('He goes to school.', '彼は学校に行きます。'),
    ('He goes to the park.', '彼は公園に行きます。'),
    ('He goes to the station.', '彼は駅に行きます。'),
    ('He goes to Japan.', '彼は日本に行きます。'),
    ('He goes to the office.', '彼は会社に行きます。'),
    ('He goes to the library.', '彼は図書館に行きます。'),
    ('He goes to the restaurant.', '彼はレストランに行きます。'),
    ('She goes to Tokyo.', '彼女は東京に行きます。'),
    ('She goes to school.', '彼女は学校に行きます。'),
    ('She goes to the park.', '彼女は公園に行きます。'),
    ('She goes to the station.', '彼女は駅に行きます。'),
    ('She goes to Japan.', '彼女は日本に行きます。'),
    ('She goes to the office.', '彼女は会社に行きます。'),
    ('She goes to the library.', '彼女は図書館に行きます。'),
    ('She goes to the restaurant.', '彼女はレストランに行きます。'),
    ('We go to Tokyo.', '私たちは東京に行きます。'),
    ('We go to school.', '私たちは学校に行きます。'),
    ('We go to the park.', '私たちは公園に行きます。'),
    ('We go to the station.', '私たちは駅に行きます。'),
    ('We go to Japan.', '私たちは日本に行きます。'),
    ('We go to the office.', '私たちは会社に行きます。'),
    ('We go to the library.', '私たちは図書館に行きます。'),
    ('We go to the restaurant.', '私たちはレストランに行きます。'),
    ('They go to Tokyo.', '彼らは東京に行きます。'),
    ('They go to school.', '彼らは学校に行きます。'),
    ('They go to the park.', '彼らは公園に行きます。'),
    ('They go to the station.', '彼らは駅に行きます。'),
    ('They go to Japan.', '彼らは日本に行きます。'),
    ('They go to the office.', '彼らは会社に行きます。'),
    ('They go to the library.', '彼らは図書館に行きます。'),
    ('They go to the restaurant.', '彼らはレストランに行きます。'),
    ('This is a book.', 'これは本です。'),
    ('This is a water.', 'これは水です。'),
    ('This is a tea.', 'これはお茶です。'),
    ('This is a coffee.', 'これはコーヒーです。'),
    ('This is an apple.', 'これはりんごです。'),
    ('This is a car.', 'これは車です。'),
    ('This is a house.', 'これは家です。'),
    ('This is a phone.', 'これは電話です。'),
    ('This is a newspaper.', 'これは新聞です。'),
    ('This is a movie.', 'これは映画です。'),
    ('This is a cake.', 'これはケーキです。'),
    ('This is a bread.', 'これはパンです。'),
    ('This is a pen.', 'これはペンです。'),
    ('This is a bag.', 'これはかばんです。'),
    ('This is a letter.', 'これは手紙です。'),
    ('This is a picture.', 'これは写真です。'),
]

for i,v in enumerate(SENTENCES_RAW):
    a,b = v
    SENTENCES_RAW[i] = b,a

with open("japanese.csv","w", encoding="utf-8") as f:
    for a,b in SENTENCES_RAW:
        f.write(f'{a};{b}\n')

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
    return .5 * np.log(uk_guess_len) + .7 * np.log(nb_intersect_sentences)

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
