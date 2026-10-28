#Jotto Botto

import random
from pathlib import Path

def loadWords(filepath):
    with open(filepath, 'r') as f:
        return set(word.strip().lower() for word in f if word.strip())

def getWords(chars):
    script_dir = Path(__file__).parent
    words = list(loadWords(script_dir / "wordsList.txt"))
    
    for i in range(len(words)):
        words[i] = words[i].lower()
    out = []
    
    for i in words:
        if len(i) == chars and isValidJottoWord(i):
            out.append(i)
    return out

def isValidJottoWord(word):
    letters = set()
    valid = True
    
    for i in word:
        
        if i in letters:
            valid = False
            break
        
        else:
            letters.add(i)
    
    if valid: return True
    else: return False

def assignScores(words):
    letterValues = {
        "a": 8.2,
        "b": 1.5,
        "c": 2.8,
        "d": 4.3,
        "e": 12.7,
        "f": 2.2,
        "g": 2.0,
        "h": 6.1,
        "i": 7.0,
        "j": 0.2,
        "k": 0.8,
        "l": 4.0,
        "m": 2.4,
        "n": 6.7,
        "o": 7.5,
        "p": 1.9,
        "q": 0.1,
        "r": 6.0,
        "s": 6.3,
        "t": 9.1,
        "u": 2.8,
        "v": 1.0,
        "w": 2.4,
        "x": 0.2,
        "y": 2.0,
        "z": 0.1,
    }
    scores = {}
    
    for i in words:
        score = 0
        
        for j in i:
            score += letterValues[j]
        scores[i] = round(score ** 2, 1)
    return scores

def chooseWord(words, difficulty):
    if not difficulty == 0:
        l = list(words.items())
        keep = range(round((((10 - difficulty) / 10)) * len(words)), round((((11 - difficulty) / 10)) * len(words)))
        pwords = [l[i] for i in keep if i < len(l)]
        pwords = dict(pwords)
    
    else: pwords = words
    entries = sum(pwords.values())
    choice = round(random.random() * entries, 1)
    
    for k, v in pwords.items():
        choice -= v
        
        if choice <= 0:
            return (k, v)

def findPercentile(words, word):
    l = {key: i for i, key in enumerate(words)}
    return round((l.get(word) / len(words)) * 100, 1)

def game(word, strength, chars, baseWords, valueWords, cheats):
    
    print() #\n
    print(f"The word has a difficulty of {strength}, its difficulty being in the top {findPercentile(valueWords, word)}% of all {len(baseWords)} valid words.")
    print("For list of valid commands, enter '/help'")
    
    guess = None
    guesses = 0
    
    message = f"Input a {chars}-letter word with no repeating characters: "
    
    while guess != word:
        guess = input(message)
        
        if guess[0] == "/":
            message = f"Input a {chars}-letter word with no repeating characters: "
            if guess == "/help":
                print("List of valid commands: ")
                print("/forfeit - reveal word and end game")
                print("/guesses - reveals number of guesses")
                print("/help - index of commands")
                if cheats: print("/hint - returns one random letter in the word (cheat)")
                if cheats: print("/peek <args> - returns True/False for each letter input (cheat)")
            
            elif "/peek" in guess and cheats:
                for i in range(6, len(guess)):
                    if guess[i] in word:
                        print(f"'{guess[i]}' is in the mystery word.")
                    else:
                        print(f"'{guess[i]}' isn't in the mystery word.")
            
            elif guess == "/hint" and cheats:
                print(f"The word contain the letter '{word[random.randint(0, chars - 1)]}'.")
            
            elif guess == "/forfeit":
                print(f"You forfeit in {guesses} guesses. The word was '{word}'")
                break
            
            elif guess == "/guesses":
                print(f"You have made {guesses} guesses.")
            
            else:
                print("Unrecognized command, please try again.")
            
            print() #\n
            
        elif guess == word:
            guess += 1
            print(f"You have guessed the word in {guesses} guesses.")
            break
        
        elif len(guess) != chars:
            message = f"That word does not have {chars} characters. Please try again: "
        
        elif not isValidJottoWord(guess):
            message = f"That word contains repeating characters. Please try again: "
        
        elif guess not in baseWords:
            message = f"That word does not appear in the English Lexicon. Please try again: "
        
        else:
            message = f"Input a {chars}-letter word with no repeating characters: "
            correct = 0
            for i in guess:
                if i in word: correct += 1
            print(f"Your guess {guess} contains {correct} correct letter(s)." + "\n")
            guesses += 1

