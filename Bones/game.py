from tkinter import *
from managers import *
import utils
import constants as const

def checkFlags():
    global bones, cs, flags
    if bones.amount >= 20 and flags[0]:
        cs = Cutscene("Unholy Treasure",
                      """You discover amongst the roots and
splinters of decaying caskets a tarnished necklace, bearing
the insignia of a gibbous moon. A faint light seems to shine
through the grime and verdigris.""")
        flags[0] = False

def killCutscene():
    cs.destroy()
    global cutscene
    cutscene = False

def onExit():
    global running, root
    running = False
    root.destroy()

root = Tk()

#checks if anywhere onscreen is clicked, to exit cutscenes
root.protocol("WM_DELETE_WINDOW", onExit)

bones = Resource("Bones")


headerFrame = Frame(root, width=900, height=30, bg=const.BGC)
headerFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
headerFrame.grid_propagate(0)

utils.addHeaderItem(headerFrame, "Save", utils.saveGame)
util.saddHeaderItem(headerFrame, "Exit", utils.exitGame)
                     
resourceFrame = Frame(root, width=200, height=600, bg=const.BGC)
resourceFrame.grid(row=1, column=0, padx=5, pady=5)
resourceFrame.grid_propagate(0)

resourceTitle = Label(resourceFrame, text="Resources",
                      bg=const.BGC, fg=const.FGC, font=titleFont)
resourceTitle.grid(sticky='w', row=0, column=0, padx=5, pady=5)

bonesAmt = Label(resourceFrame, text=("Bones: " + str(bones._get_amount())),
                 bg=const.BGC, fg=const.FGC, font=font)
bonesAmt.grid(sticky='w', row=1, column=0, padx=5, pady=5)

actionFrame = Frame(root, width=400, height=600, bg=const.BGC)
actionFrame.grid(row=1, column=1, padx=5, pady=5)
actionFrame.grid_propagate(0)
actionFrame.grid_columnconfigure(0, weight=1)
actionFrame.grid_columnconfigure(1, weight=1)

actionHeader = Frame(actionFrame, bg=const.BGC, width=400, height=40)
actionHeader.grid(row=0,column=0,columnspan=2)
actionHeader.grid_propagate(0)
addHeaderItem(actionHeader, "Graveyard")
addHeaderItem(actionHeader, "Town")

bonesButton = Button(actionFrame, text="Dig for bones.",
                     width=15, bg="grey", font=font)
bonesButton.tooltip = "The damp earth contains\na grisly reward."
buttonHoverConfig(bonesButton)
bonesButton.bind("<Button-1>",
                 lambda event,
                 resource=bones,
                 label=bonesAmt:addResource(resource,label))
bonesButton.grid(row=1, column=0, padx=10, pady=5)


logFrame = Frame(root, width=300, height=600, bg=const.BGC)
logFrame.grid(row=1, column=2, padx=5, pady=5)
logFrame.grid_propagate(0)

logTitle = Label(logFrame, text="Log", bg=const.BGC,
                 fg=const.FGC, font=titleFont, justify=LEFT)
logTitle.grid(sticky='w', row=0, column=0, padx=5, pady=5)

logItem = Label(logFrame, text="You are alone in an\novergrown graveyard.",
                bg=const.BGC, fg=const.FGC, font=font, justify=LEFT)
logItem.grid(row=1, column=0, padx=5, pady=5)

running = True

flags = [True]
cs = utils.Cutscene()
cutscene = True

while running:
    root.update_idletasks()
    checkFlags()
    root.update()



