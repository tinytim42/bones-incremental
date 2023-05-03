#TODO: utils.actionFrame needs its own manager that can add buttons
#      and access resources, to manage gathering and purchasing

#TODO: actionFrame manager will also need the ability to swap between
#      different tabs, ungridding and regridding buttons as necessary

#TODO: code purchasing

#TODO: create flag manager

from tkinter import *
from managers import *
import utils
import constants as const

game = utils.Gui()

game.csm._activateCutscene('Introduction')

while game.running:
    game.root.update_idletasks()
    game._updateGui()
    game.root.update()



