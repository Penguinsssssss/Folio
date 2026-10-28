# jotto botto 2

import random
import json

TRIALS = 10
DEBUG = False

def dbg(s):
    if DEBUG: print(s)

def restorelines():
    with open(r"c:\users\benja\downloads\jbparse1.txt", "r") as file:
        return file.read().splitlines()

def game(word):
    lines = restorelines()

    guess = ""
    guesses = 0
    dbg(f"{len(lines)} words remaining")
    while guess != word:
        nl = []
        guess = random.choice(lines)
        correct = len(set(guess) & set(word))
        for i in lines:
            if len(set(guess) & set(i)) == correct and i != guess:
                nl.append(i)
        lines = nl.copy()
        dbg(f"Guess {guess} has {correct} correct letters, {len(lines)} words remaining.")
        guesses += 1
    dbg(f"Guessed {guess} in {guesses} guesses")
    return guesses

def humanword():
    lines = restorelines()
    word = ""
    while word not in lines:
        word = input("Enter your word: ")
        if word not in lines: print("Invalid")
    return word
    
def trials():
    scores = []
    scoresdict = {}
    lines = restorelines()
    for word in lines:
        print(word)
        indivscores = []
        for _ in range(TRIALS):
            score = game(random.choice(lines))
            scores.append(score)
            indivscores.append(score)
        scoresdict[word] = sum(indivscores) / len(indivscores)

    with open(r"c:\users\benja\downloads\jottoworddiff2.json", "w") as f:
        json.dump(scoresdict, f, indent=4)
            
    print(f"Average guesses: {sum(scores) / len(scores)}")

def main():
    mode = False
    if mode:
        trials()
    else:
        while True:
            game(humanword())

if __name__ == "__main__":
    main()