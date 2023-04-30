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

        bonesBtn = btn(self.actionFrame, text="Dig for bones.",
                            width=15, bg="grey", font=c.font)
        bonesBtn.tooltip = "The damp earth contains\na grisly reward."
        self.btnHoverConfig(bonesBtn)
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

    # function to change properties of button on hover
    def changeFgOnHover(self, btn, colorOnHover, colorOnLeave):
    
        # adjusting background of the widget
        # background on entering widget
        btn.bind("<Enter>",
                    func=lambda e: btn.config(fg=colorOnHover))
    
        # background color on leving widget
        btn.bind("<Leave>",
                    func=lambda e: btn.config(fg=colorOnLeave))

    def addHeaderItem(self, frame, text="Blank", action=lambda: None):
        if frame.grid_size()[0] > 0:
            divider = Label(frame, text="|", bg=c.BGC, fg=c.FGC,
                            font=c.font)
            divider.grid(row=0,column=frame.grid_size()[0])

        headerBtn = btn(frame, text=text, bg=c.BGC, fg=c.FGC,
                relief=FLAT, font=c.font, activebackground=c.BGC,
                activeforeground="white", bd=0)
        headerBtn.grid(row=0, column=frame.grid_size()[0])
        headerBtn.bind("<Button-1>", lambda e:action())
        self.changeFgOnHover(headerBtn, "skyblue", c.FGC)

    def createTooltip(self, btn):
        #gets absolute position based on root window
        xpos = (btn.master.winfo_x() + btn.winfo_x())
        ypos = (btn.master.winfo_y() +
                btn.winfo_y() +
                btn.winfo_height() + 10)
        tt = LabelFrame(self.root, width=500, height=60, bg=c.BGC)
        ttext = Label(tt, text=btn.tooltip, bg=c.BGC,
                    fg=c.FGC, font=c.font)
        ttext.grid(row=0,column=0,padx=10,pady=5)
        tt.place(x=xpos, y=ypos)
        btn.tt = tt

    def destroyTooltip(self, btn):
        btn.tt.destroy()

    def btnEnter(self, btn):
        if not self.csm.active:
            self.createTooltip(btn)
            btn.config(bg=c.FGC)

    def btnLeave(self, btn):
        if not self.csm.active:
            self.destroyTooltip(btn)
            btn.config(bg="grey")

    def btnHoverConfig(self, btn):
    
        # adjusting background of the widget
        # background on entering widget
        btn.bind("<Enter>", func=lambda e: self.btnEnter(btn))
    
        # background color on leving widget
        btn.bind("<Leave>", func=lambda e: self.btnLeave(btn))

class btn(Button):
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
        super().__init__(parent, **kwargs)

        self.xpos = (self.master.winfo_x() + self.winfo_x())
        self.ypos = (self.master.winfo_y() +
                     self.winfo_y() +
                     self.winfo_height() + 10)

        self.bind("<Enter>", func=lambda x: self._btnEnter)
        self.bind("<Leave>", func=lambda x: self._btnLeave)
    
    def _btnEnter(self):
        if self.active:
            btn.config(bg=c.FGC)
            self._activateTooltip()
        else:
            btn.config(bg=c.INACTIVE_COLOR)
        if not self.ttActive:
            self._activateTooltip()
    
    def _btnLeave(self):
        if self.active:
            btn.config(bg="grey")
        else:
            btn.config(bg=c.INACTIVE_COLOR)
        if self.ttActive:
            self._deactivateTooltip()

    def _activateTooltip(self):
        self.tooltip.place(x=self.xpos, y=self.ypos)
    
    def _deactivateTooltip(self):
        self.tooltip.unplace()






if __name__ == "__main__":
    game = Gui()
    btn = btn(game.root)