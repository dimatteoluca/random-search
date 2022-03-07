import random, webbrowser, time, io, keyboard, threading, ctypes
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


# BROWSERS 
webbrowser.register("Chrome", None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
webbrowser.register("Edge", None, webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
#webbrowser.register("Firefox", None, webbrowser.BackgroundBrowser("C:\Program Files\Mozilla Firefox\Firefox.exe"))

# ENGINES
bing =      "https://www.bing.com/search?q="
google =    "https://www.google.com/search?q="
ecosia =    "https://www.ecosia.org/search?q="

# COLORS
cyan =      "#0ee0ed"
azure =     "#0ca3ea"
blue =      "#0f388e"
pink =      "#d372a9" #bd74ad
purple =    "#7c6bac"
grey =      "#e0e0e0"

# INITIAL STATE
language =          "English"
browser =           "Chrome"
engine =            google
pc =                True
mobile =            True
pcSearches =        5
mobileSearches =    5
tabs =              0
loop =              True

# WINDOW POSITION & SIZE
user32 = ctypes.windll.user32
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)
positionX = int((screenWidth/4)*3)
positionY = int((screenHeight/5)*2)
windowWidth = 410
#windowHeight = auto
settingsWidth = 280
settingsHeight = 350


# FUNCTIONS BEGINNING ///////////////////////////////////////////////////////////////////////////////////////////////
def buttonsReset1():

    start_btn["state"] = NORMAL
    start_btn["bg"] = pink
    start_btn["cursor"] = "hand2"

    stop_btn["state"] = DISABLED
    stop_btn["bg"] = grey
    stop_btn["cursor"] = "arrow"

    settings_btn["state"] = NORMAL
    settings_btn["bg"] = azure
    settings_btn["cursor"] = "hand2"

def buttonsReset2():

    start_btn["state"] = DISABLED
    start_btn["bg"] = grey
    start_btn["cursor"] = "arrow"

    stop_btn["state"] = NORMAL
    stop_btn["bg"] = purple
    stop_btn["cursor"] = "hand2"

    settings_btn["state"] = DISABLED
    settings_btn["bg"] = grey
    settings_btn["cursor"] = "arrow"

def buttonsReset3():

    start_btn["state"] = NORMAL
    start_btn["bg"] = pink
    start_btn["cursor"] = "hand2"

    settings_btn["state"] = NORMAL
    settings_btn["bg"] = azure
    settings_btn["cursor"] = "hand2"

def selectedLanguage():

    if (language=="English"):
        file = "./res/eng.txt"

    elif (language=="Italiano"):
        file = "./res/ita.txt"

    with io.open(file, mode="r", encoding="utf-8") as file:
        allText = file.read()
        wordsList = list(map(str, allText.split('\n')))

    return wordsList

def randomWordsSelection(words):

    randomNumber = random.randrange(20)

    # 1 word,  05% chance
    if randomNumber==0:
        url = "+".join([engine, random.choice(words)])
        sleepTime = 1.2

    # 2 words, 25% chance
    if randomNumber in range(1,6):
        url = "+".join([engine, random.choice(words), random.choice(words)])
        sleepTime = 2.2

    # 3 words, 40% chance
    if randomNumber in range(6,14):
        url = "+".join([engine, random.choice(words), random.choice(words), random.choice(words)])
        sleepTime = 3

    # 4 words, 30% chance
    if randomNumber in range(14,20):
        url = "+".join([engine, random.choice(words), random.choice(words), random.choice(words), random.choice(words)])
        sleepTime = 3.7
    
    return (url, sleepTime)

def gottaStop():

    if not loop:
                thread = threading.Thread(target=close, daemon=True)
                thread.start()
                return True

def singleSearch(words):

    rws = randomWordsSelection(words)
    url = rws[0]
    sleepTime = rws[1]

    time.sleep(1)
    if gottaStop(): return
    keyboard.press_and_release('ctrl+l')
    time.sleep(sleepTime)
    keyboard.write(url)
    time.sleep(0.5)
    keyboard.press_and_release('enter')

def realSearch():

    global tabs
    global mobileSearches

    wordsList = selectedLanguage()

    progress['value'] = 0
    if (pc & mobile):
        valuePerSearch = 100/(pcSearches + mobileSearches)
    elif not mobile:
        valuePerSearch = 100/(pcSearches)
    else:
        valuePerSearch = 100/(mobileSearches)

    if pc:

        webbrowser.get(browser).open_new_tab("starting-pc-searches")
        tabs = 1

        for search in range(pcSearches):

            if gottaStop(): return
            singleSearch(wordsList)
            progress['value'] += valuePerSearch

        time.sleep(2)
        if not mobile:
            keyboard.press_and_release('ctrl+w')

    if mobile:

        webbrowser.get(browser).open_new_tab("starting-mobile-searches")
        tabs += 1
        time.sleep(1)
        keyboard.press_and_release('f12')
        #if browser=="Firefox":          # Firefox does one less search than other browsers and doesn't go in device mode by default
        #    mobileSearches += 1
        #    time.sleep(1)
        #    keyboard.press_and_release('ctrl+shift+m')
        #tabs = 1

        for search in range(mobileSearches):

            if gottaStop(): return
            singleSearch(wordsList)
            #if browser=='Firefox' and search==(mobileSearches-1): break      # read previous comment
            progress['value'] += valuePerSearch

        time.sleep(2)
        keyboard.press_and_release('ctrl+w')
        if pc:
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')

    buttonsReset1()

def search():

    buttonsReset2()
    
    global loop
    loop = True

    thread = threading.Thread(target=realSearch, daemon=True)
    thread.start()

def stop():

    #Buttons reset
    stop_btn["state"] = DISABLED
    stop_btn["bg"] = grey
    stop_btn["cursor"] = "arrow"

    global loop
    loop = False

def close():

    global tabs
    
    webbrowser.get(browser).open_new_tab("closing-tabs")
    tabs += 1

    for tab in range(tabs):

        time.sleep(0.5)
        keyboard.press_and_release('ctrl+w')
        tabs -= 1

    progress['value'] = 100
    buttonsReset3()

def ok(newWindow, la_clicked, br_clicked, en_clicked, mo_clicked, ps_entry, ms_entry):

    global pc
    global mobile
    global language
    global browser
    global engine
    global pcSearches
    global mobileSearches

    language = la_clicked.get()
    browser = br_clicked.get()
    if (en_clicked.get() == "Bing"):
        engine = bing
    elif (en_clicked.get() == "Ecosia"):
        engine = ecosia
    else:
        engine = google
    if (mo_clicked.get() == "PC + Mobile"):
        pc = True
        mobile = True
    elif (mo_clicked.get() == "PC"):
        pc = True
        mobile = False
    else:
        pc = False
        mobile = True
    if (ps_entry != ""):
        try:
            pcSearches = int(ps_entry.get())
        except:
            1+1
    if (ms_entry != ""):
        try:
            mobileSearches = int(ms_entry.get())
        except:
            1+1

    newWindow.destroy()
    buttonsReset3()

def myDestroy(newWindow):

    newWindow.destroy()
    buttonsReset3()

def disable_event():
    pass

def settings():

    #Buttons reset
    start_btn["state"] = DISABLED
    start_btn["bg"] = grey
    start_btn["cursor"] = "arrow"

    settings_btn["state"] = DISABLED
    settings_btn["bg"] = grey
    settings_btn["cursor"] = "arrow"

    #New window
    newWindow = Toplevel(root)
    newWindow.attributes('-topmost', True) 
    newWindow.resizable(0, 0)
    newWindow.iconbitmap("./res/rsi.ico")
    newWindow.title("Settings")
    newWindow.protocol("WM_DELETE_WINDOW", disable_event)
    newWindow.geometry("+"+str(positionX+int((windowWidth-settingsWidth)/2))+"+"+str(positionY+40))

    nw_canvas = Canvas(newWindow, height=settingsHeight, width=settingsWidth)
    nw_canvas.pack()
    nw_canvas.grid(rowspan=7, columnspan=2)

    #Selection label
    lang_label = Label(newWindow, text="Search language:")
    lang_label.grid(row=0, column=0, sticky=E)
    la_options = ["English", "Italiano"]
    la_clicked = StringVar()
    if language=="English":
        la_clicked.set(la_options[0])
    else:
        la_clicked.set(la_options[1])
    la_drop = OptionMenu(newWindow, la_clicked, *la_options)
    la_drop.grid(row=0, column=1)
    #browser
    browser_label = Label(newWindow, text="Browser:")
    browser_label.grid(row=1, column=0, sticky=E)
    # br_options = ["Chrome", "Edge", "Firefox"]
    br_options = ["Chrome", "Edge"]
    br_clicked = StringVar()
    if browser=="Chrome":
        br_clicked.set(br_options[0])
    elif browser=="Edge":
        br_clicked.set(br_options[1])
    else:
        br_clicked.set(br_options[2])
    br_drop = OptionMenu(newWindow, br_clicked, *br_options)
    br_drop.grid(row=1, column=1)
    #engine
    engine_label = Label(newWindow, text="Engine:")
    engine_label.grid(row=2, column=0, sticky=E)
    en_options = ["Bing", "Ecosia", "Google"]
    en_clicked = StringVar()
    if engine==bing:
        en_clicked.set(en_options[0])
    elif engine==ecosia:
        en_clicked.set(en_options[1])
    else:
        en_clicked.set(en_options[2])
    en_drop = OptionMenu(newWindow, en_clicked, *en_options)
    en_drop.grid(row=2, column=1)
    #n. of pc searches
    pcSearches_label = Label(newWindow, text="PC searches:")
    pcSearches_label.grid(row=4, column=0, sticky=E)
    ps_entry = Entry(newWindow, width=6, justify="center")
    ps_entry.insert(0, pcSearches)
    ps_entry.grid(row=4, column=1)
    #n. of mobile searches
    mobileSearches_label = Label(newWindow, text="Mobile searches:")
    mobileSearches_label.grid(row=5, column=0, sticky=E)
    ms_entry = Entry(newWindow, width=6, justify="center")
    ms_entry.insert(0, mobileSearches)
    ms_entry.grid(row=5, column=1)
    #mode
    mode_label = Label(newWindow, text="Search mode:")
    mode_label.grid(row=3, column=0, sticky=E)
    mo_options = ["PC + Mobile", "PC", "Mobile"]
    mo_clicked = StringVar()
    if pc & mobile:
        mo_clicked.set(mo_options[0])
    elif not mobile:
        mo_clicked.set(mo_options[1])
    else:
        mo_clicked.set(mo_options[2])
    mo_drop = OptionMenu(newWindow, mo_clicked, *mo_options)
    mo_drop.grid(row=3, column=1)
    #parent widget for the buttons
    buttonsFrame = Frame(newWindow)
    buttonsFrame.grid(row=6, column=0,rowspan=1, columnspan=2)
        #ok
    ok_text = StringVar()
    ok_btn = Button(buttonsFrame, textvariable=ok_text, height=1, width=10, command=lambda:ok(newWindow, la_clicked, br_clicked, en_clicked, mo_clicked, ps_entry, ms_entry), cursor="hand2")
    ok_text.set("Ok")
    ok_btn.grid(row=0, column=0)
        #cancel
    cancel_text = StringVar()
    cancel_btn = Button(buttonsFrame, textvariable=cancel_text, height=1, width=10, command=lambda:myDestroy(newWindow), cursor="hand2")
    cancel_text.set("Cancel")
    cancel_btn.grid(row=0, column=1)

def openLink(link):
    webbrowser.open_new_tab(link)
# FUNCTIONS END //////////////////////////////////////////////////////////////////////////////////////////////////


# INTERFACE BEGINNING
root = Tk()                         # beginning of the interface

root.title("RandomSearch")                  # window title
root.iconbitmap("./res/rsi.ico")            # window icon
root.attributes('-topmost', True)           # the window is always on top
root.resizable(0, 0)                        # the window is not resizable
root.geometry("+"+str(positionX)+"+"+str(positionY))

canvas = Canvas(root, width=windowWidth)    # needed for the layout
#canvas.pack()                              # canvas size depends on the size of the elements in it
canvas.grid(rowspan=5, columnspan=1)        # grid layout (5x1)

#(  1  )Logo
logo = Image.open("./res/rsl.png").resize([280,270])
logo = ImageTk.PhotoImage(logo)             # converts the Pillow Image into a Tkinter Image
logo_label = Label(image=logo)       
logo_label.image = logo
logo_label.grid(row=0, column=0, pady=(30,0))

#(  2  )Progress bar
style = ttk.Style()
style.theme_use('alt')
style.configure("cyan.Horizontal.TProgressbar", foreground="cyan", background="cyan")
progress = ttk.Progressbar(root, orient=HORIZONTAL, length=240, mode='determinate', style="cyan.Horizontal.TProgressbar")
progress.pack_forget()
progress.grid(row=2, column=0, pady=(0,20))

#(  3-4  )Parent widget for the buttons
btns_frame = Frame(root)
btns_frame.grid(row=3, column=0, columnspan=2, rowspan=2, pady=(0,40))

    #Start button
start_text = StringVar()
start_btn = Button(btns_frame, textvariable=start_text, font=("Raleway", "11","bold"), bg=pink, fg="white", height=2, width=12, command=lambda:search(), cursor="hand2")
start_text.set("Start")
start_btn.grid(row=0, column=0)

    #Stop button
stop_text = StringVar()
stop_btn = Button(btns_frame, textvariable=stop_text, font=("Raleway", "11","bold"), bg=grey, fg="white", height=2, width=12, command=lambda:stop(), state=DISABLED)
stop_text.set("Stop")
stop_btn.grid(row=0, column=1)

    #Settings button
settings_text = StringVar()
settings_btn = Button(btns_frame, textvariable=settings_text, font=("Raleway", "11","bold"), bg=azure, fg="white", height=2, width=12, command=lambda:settings(), cursor="hand2")
settings_text.set("Settings")
settings_btn.grid(row=1, column=0)

    #Quit button
quit_text = StringVar()
quit_btn = Button(btns_frame, textvariable=quit_text, font=("Raleway", "11","bold"), bg=blue, fg="white", height=2, width=12, command=root.quit, cursor="hand2")
quit_text.set("Quit")
quit_btn.grid(row=1, column=1)

#(  5  )Info
info_label = Label(root, text="Info: https://github.com/dimatteoluca", fg="grey", cursor="hand2")
info_label.bind("<Button-1>", lambda e: openLink("https://github.com/dimatteoluca"))
info_label.grid(row=5, column=0)

root.mainloop()                         
# INTERFACE END
