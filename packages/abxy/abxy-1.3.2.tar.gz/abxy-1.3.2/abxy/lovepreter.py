#Imports
import inkster
import random
import asyncio
from inkster import educational
from inkster import easy
#Random
Lresponse = ["Abxy > Awww I love you to! :D", 'Abxy > Stop kissing me LOL', "Abxy > *blushes*", "Abxy > Hehe..uhh love you bye!", "Inkster > Oh! Hehe...well you be my valentine? I mean you don't have to..since you found me..", "Abxy > I think I just found my crush...", "Abxy > *makes heart with hands*"]
#Inputs
love = input("[SYSTEM] Welcome to the Love interpreter in Abxy!(A third party library for inkster)\nPress any key to start!")

class LovePreter:

    while True:
        msms = love
        if love == True:
            print("[SYSTEM] Starting..STARTED!")
        loving = input("LovePreter > ")
        print(random.choice(Lresponse))
