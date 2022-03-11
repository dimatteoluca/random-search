import json

config = {"pcSpeed":"Fast", "timeMultiplier":"1.5", "language":"English", "browser":"Chrome", "engine":"https://www.google.com/search?q=", "pc":"True", "mobile":"True","pcSearchesNumber":"5", "mobileSearchesNumber":"5"}

with open('config.json','w') as f:
    json.dump(config, f)