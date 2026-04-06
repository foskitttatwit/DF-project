import random

numPasswords = 10000
outputFile = "data/strong_passwords.txt"

commonWords = [
    "password", "summer", "winter", "spring", "fall", "welcome", "dragon",
    "soccer", "baseball", "football", "monkey", "shadow", "sunshine",
    "flower", "princess", "mustang", "freedom", "hello", "secret",
    "cheese", "qwerty", "purple", "orange", "family", "love", "school"
]

normalWords = [
    "river", "stone", "blue", "tiger", "cactus", "moon", "train", "leaf",
    "quiet", "piano", "falcon", "forest", "glass", "storm", "maple",
    "ocean", "ember", "silver", "gold", "cloud", "sunset", "meadow",
    "rocket", "anchor", "comet", "breeze", "summit", "harbor", "willow",
    "drift", "sparrow", "pebble", "thunder", "lantern", "cedar", "blossom",
    "frost", "echo", "crystal", "ridge", "valley", "birch", "mist"
]

names = [
    "jack", "emma", "liam", "olivia", "noah", "ava", "lucas", "mia",
    "ethan", "sophia", "james", "isabella", "logan", "amelia",
    "mason", "harper", "elijah", "evelyn", "aiden", "abigail",
    "michael", "sarah", "david", "anna", "daniel", "grace",
    "josh", "lily", "ryan", "chloe"
]

symbols = ["!", "@", "#", "$", "%", "&", "*", "?"]

substitutions = {
    "a": "@",
    "o": "0",
    "i": "1",
    "e": "3",
    "s": "$"
}

years = [str(year) for year in range(2000, 2027)]

def randomDigits(minLen=1, maxLen=4):
    length = random.randint(minLen, maxLen)
    return "".join(random.choice("0123456789") for _ in range(length))


def maybeCapitalize(word):
    style = random.choice(["lower", "capitalized", "upper"])
    if style == "capitalized":
        return word.capitalize()
    if style == "upper":
        return word.upper()
    return word


def applySubstitution(word, chance=0.35):
    chars = list(word)
    changed = False

    for i in range(len(chars)):
        lowerChar = chars[i].lower()
        if lowerChar in substitutions and random.random() < chance:
            chars[i] = substitutions[lowerChar]
            changed = True

    if not changed and len(chars) > 0:
        possibleIndexes = [i for i, c in enumerate(chars) if c.lower() in substitutions]
        if possibleIndexes and random.random() < 0.5:
            index = random.choice(possibleIndexes)
            chars[index] = substitutions[chars[index].lower()]

    return "".join(chars)


def getCommonBase():
    pool = commonWords + names
    return random.choice(pool)


def getNormalBase():
    pool = normalWords + names
    return random.choice(pool)

def generatePredictablePassword():
    pattern = random.choice([
        "wordYearSymbol",
        "wordDigitsSymbol",
        "nameDigitsSymbol",
        "capitalWordDigitsSymbol",
        "subWordDigitsSymbol",
        "wordSymbolDigits",
        "nameYearSymbol",
        "twoCommonParts"
    ])

    word = getCommonBase()
    name = random.choice(names)

    if pattern == "wordYearSymbol":
        return maybeCapitalize(word) + random.choice(years) + random.choice(symbols)

    if pattern == "wordDigitsSymbol":
        return maybeCapitalize(word) + randomDigits(1, 3) + random.choice(symbols)

    if pattern == "nameDigitsSymbol":
        return maybeCapitalize(name) + randomDigits(1, 3) + random.choice(symbols)

    if pattern == "capitalWordDigitsSymbol":
        return word.capitalize() + randomDigits(2, 4) + random.choice(symbols)

    if pattern == "subWordDigitsSymbol":
        return applySubstitution(word.capitalize()) + randomDigits(1, 3) + random.choice(symbols)

    if pattern == "wordSymbolDigits":
        return maybeCapitalize(word) + random.choice(symbols) + randomDigits(1, 3)

    if pattern == "nameYearSymbol":
        return name.capitalize() + random.choice(years) + random.choice(symbols)

    if pattern == "twoCommonParts":
        part1 = maybeCapitalize(random.choice(commonWords))
        part2 = random.choice(["123", "12", "1", "2024", "2025", "99", "7"])
        return part1 + part2 + random.choice(symbols)

    return maybeCapitalize(word) + "123!"

def generateModeratelyStrongPassword():
    pattern = random.choice([
        "twoWordsDigits",
        "twoWordsSymbolDigits",
        "nameWordDigits",
        "wordNameSymbolDigits",
        "subWordWordDigits",
        "twoWordsYearSymbol",
        "threePartSimple"
    ])

    w1 = maybeCapitalize(getNormalBase())
    w2 = maybeCapitalize(getNormalBase())
    w3 = maybeCapitalize(getNormalBase())

    if pattern == "twoWordsDigits":
        return w1 + w2 + randomDigits(2, 4)

    if pattern == "twoWordsSymbolDigits":
        return w1 + w2 + random.choice(symbols) + randomDigits(2, 4)

    if pattern == "nameWordDigits":
        return maybeCapitalize(random.choice(names)) + maybeCapitalize(random.choice(normalWords)) + randomDigits(2, 4)

    if pattern == "wordNameSymbolDigits":
        return maybeCapitalize(random.choice(normalWords)) + maybeCapitalize(random.choice(names)) + random.choice(symbols) + randomDigits(2, 4)

    if pattern == "subWordWordDigits":
        return applySubstitution(w1) + w2 + randomDigits(2, 4)

    if pattern == "twoWordsYearSymbol":
        return w1 + w2 + random.choice(years) + random.choice(symbols)

    if pattern == "threePartSimple":
        return w1 + w2 + w3

    return w1 + w2 + "42"

def generateActuallyStrongPassword():
    pattern = random.choice([
        "threeWordsSymbolDigits",
        "mixedOrder",
        "substitutionHeavy",
        "longPassphrase",
        "nameWordWordSymbolDigits"
    ])

    w1 = maybeCapitalize(random.choice(normalWords))
    w2 = maybeCapitalize(random.choice(normalWords))
    w3 = maybeCapitalize(random.choice(normalWords))
    name = maybeCapitalize(random.choice(names))

    if pattern == "threeWordsSymbolDigits":
        return w1 + w2 + w3 + random.choice(symbols) + randomDigits(2, 4)

    if pattern == "mixedOrder":
        return randomDigits(2, 4) + w1 + random.choice(symbols) + w2 + random.choice(symbols)

    if pattern == "substitutionHeavy":
        return applySubstitution(w1, 0.5) + applySubstitution(w2, 0.5) + random.choice(symbols) + randomDigits(2, 4)

    if pattern == "longPassphrase":
        return w1 + w2 + w3 + randomDigits(2, 4)

    if pattern == "nameWordWordSymbolDigits":
        return name + w1 + w2 + random.choice(symbols) + randomDigits(2, 4)

    return w1 + w2 + w3 + "!42"

def generatePassword():
    category = random.random()

    if category < 0.50:
        return generatePredictablePassword()
    elif category < 0.80:
        return generateModeratelyStrongPassword()
    else:
        return generateActuallyStrongPassword()

generated = set()

while len(generated) < numPasswords:
    password = generatePassword()
    if len(password) >= 8:
        generated.add(password)

with open(outputFile, "w") as file:
    for password in generated:
        file.write(password + "\n")

print(f"Generated {len(generated)} passwords into {outputFile}")