from tkinter import *
from managers import *
import utils
import constants as const


def checkFlags(game, flags):
    if game.rsm.resources["Bones"].amount > 20 and flags[0]:
        game.csm._createCutscene()
        flags[0] = False

game = utils.Gui()

flags = [True]

while game.running:
    game.root.update_idletasks()
    checkFlags(game, flags)
    game.root.update()



