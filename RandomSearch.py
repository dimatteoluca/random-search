import webbrowser, time, threading, ctypes, utils, json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


# VERSION NUMBER
versionNumber = "1.2.0"

# BROWSERS 
webbrowser.register("Chrome", None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
webbrowser.register("Edge", None, webbrowser.BackgroundBrowser("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))
webbrowser.register("Firefox", None, webbrowser.BackgroundBrowser("C:\Program Files\Mozilla Firefox\Firefox.exe"))
webbrowser.register("Opera", None, webbrowser.BackgroundBrowser("C:\Program Files\Opera\launcher.exe"))

# ENGINES
bing =      "https://www.bing.com/search?q="
duckgo =    "https://duckduckgo.com/?q="
ecosia =    "https://www.ecosia.org/search?q="
google =    "https://www.google.com/search?q="
yahoo =     "https://search.yahoo.com/search?q="

# COLORS
cyan =      "#0ee0ed"
azure =     "#0ca3ea"
blue =      "#0f388e"
pink =      "#d372a9" #bd74ad
purple =    "#7c6bac"
grey =      "#e0e0e0"

# INITIAL STATE
with open('config.json','r') as f:
    config = json.load(f)

pcSpeed =               str(config["pcSpeed"])
timeMultiplier =        float(config["timeMultiplier"])
language =              str(config["language"])
browser =               str(config["browser"])
engine =                str(config["engine"])
if str(config["pc"])=="True":
    pc = True
elif str(config["pc"])=="False":
    pc = False
if str(config["mobile"])=="True":
    mobile = True
elif str(config["mobile"])=="False":
    mobile = False
pcSearchesNumber =      int(config["pcSearchesNumber"])
mobileSearchesNumber =  int(config["mobileSearchesNumber"])
tabs =                  0
halt =                  False

# POSITIONS & SIZES
user32 = ctypes.windll.user32
screenWidth = user32.GetSystemMetrics(0)
screenHeight = user32.GetSystemMetrics(1)
positionX = int((screenWidth/4)*3)
positionY = int((screenHeight/5)*2)
windowWidth = 380
#windowHeight = auto
settingsWindowWidth = 280
settingsWindowHeight = 350
optionMenusWidth = 12


# FUNCTIONS BEGINNING //////////////////////////////////////////////////////////////////////////////////////////////////
def search():

    global halt

    buttonsReset2()    
    halt = False

    thread = threading.Thread(target=realSearch, daemon=True)
    thread.start()

def realSearch():

    global tabs

    wordsList = utils.getWordsList(language)
    valuePerSearch = utils.getProgressBarValuePerSearch(pc, mobile, pcSearchesNumber, mobileSearchesNumber)
    progressBar['value'] = 0

    webbrowser.get(browser).open_new_tab("https://www.example.org/")
    tabs += 1

    if pc:
        ret = doSearches(wordsList, "pc", pcSearchesNumber, valuePerSearch)
    if mobile:
        ret = doSearches(wordsList, "mobile", mobileSearchesNumber, valuePerSearch)

    if (ret=="halt"):
        utils.closeTabs(browser, tabs, timeMultiplier)
    if (ret=="go"):
        for tab in range(tabs):
            utils.closeTab(timeMultiplier)

    tabs = 0
    buttonsReset1()

def doSearches(wordsList, searchesType, searchesNumber, valuePerSearch):
    
    if (searchesType == "mobile"):
        utils.setBrowsersDevInterface(browser, timeMultiplier)

    for search in range(searchesNumber):

        if (singleSearch(wordsList) == "halt"):
            progressBar['value'] = 100
            return "halt"
        progressBar['value'] += valuePerSearch

    time.sleep(2*timeMultiplier)
    return "go"

def singleSearch(wordsList):
    
    if halt:
        return "halt"
    rw = utils.randomWordsURLandSleepTime(engine, wordsList)
    url = rw[0]
    sleepTime = rw[1]
    utils.doSearch(url, sleepTime, timeMultiplier)

def stop():

    global halt

    utils.disableButton(stop_btn)
    halt = True

def settings():

    # Buttons reset
    utils.disableButton(start_btn)
    utils.disableButton(settings_btn)

    # New window
    settingsWindow = Toplevel(root)
    settingsWindow.geometry("+"+str(positionX+int((windowWidth-settingsWindowWidth)/2))+"+"+str(positionY+40))
    settingsWindow.title("Settings")
    settingsWindow.iconbitmap("./res/rsi.ico")
    settingsWindow.attributes('-topmost', True) 
    settingsWindow.resizable(0, 0)
    settingsWindow.protocol("WM_DELETE_WINDOW", utils.disableEvent)

    sw_canvas = Canvas(settingsWindow, height=settingsWindowHeight, width=settingsWindowWidth)
    #sw_canvas.pack()
    sw_canvas.grid(rowspan=8, columnspan=2)

    getConfig()

    #(  1  ) PC speed
    speed_label = Label(settingsWindow, text="PC speed:")
    speed_label.grid(row=0, column=0, sticky=E)
    sp_options = ["Very Fast", "Fast", "Slow", "Very Slow"]
    sp_clicked = StringVar()
    if pcSpeed=="Very Fast":
        sp_clicked.set(sp_options[0])
    elif pcSpeed=="Fast":
        sp_clicked.set(sp_options[1])
    elif pcSpeed=="Slow":
        sp_clicked.set(sp_options[2])
    elif pcSpeed=="Very Slow":
        sp_clicked.set(sp_options[3])
    sp_drop = OptionMenu(settingsWindow, sp_clicked, *sp_options)
    sp_drop.config(width=optionMenusWidth)
    sp_drop.grid(row=0, column=1)

    #(  2  ) Language
    lang_label = Label(settingsWindow, text="Search language:")
    lang_label.grid(row=1, column=0, sticky=E)
    la_options = ["English", "Italiano"]
    la_clicked = StringVar()
    if language=="English":
        la_clicked.set(la_options[0])
    elif language=="Italiano":
        la_clicked.set(la_options[1])
    la_drop = OptionMenu(settingsWindow, la_clicked, *la_options)
    la_drop.config(width=optionMenusWidth)
    la_drop.grid(row=1, column=1)

    #(  3  ) Browser
    browser_label = Label(settingsWindow, text="Browser:")
    browser_label.grid(row=2, column=0, sticky=E)
    br_options = ["Chrome", "Edge", "Firefox", "Opera"]
    br_clicked = StringVar()
    if browser=="Chrome":
        br_clicked.set(br_options[0])
    elif browser=="Edge":
        br_clicked.set(br_options[1])
    elif browser=="Firefox":
        br_clicked.set(br_options[2])
    elif browser=="Opera":
        br_clicked.set(br_options[3])
    br_drop = OptionMenu(settingsWindow, br_clicked, *br_options)
    br_drop.config(width=optionMenusWidth)
    br_drop.grid(row=2, column=1)

    #(  4  ) Engine
    engine_label = Label(settingsWindow, text="Engine:")
    engine_label.grid(row=3, column=0, sticky=E)
    en_options = ["Bing", "DuckDuckGo", "Ecosia", "Google", "Yahoo"]
    en_clicked = StringVar()
    if engine==bing:
        en_clicked.set(en_options[0])
    elif engine==duckgo:
        en_clicked.set(en_options[1])
    elif engine==ecosia:
        en_clicked.set(en_options[2])
    elif engine==google:
        en_clicked.set(en_options[3])
    elif engine==yahoo:
        en_clicked.set(en_options[4])
    en_drop = OptionMenu(settingsWindow, en_clicked, *en_options)
    en_drop.config(width=optionMenusWidth)
    en_drop.grid(row=3, column=1)

    #(  5  ) Mode
    mode_label = Label(settingsWindow, text="Search mode:")
    mode_label.grid(row=4, column=0, sticky=E)
    mo_options = ["PC + Mobile", "PC", "Mobile"]
    mo_clicked = StringVar()
    if pc & mobile:
        mo_clicked.set(mo_options[0])
    elif not mobile:
        mo_clicked.set(mo_options[1])
    elif not pc:
        mo_clicked.set(mo_options[2])
    mo_drop = OptionMenu(settingsWindow, mo_clicked, *mo_options)
    mo_drop.config(width=optionMenusWidth)
    mo_drop.grid(row=4, column=1)

    #(  6  ) N. of pc searches
    pcSearchesNumber_label = Label(settingsWindow, text="PC searches:")
    pcSearchesNumber_label.grid(row=5, column=0, sticky=E)
    ps_entry = Entry(settingsWindow, width=6, justify="center")
    ps_entry.insert(0, pcSearchesNumber)
    ps_entry.grid(row=5, column=1)

    #(  7  ) N. of mobile searches
    mobileSearchesNumber_label = Label(settingsWindow, text="Mobile searches:")
    mobileSearchesNumber_label.grid(row=6, column=0, sticky=E)
    ms_entry = Entry(settingsWindow, width=6, justify="center")
    ms_entry.insert(0, mobileSearchesNumber)
    ms_entry.grid(row=6, column=1)

    #(  8  ) Buttons
    buttonsFrame = Frame(settingsWindow)
    buttonsFrame.grid(row=7, column=0,rowspan=1, columnspan=2)
        #ok
    ok_text = StringVar()
    ok_btn = Button(buttonsFrame, textvariable=ok_text, height=1, width=10, command=lambda:ok(settingsWindow, sp_clicked, la_clicked, br_clicked, en_clicked, mo_clicked, ps_entry, ms_entry), cursor="hand2")
    ok_text.set("Ok")
    ok_btn.grid(row=0, column=0)
        #cancel
    cancel_text = StringVar()
    cancel_btn = Button(buttonsFrame, textvariable=cancel_text, height=1, width=10, command=lambda:myDestroy(settingsWindow), cursor="hand2")
    cancel_text.set("Cancel")
    cancel_btn.grid(row=0, column=1)

def myDestroy(settingsWindow):

    settingsWindow.destroy()
    buttonsReset3()

def ok(settingsWindow, sp_clicked, la_clicked, br_clicked, en_clicked, mo_clicked, ps_entry, ms_entry):

    global pcSpeed
    global timeMultiplier
    global language
    global browser
    global engine
    global pc
    global mobile
    global pcSearchesNumber
    global mobileSearchesNumber

    if (sp_clicked.get() == "Very Fast"):
        pcSpeed = "Very Fast"
        timeMultiplier = 1.0
    elif (sp_clicked.get() == "Fast"):
        pcSpeed = "Fast"
        timeMultiplier = 1.5
    elif (sp_clicked.get() == "Slow"):
        pcSpeed = "Slow"
        timeMultiplier = 2.0
    elif (sp_clicked.get() == "Very Slow"):
        pcSpeed = "Very Slow"
        timeMultiplier = 3.0

    language = la_clicked.get()

    browser = br_clicked.get()

    if (en_clicked.get() == "Bing"):
        engine = bing
    elif (en_clicked.get() == "DuckDuckGo"):
        engine = duckgo
    elif (en_clicked.get() == "Ecosia"):
        engine = ecosia
    elif (en_clicked.get() == "Google"):
        engine = google
    elif (en_clicked.get() == "Yahoo"):
        engine = yahoo

    if (mo_clicked.get() == "PC + Mobile"):
        pc = True
        mobile = True
    elif (mo_clicked.get() == "PC"):
        pc = True
        mobile = False
    elif (mo_clicked.get() == "Mobile"):
        pc = False
        mobile = True
        
    try:
        m = int(ps_entry.get())
        n = int(ms_entry.get())
    except ValueError:
        messagebox.showerror(title="Warning", message="Insert a positive integer.")
        m = 0
        n = 0
    if ((ps_entry != "") and (m > 0)):
        pcSearchesNumber = m
    if ((ms_entry != "") and (n > 0)):
        mobileSearchesNumber = n

    
    setConfig()
    settingsWindow.destroy()
    buttonsReset3()

def getConfig():

    global pcSpeed
    global timeMultiplier
    global language
    global browser
    global engine
    global pc
    global mobile
    global pcSearchesNumber
    global mobileSearchesNumber

    with open('config.json','r') as f:
        config = json.load(f)

    pcSpeed =               str(config["pcSpeed"])
    timeMultiplier =        float(config["timeMultiplier"])
    language =              str(config["language"])
    browser =               str(config["browser"])
    engine =                str(config["engine"])
    if str(config["pc"])=="True":
        pc = True
    elif str(config["pc"])=="False":
        pc = False
    if str(config["mobile"])=="True":
        pc = True
    elif str(config["mobile"])=="False":
        pc = False
    pcSearchesNumber =      int(config["pcSearchesNumber"])
    mobileSearchesNumber =  int(config["mobileSearchesNumber"])

def setConfig():

    config = {"pcSpeed":str(pcSpeed), "timeMultiplier":str(timeMultiplier), "language":str(language), "browser":str(browser), "engine":str(engine), "pc":str(pc), "mobile":str(mobile),"pcSearchesNumber":str(pcSearchesNumber), "mobileSearchesNumber":str(mobileSearchesNumber)}

    with open('config.json','w') as f:
        json.dump(config, f)

def buttonsReset1():

    utils.enableButton(start_btn, pink)
    utils.disableButton(stop_btn)
    utils.enableButton(settings_btn, azure)

def buttonsReset2():

    utils.disableButton(start_btn)
    utils.enableButton(stop_btn, purple)
    utils.disableButton(settings_btn)

def buttonsReset3():

    utils.enableButton(start_btn, pink)
    utils.enableButton(settings_btn, azure)
# FUNCTIONS END


# INTERFACE BEGINNING //////////////////////////////////////////////////////////////////////////////////////////////////
root = Tk()

root.geometry("+"+str(positionX)+"+"+str(positionY))
root.title("RandomSearch")                  # window title
root.iconbitmap("./res/rsi.ico")            # window icon
root.attributes('-topmost', True)           # the window is always on top
root.resizable(0, 0)                        # the window is not resizable

canvas = Canvas(root, width=windowWidth)    # needed for the layout
canvas.grid(rowspan=5, columnspan=1)        # grid layout (5x1)

#(  1  ) Logo
logo = Image.open("./res/rsl.png").resize([280,270])
logo = ImageTk.PhotoImage(logo)             # converts the Pillow Image into a Tkinter Image
logo_label = Label(image=logo)       
logo_label.image = logo
logo_label.grid(row=0, column=0, pady=(30,0))

#(  2  ) Progress bar
style = ttk.Style()
style.theme_use('alt')
style.configure("cyan.Horizontal.TProgressbar", foreground="cyan", background="cyan")
progressBar = ttk.Progressbar(root, orient=HORIZONTAL, length=240, mode='determinate', style="cyan.Horizontal.TProgressbar")
progressBar.pack_forget()
progressBar.grid(row=2, column=0, pady=(0,20))

#(  3-4  ) Buttons
btns_frame = Frame(root)
btns_frame.grid(row=3, column=0, columnspan=2, rowspan=2, pady=(0,40))
    # Start
start_text = StringVar()
start_btn = Button(btns_frame, textvariable=start_text, font=("Raleway", "11","bold"), bg=pink, fg="white", height=2, width=12, command=lambda:search(), cursor="hand2")
start_text.set("Start")
start_btn.grid(row=0, column=0)
    # Stop
stop_text = StringVar()
stop_btn = Button(btns_frame, textvariable=stop_text, font=("Raleway", "11","bold"), bg=grey, fg="white", height=2, width=12, command=lambda:stop(), state=DISABLED)
stop_text.set("Stop")
stop_btn.grid(row=0, column=1)
    # Settings
settings_text = StringVar()
settings_btn = Button(btns_frame, textvariable=settings_text, font=("Raleway", "11","bold"), bg=azure, fg="white", height=2, width=12, command=lambda:settings(), cursor="hand2")
settings_text.set("Settings")
settings_btn.grid(row=1, column=0)
    # Quit
quit_text = StringVar()
quit_btn = Button(btns_frame, textvariable=quit_text, font=("Raleway", "11","bold"), bg=blue, fg="white", height=2, width=12, command=root.quit, cursor="hand2")
quit_text.set("Quit")
quit_btn.grid(row=1, column=1)

#(  5  ) Info
info_label = Label(root, text="RandomSearch v"+versionNumber+"\nInfo: https://github.com/dimatteoluca/random-search", fg="grey", cursor="hand2")
info_label.bind("<Button-1>", lambda e: utils.openLink("https://github.com/dimatteoluca/random-search"))
info_label.grid(row=5, column=0)

root.mainloop()                         
# INTERFACE END
