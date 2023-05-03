from tkinter import *
from managers import *
from objects import *
import constants as c
import events

class Gui:
    def __init__(self):
        self.root = Tk()
        self.rsm = ResourceManager(self.root)
        self.csm = CutsceneManager(self.root)
        for event in events.csEvents:
            self.csm._createCutscene(event)
        self.lm = LogManager(self.root)
        #self.afm = ActionManager(self.root, self.rsm)
        self.root.title("Bones Incremental")
        self.root.configure(background="black")
        self.root.minsize(c.SCREEN_SIZE[0], c.SCREEN_SIZE[1])

        self.root.protocol("WM_DELETE_WINDOW", self._exitGame)
        #checks if anywhere onscreen is clicked, to exit cutscenes
        self.root.bind("<Button-1>", lambda e:self.csm._endCutscene())

        headerFrame = Frame(self.root, width=900, height=30, bg=c.BGC)
        headerFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        headerFrame.grid_propagate(0)

        self._addHeaderItem(headerFrame, "Save", self._saveGame)
        self._addHeaderItem(headerFrame, "Exit", self._exitGame)

        self.headerFrame = headerFrame

        actionFrame = Frame(self.root, width=400, height=600, bg=c.BGC)
        actionFrame.grid(row=1, column=1, padx=5, pady=5)
        actionFrame.grid_propagate(0)
        actionFrame.grid_columnconfigure(0, weight=1)
        actionFrame.grid_columnconfigure(1, weight=1)

        actionHeader = Frame(actionFrame, bg=c.BGC, width=400, height=40)
        actionHeader.grid(row=0,column=0,columnspan=2)
        actionHeader.grid_propagate(0)

        self._addHeaderItem(actionHeader, "Graveyard")
        self._addHeaderItem(actionHeader, "Town")
    
        self.actionFrame = actionFrame
        self.actionHeader = actionHeader

        #may need an "_addButton" method for rsm
        bonesBtn = Btn(self.actionFrame, text="Dig for bones.",
                       tttext="The damp earth contains\na grisly reward.")
        bonesBtn.bind("<Button-1>", 
                      lambda e:self.rsm._gather("Bones"))
        bonesBtn.grid(row=1, column=0, padx=10, pady=5)

        turnipBtn = BuyBtn(self.actionFrame)
        turnipBtn.grid(row=1, column=1, padx=10, pady=5)
        turnipBtn.bind("<Button-1>", lambda e:turnipBtn._buy(self.rsm))

        self.running = True

    def _saveGame(self):
        if not self.csm.active:
            print("saved")

    def _exitGame(self):   
        self.root.destroy()
        self.running = False

    def _addHeaderItem(self, frame, text="Blank", action=lambda: None):
        if frame.grid_size()[0] > 0:
            divider = Label(frame, text="|", bg=c.BGC, fg=c.FGC,
                            font=c.font)
            divider.grid(row=0,column=frame.grid_size()[0])

        headerBtn = HeaderBtn(frame, text=text, action=lambda e:action())
        headerBtn.grid(row=0, column=frame.grid_size()[0])
    
    def _updateGui(self):
        #btns = self.afm.activeTab.children
        btns = self.actionFrame.winfo_children()
        for b in btns:
            if b.__class__.__name__ == "BuyBtn":
                b._setBuyable(self.rsm)




if __name__ == "__main__":
    game = Gui()
    btn = Btn(game.root)
    buyBtn = BuyBtn(game.root)