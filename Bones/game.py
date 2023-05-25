#TODO: code upgrades that change multiplier for resource gathering
#TODO: allow flags to unlock new tabs/resources/buttons
#TODO: create flag manager

from tkinter import *
from managers import *
import utils
import constants as const

game = utils.Gui()

while game.running:
    game.root.update_idletasks()
    game._updateGui()
    game.root.update()



