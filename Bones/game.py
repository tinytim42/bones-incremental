from tkinter import *
from managers import *
import utils
import constants as const


def checkFlags():
    pass
    '''global rsm, cs, flags
    if rsm.resources["Bones"].amount >= 20 and flags[0]:
        cs = Cutscene("Unholy Treasure",
                      """You discover amongst the roots and
splinters of decaying caskets a tarnished necklace, bearing
the insignia of a gibbous moon. A faint light seems to shine
through the grime and verdigris.""")
        flags[0] = False'''

game = utils.Gui()

flags = [True]

while game.running:
    game.root.update_idletasks()
    checkFlags()
    game.root.update()



