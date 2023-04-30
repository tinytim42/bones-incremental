from tkinter import *
from managers import *
import constants as c

class Gui:
    def __init__(self):
        self.root = Tk()
        self.rsm = ResourceManager(self.root)
        self.csm = CutsceneManager(self.root)
        self.lm = LogManager(self.root)
        self.root.title("Bones Incremental")
        self.root.configure(background="black")
        self.root.minsize(c.SCREEN_SIZE[0], c.SCREEN_SIZE[1])

        self.root.protocol("WM_DELETE_WINDOW", self.exitGame)
        #checks if anywhere onscreen is clicked, to exit cutscenes
        self.root.bind("<Button-1>", lambda e:self.csm._endCutscene())

        headerFrame = Frame(self.root, width=900, height=30, bg=c.BGC)
        headerFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        headerFrame.grid_propagate(0)

        self.addHeaderItem(headerFrame, "Save", self.saveGame)
        self.addHeaderItem(headerFrame, "Exit", self.exitGame)

        self.headerFrame = headerFrame

        actionFrame = Frame(self.root, width=400, height=600, bg=c.BGC)
        actionFrame.grid(row=1, column=1, padx=5, pady=5)
        actionFrame.grid_propagate(0)
        actionFrame.grid_columnconfigure(0, weight=1)
        actionFrame.grid_columnconfigure(1, weight=1)

        actionHeader = Frame(actionFrame, bg=c.BGC, width=400, height=40)
        actionHeader.grid(row=0,column=0,columnspan=2)
        actionHeader.grid_propagate(0)

        self.addHeaderItem(actionHeader, "Graveyard")
        self.addHeaderItem(actionHeader, "Town")
    
        self.actionFrame = actionFrame
        self.actionHeader = actionHeader

        bonesBtn = Btn(self.actionFrame, text="Dig for bones.",
                       tttext="The damp earth contains\na grisly reward.")
        bonesBtn.bind("<Button-1>", 
                      lambda e:self.rsm._gather("Bones"))
        bonesBtn.grid(row=1, column=0, padx=10, pady=5)

        self.running = True

        #starts opening cutscene
        self.csm._createCutscene()
        self.csm.active = self.csm.cutscenes[0]

    def saveGame(self):
        if not self.csm.active:
            print("saved")

    def exitGame(self):   
        self.root.destroy()
        self.running = False

    def addHeaderItem(self, frame, text="Blank", action=lambda: None):
        if frame.grid_size()[0] > 0:
            divider = Label(frame, text="|", bg=c.BGC, fg=c.FGC,
                            font=c.font)
            divider.grid(row=0,column=frame.grid_size()[0])

        headerBtn = HeaderBtn(frame, text=text, action=lambda e:action())
        headerBtn.grid(row=0, column=frame.grid_size()[0])

class Btn(Button):
    def __init__(self, parent, text="It's a button!", 
                 tttext = "Tooltip yay", **kwargs):
        self.text = text
        self.root = parent.winfo_toplevel()
        #interactable (deactivated for cutscenes)
        self.active = True
        #if it costs something, lights up when enough resources are available
        self.affordable = True
        #if it's a building/upgrade, purchased deactivates clicking
        #but leaves tooltip mouseover available for QOL
        self.purchased = False
        #tooltip helpers
        self.tttext = tttext
        self.ttActive = False
        self.tooltip = LabelFrame(self.root, width=500, height=60, bg=c.BGC)

        self.label = Label(self.tooltip, text=self.tttext, bg=c.BGC,
                             fg=c.FGC, font=c.font)
        self.label.grid(row=0,column=0,padx=10,pady=5)
        #gets absolute position below button
        super().__init__(parent, text=text, 
                         width=15, bg="grey", 
                         font=c.font, **kwargs)
        
        self.xpos = 0
        self.ypos = 0

        self.bind("<Enter>", lambda e:self._Enter())
        self.bind("<Leave>", lambda e:self._Leave())
    
    def _Enter(self):
        if self.active:
            self.config(bg=c.FGC)
        else:
            self.config(bg=c.INACTIVE_COLOR)
        if not self.ttActive:
            self._activateTooltip()
    
    def _Leave(self):
        if self.active:
            self.config(bg="grey")
        else:
            self.config(bg=c.INACTIVE_COLOR)
        if self.ttActive:
            self._deactivateTooltip()
    
    def _setMethod(self, action):
        self.bind("<Button-1>", action)

    def _activateTooltip(self):
        if self.xpos == 0 and self.ypos == 0:
            self.xpos = (self.master.winfo_x() + self.winfo_x())
            self.ypos = (self.master.winfo_y() +
                         self.winfo_y() +
                         self.winfo_height() + 10)
        self.tooltip.place(x=self.xpos, y=self.ypos)
        self.ttActive = True
    
    def _deactivateTooltip(self):
        self.tooltip.place_forget()
        self.ttActive = False

class HeaderBtn(Button):
    def __init__(self, parent, text="Test", action=lambda: None, **kwargs):

        super().__init__(parent, text=text, bg=c.BGC, fg=c.FGC, 
                         relief=FLAT, font=c.font, activebackground=c.BGC, 
                         activeforeground="white", bd=0, **kwargs)

        self.bind("<Enter>", 
                  func=lambda e: self.config(fg="skyblue"))
        self.bind("<Leave>",
                  func=lambda e: self.config(fg=c.FGC))
        self.bind("<Button-1>", action)







if __name__ == "__main__":
    game = Gui()
    btn = Btn(game.root)