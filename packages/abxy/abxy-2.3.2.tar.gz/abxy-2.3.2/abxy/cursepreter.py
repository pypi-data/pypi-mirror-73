#Imports
import inkster
import random
import asyncio
from inkster import educational
from inkster import easy
#Random
CUresponse = ["Abxy > FUCK YOU!", 'Abxy > Bitch shut up.', "Abxy > Aww your such a dick.", "Abxy > Motherfucker.", "Inkster > YOU FOUND ME FUCKERS! HAHA", "Abxy > Fuck off.", "Abxy > Ever thought of fucking yourself?"]
#Inputs
curse = input("[SYSTEM] Welcome to the Curse interpreter in Abxy!(A third party library for inkster)\nPress any key to start!")

class CursePreter:

    while True:
        ok = curse
        if curse == True:
            print("[SYSTEM] Starting..STARTED!")
        cursing = input("CursePreter > ")
        print(random.choice(CUresponse))
