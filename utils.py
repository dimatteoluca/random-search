import io, random, webbrowser, time, keyboard
from tkinter import *


# Colors
grey = "#e0e0e0"
# Languages
eng = "./res/eng.txt"
ita = "./res/ita.txt"
separator = '\n'


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

# BROWSER MANAGEMENT
def doSearch(url, sleepTime, timeMultiplier):
    time.sleep(1.5*timeMultiplier)
    keyboard.press_and_release('ctrl+l')
    time.sleep(sleepTime)
    keyboard.write(url)
    time.sleep(0.5*timeMultiplier)
    keyboard.press_and_release('enter')

def openLink(link):
    webbrowser.open_new_tab(link)

def closeTab(timeMultiplier):
    time.sleep(0.5*timeMultiplier)
    keyboard.press_and_release('ctrl+w')

def closeTabs(browser, tabs, timeMultiplier):
    webbrowser.get(browser).open_new_tab("https://www.example.org/")
    tabs += 1
    for tab in range(tabs):
        closeTab(timeMultiplier)

def setBrowsersDevInterface(browser, timeMultiplier):
    time.sleep(1*timeMultiplier)
    if browser=="Opera":
        keyboard.press_and_release('ctrl+shift+c')
    else:
        keyboard.press_and_release('f12')

    if browser=="Firefox":
        time.sleep(0.5*timeMultiplier)
        keyboard.press_and_release('ctrl+shift+m')
    time.sleep(0.5*timeMultiplier)

# OTHERS
def getWordsList(language):

    if (language=="English"):
        file = eng
    elif (language=="Italiano"):
        file = ita

    with io.open(file, mode="r", encoding="utf-8") as file:
        allText = file.read()
        wordsList = list(map(str, allText.split(separator)))

    return wordsList

def randomWordsURLandSleepTime(engine, wordsList):

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

def getProgressBarValuePerSearch(pc, mobile, pcSearchesNumber, mobileSearchesNumber):
    if (pc & mobile):
        valuePerSearch = 100/(pcSearchesNumber + mobileSearchesNumber)
    elif not mobile:
        valuePerSearch = 100/(pcSearchesNumber)
    else:
        valuePerSearch = 100/(mobileSearchesNumber)
    return valuePerSearch
