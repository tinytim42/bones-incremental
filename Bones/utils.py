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

        bonesButton = Button(self.actionFrame, text="Dig for bones.",
                            width=15, bg="grey", font=c.font)
        bonesButton.tooltip = "The damp earth contains\na grisly reward."
        self.buttonHoverConfig(bonesButton)
        bonesButton.bind("<Button-1>",
                        lambda e:self.rsm._gather("Bones"))
        bonesButton.grid(row=1, column=0, padx=10, pady=5)

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
    def changeFgOnHover(self, button, colorOnHover, colorOnLeave):
    
        # adjusting background of the widget
        # background on entering widget
        button.bind("<Enter>",
                    func=lambda e: button.config(fg=colorOnHover))
    
        # background color on leving widget
        button.bind("<Leave>",
                    func=lambda e: button.config(fg=colorOnLeave))

    def addHeaderItem(self, frame, text="Blank", action=lambda: None):
        if frame.grid_size()[0] > 0:
            divider = Label(frame, text="|", bg=c.BGC, fg=c.FGC,
                            font=c.font)
            divider.grid(row=0,column=frame.grid_size()[0])

        headerButton = Button(frame, text=text, bg=c.BGC, fg=c.FGC,
                relief=FLAT, font=c.font, activebackground=c.BGC,
                activeforeground="white", bd=0)
        headerButton.grid(row=0, column=frame.grid_size()[0])
        headerButton.bind("<Button-1>", lambda e:action())
        self.changeFgOnHover(headerButton, "skyblue", c.FGC)

    def createTooltip(self, button):
        #gets absolute position based on root window
        xpos = (button.master.winfo_x() +
                button.winfo_x() +
                button.winfo_width() + 10)
        ypos = button.master.winfo_y() + button.winfo_y()
        tt = LabelFrame(self.root, width=500, height=60, bg=c.BGC)
        ttext = Label(tt, text=button.tooltip, bg=c.BGC,
                    fg=c.FGC, font=c.font)
        ttext.grid(row=0,column=0,padx=10,pady=5)
        tt.place(x=xpos, y=ypos)
        button.tt = tt

    def destroyTooltip(self, button):
        button.tt.destroy()

    def buttonEnter(self, button):
        if not self.csm.active:
            self.createTooltip(button)
            button.config(bg=c.FGC)

    def buttonLeave(self, button):
        if not self.csm.active:
            self.destroyTooltip(button)
            button.config(bg="grey")

    def buttonHoverConfig(self, button):
    
        # adjusting background of the widget
        # background on entering widget
        button.bind("<Enter>", func=lambda e: self.buttonEnter(button))
    
        # background color on leving widget
        button.bind("<Leave>", func=lambda e: self.buttonLeave(button))


#    def addResource(self, resource, label):
#        if not self.csm.active:
#            resource._set_amount(resource._get_amount() + 1)
#            label.configure(text=(resource.name + ": " +
#                                str(resource._get_amount())))



if __name__ == "__main__":
    game = Gui()