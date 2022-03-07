import io, random, threading
from tkinter import *


grey = "#e0e0e0"


# WINDOW MANAGEMENT
def disableEvent():
    pass

# BUTTONS MANAGEMENT
def enableButton(btn, color):

    btn["state"] = NORMAL
    btn["bg"] = color
    btn["cursor"] = "hand2"

def disableButton(btn):

    btn["state"] = DISABLED
    btn["bg"] = grey
    btn["cursor"] = "arrow"


# OTHER
def getWordsList(language):

    if (language=="English"):
        file = "./res/eng.txt"

    elif (language=="Italiano"):
        file = "./res/ita.txt"

    with io.open(file, mode="r", encoding="utf-8") as file:
        allText = file.read()
        wordsList = list(map(str, allText.split('\n')))

    return wordsList

def randomWordsSelection(engine, wordsList):

    randomNumber = random.randrange(20)

    # 1 word,  05% chance
    if randomNumber==0:
        url = "+".join([engine, random.choice(wordsList)])
        sleepTime = 1.2

    # 2 words, 25% chance
    if randomNumber in range(1,6):
        url = "+".join([engine, random.choice(wordsList), random.choice(wordsList)])
        sleepTime = 2.2

    # 3 words, 40% chance
    if randomNumber in range(6,14):
        url = "+".join([engine, random.choice(wordsList), random.choice(wordsList), random.choice(wordsList)])
        sleepTime = 3

    # 4 words, 30% chance
    if randomNumber in range(14,20):
        url = "+".join([engine, random.choice(wordsList), random.choice(wordsList), random.choice(wordsList), random.choice(wordsList)])
        sleepTime = 3.7
    
    return (url, sleepTime)

def gottaStop(halt, close_function):

    if halt:
                thread = threading.Thread(target=close_function, daemon=True)
                thread.start()
                return True
