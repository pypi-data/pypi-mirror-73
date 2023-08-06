#Imports
import inkster
import random
import asyncio
from inkster import educational
from inkster import easy
#Random
Cresponse = ["Abxy > Hello there!", 'Abxy > Sure!', "Abxy > Uhh...no", "Abxy > Sure", "Inkster > Looks like you actually got to see me. Its me Inkster!", "Abxy > ...", "Abxy > Meh."]
#Inputs
chat = input("[SYSTEM] Welcome to the Chat interpreter in Abxy!(A third party library for inkster)\nPress any key to start!")

class ChatPreter:

    while True:
        ok = chat
        if chat == True:
            print("[SYSTEM] Starting..STARTED!")
        chatting = input("ChatPreter > ")
        print(random.choice(Cresponse))
