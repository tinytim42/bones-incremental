from tkinter import *
from managers import *
from objects import *
import constants as c
import text

class Gui:
    def __init__(self):
        self.root = Tk()
        self.rsm = ResourceManager(self.root)
        self.csm = CutsceneManager(self.root)
        for key in text.csEvents.keys():
            self.csm._createCutscene(key, text.csEvents[key])
        self.lm = LogManager(self.root)
        self.ugm = UpgradeManager(self.root, self.rsm)
        self.afm = ActionManager(self.root, self.rsm, self.ugm)
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
        btns = self.afm.activeTab.frame.winfo_children()
        #btns = self.actionFrame.winfo_children()
        for b in btns:
            if b.__class__.__name__ == "BuyBtn":
                b._setBuyable()

if __name__ == "__main__":
    game = Gui()
    btn = Btn(game.root)
    buyBtn = BuyBtn(game.root)