def main():
    cheats = False
    chars = 5
    difficulty = 1
    message = f"Welcome to Jotto Botto. Please enter a command. For a list of all commands, type /help: "
    while True:
        
        command = input(message)
        message = f"Please enter a command. For a list of all commands, type /help: "
        
        if command == "/help":
            print("/help - lists all valid commands")
            print("/rules - returns a list of Jotto rules")
            print("/settings - lists all current settings")
            print("    /settings chars <args> - sets number of characters in the target word")
            print("    /settings cheats <args> - enables or disables in game cheating commands")
            print("    /settings difficulty <args> - select word difficulty 1(easiest) - 10(hardest). Enter '0' for a random difficulty")
            print("/start - starts the game")
            message = f"Please enter a command. For a list of all commands, type /help: "
        
        elif command == "/settings":
            print(f"Cheats {cheats}")
            print(f"Chars {chars}")
            print(f"Difficulty {difficulty}")
            message = f"Please enter a command. For a list of all commands, type /help: "
        
        elif "/settings cheats " in command:
            if command[17].lower() == "t":
                cheats = True
                print("Enabled cheats")
                message = f"Please enter a command. For a list of all commands, type /help: "
            
            elif command[17].lower() == "f":
                cheats = False
                print("Disabled cheats")
                message = f"Please enter a command. For a list of all commands, type /help: "
            
            else:
                message = "Invalid assignment. Please enter 'True' or 'False': "
        
        elif "/settings chars " in command:
            try:
                if 16 > int(command[16:]) > 0: 
                    chars = int(command[16:])
                    print(f"Set chars to {chars}")
                    message = f"Please enter a command. For a list of all commands, type /help: "
                else: message = f"No valid words of length {command[16:]}, please try again."
            
            except ValueError:
                message = "Invalid assignment. Please enter a number: "
        
        elif "/settings difficulty " in command:
            try:
                if 11 > int(command[21:]) > -1: 
                    difficulty = int(command[21:])
                    print(f"Set difficulty to {difficulty}")
                    message = f"Please enter a command. For a list of all commands, type /help: "
                else: message = f"Difficulty of {command[21:]} is invalid, please try again: "
            
            except ValueError:
                message = "Invalid assignment. Please enter a number: "
        
        elif "/rules" in command:
            print("Rules of jotto:")
            print("Jotto is a game played between two players.")
            print("At the start of the game, each player chooses an english word of a predecided length.")
            print("   (This word must not contain repeating characters)")
            print("Each turn, a player will guess a valid word")
            print("   (This word must not contain repeating characters and must be of the predetermined length)")
            print("The other player will tell them how many letters from thier guess are contained in their secret word.")
            print("Play alternates and first player to guess the others secret word wins.")
            print("This program is designed to be a practice tool.")
            print("You are the only player and are guessing against an algorithm who will select a random english word.")
            message = f"Please enter a command. For a list of all commands, type /help: "
            
        elif command == "/start":
            baseWords = sorted(getWords(chars))
            words = assignScores(baseWords)
            words = dict(sorted(words.items(), key=lambda item: item[1]))
            word, strength = chooseWord(words, difficulty)
            game(word, strength, chars, baseWords, words, cheats)
            message = f"Please enter a command. For a list of all commands, type /help: "
        
        else:
            if command[0] == "/":
                message = "Invalid command, please try again: "
            
            else:
                message = "Invalid command, try using '/': "
        print() #\n

main()