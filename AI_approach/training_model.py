import csv
import math
import random
import re
import string

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def countUpper(password):
    count = 0
    for char in password:
        if char.isupper():
            count += 1
    return count


def countLower(password):
    count = 0
    for char in password:
        if char.islower():
            count += 1
    return count


def countDigits(password):
    count = 0
    for char in password:
        if char.isdigit():
            count += 1
    return count


def countSymbols(password):
    count = 0
    for char in password:
        if not char.isalnum():
            count += 1
    return count


def hasRepeat(password):
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            return 1
    return 0


def hasSequential(password):
    passwordLower = password.lower()

    for i in range(len(passwordLower) - 2):
        a = passwordLower[i]
        b = passwordLower[i + 1]
        c = passwordLower[i + 2]

        if a.isalpha() and b.isalpha() and c.isalpha():
            if ord(b) == ord(a) + 1 and ord(c) == ord(b) + 1:
                return 1

        if a.isdigit() and b.isdigit() and c.isdigit():
            if int(b) == int(a) + 1 and int(c) == int(b) + 1:
                return 1

    return 0


def estimateEntropy(password):
    poolSize = 0

    if any(char.islower() for char in password):
        poolSize += 26
    if any(char.isupper() for char in password):
        poolSize += 26
    if any(char.isdigit() for char in password):
        poolSize += 10
    if any(not char.isalnum() for char in password):
        poolSize += len(string.punctuation)

    if poolSize == 0:
        return 0

    return len(password) * math.log2(poolSize)


def numberAtEnd(password):
    if len(password) == 0:
        return 0
    return 1 if password[-1].isdigit() else 0


def symbolAtEnd(password):
    if len(password) == 0:
        return 0
    return 1 if not password[-1].isalnum() else 0


def hasYearPattern(password):
    matches = re.findall(r"(19\d{2}|20\d{2})", password)
    return 1 if len(matches) > 0 else 0


def alphaRatio(password):
    if len(password) == 0:
        return 0

    count = 0
    for char in password:
        if char.isalpha():
            count += 1

    return count / len(password)


def digitRatio(password):
    if len(password) == 0:
        return 0

    count = 0
    for char in password:
        if char.isdigit():
            count += 1

    return count / len(password)


def symbolRatio(password):
    if len(password) == 0:
        return 0

    count = 0
    for char in password:
        if not char.isalnum():
            count += 1

    return count / len(password)


def extractFeatures(password):
    length = len(password)
    upper = countUpper(password)
    lower = countLower(password)
    digits = countDigits(password)
    symbols = countSymbols(password)
    repeat = hasRepeat(password)
    sequential = hasSequential(password)
    entropy = estimateEntropy(password)
    endsDigit = numberAtEnd(password)
    endsSymbol = symbolAtEnd(password)
    yearPattern = hasYearPattern(password)
    alphaRatioValue = alphaRatio(password)
    digitRatioValue = digitRatio(password)
    symbolRatioValue = symbolRatio(password)

    return [
        length,
        upper,
        lower,
        digits,
        symbols,
        repeat,
        sequential,
        entropy,
        endsDigit,
        endsSymbol,
        yearPattern,
        alphaRatioValue,
        digitRatioValue,
        symbolRatioValue
    ]


def loadPasswords(filename, label):
    rows = []

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        passwords = file.read().splitlines()

    for password in passwords:
        if password.strip() == "":
            continue

        features = extractFeatures(password)
        rows.append(features + [label])

    return rows


weakRows = loadPasswords("data/weak_passwords.txt", 0)
strongRows = loadPasswords("data/strong_passwords.txt", 1)

allRows = weakRows + strongRows
random.shuffle(allRows)

print("Weak passwords loaded:", len(weakRows))
print("Strong passwords loaded:", len(strongRows))
print("Total rows:", len(allRows))

with open("data/password_dataset.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "length",
        "upper",
        "lower",
        "digits",
        "symbols",
        "repeat",
        "sequential",
        "entropy",
        "endsDigit",
        "endsSymbol",
        "yearPattern",
        "alphaRatio",
        "digitRatio",
        "symbolRatio",
        "label"
    ])
    writer.writerows(allRows)

print("Saved feature dataset to data/password_dataset.csv")

dataArray = np.array(allRows, dtype=float)
X = dataArray[:, :-1]
y = dataArray[:, -1]

XTrain, XTest, yTrain, yTest = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
XTrain = scaler.fit_transform(XTrain)
XTest = scaler.transform(XTest)

print("\nTensorFlow version:", tf.__version__)
print("GPUs detected:", tf.config.list_physical_devices("GPU"))

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(XTrain.shape[1],)),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

history = model.fit(
    XTrain,
    yTrain,
    validation_split=0.1,
    epochs=5,
    batch_size=64
)

testLoss, testAccuracy = model.evaluate(XTest, yTest)
print("\nTest Loss:", testLoss)
print("Test Accuracy:", testAccuracy)
print(f"Final Test Accuracy: {testAccuracy:.4f}")

print("\nSample Model Predictions: ")

testPasswords = [
    "Irfan123!",
    "Irfan",
    "Irfan#123",
    "Qx7!Lp9@Zk2",
    "P4$$w0rd",
    "Goku2026!"
]

for pw in testPasswords:
    features = np.array(extractFeatures(pw), dtype=float).reshape(1, -1)
    features = scaler.transform(features)

    modelProb = model.predict(features, verbose=0)[0][0]
    modelPred = 1 if modelProb >= 0.5 else 0

    print(f"\nPassword: {pw}")
    print(f"Predicted Label: {modelPred}")
    print(f"Prediction: {'Strong' if modelPred == 1 else 'Weak'}")
    print(f"Model Probability of Strong: {modelProb:.3f}")