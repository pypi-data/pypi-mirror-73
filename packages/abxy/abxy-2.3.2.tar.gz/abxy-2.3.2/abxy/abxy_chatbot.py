# Description : Abxy the chatbot.

#Imports
from nltk.chat.util import Chat, reflections

pairs = [
    ['My name is (.*)', ['Abxy > Hello there %1!']],
    ['(hi|hello|hey|holla|heyo|hola|heya|hoi)', ['Abxy > Hello there!', 'Abxy > Hi there!', 'Abxy > Hai!']],
    ['(.*) in (.*) is fun', ['Abxy > %1 in %2 sounds fun! :D']],
    ['(.*)(location|city) ?', ['Abxy > Abxy, Paruko Town']],
    ['(.*) created you ?', ['Abxy > AbxyPlayz created me in Python Programming Language.']],
    ['How is the weather in (.*) ?', ['Abxy > The weather in %1 Its amazing like always! :D']],
    ['(.*)help(.*)', ['Abxy > What do you need help with?']],
    ['(.*) your name?', ['Abxy > My name is Abxy!']],
    ['(.*) fuck you', ['Abxy > That is indeed rude..']],
    ['Abxy', ['Abxy > ?']],
    ['What is abxy?', ['Abxy > Abxy is a third party library for the package named inkster(https://pypi.org/project/inkster/).\nAbxy is a chatbot package with random interpreters such as ChatPreter the chatbot interpreter.']]
]

Abxy_Reflections = {
    'Hello': 'Abxy > Hello There.',
    'Go' : 'Abxy > Gone'
}

print('[SYSTEM] Welcome to the Abxy Chatbot in Abxy!(A third party library for inkster)\nAsk Abxy anything she is able to answer! :D')
chat = Chat(pairs, Abxy_Reflections)
chat.converse(())