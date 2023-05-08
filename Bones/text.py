#Manages event triggers, cutscene text, and unlocks
from tkinter import *

csEvents = {}
csEvents["Introduction"] = ["The Beginning",
"""You awaken in a graveyard in the dead of \
night. There is dirt under your fingernails already, and a \
dull, rusted shovel lies near your outstretched hand. You \
know what you must do."""]

csEvents["Shovel Upgrade"] = ["Tools of the Trade", 
"""Your hands ache from exertion. The \
coarse wood of the shovel and its blunted point make this \
arduous labor slow and painful. Surely there is someone in town who might supply superior  \
tools, better suited to your task."""]

tooltips = {}



