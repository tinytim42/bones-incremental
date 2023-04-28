from tkinter import *
from managers import *
import constants as c

def saveGame():
    if csm.active:
        print("saved")

def exitGame():
    if csm.active:
        onExit()

# function to change properties of button on hover
def changeFgOnHover(button, colorOnHover, colorOnLeave):
 
    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>",
                func=lambda e: button.config(fg=colorOnHover))
 
    # background color on leving widget
    button.bind("<Leave>",
                func=lambda e: button.config(fg=colorOnLeave))

def buttonHoverConfig(button):
 
    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: buttonEnter(button))
 
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: buttonLeave(button))

def addHeaderItem(frame, text="Blank", action=lambda: None):
    if frame.grid_size()[0] > 0:
        divider = Label(frame, text="|", bg=c.BGC, fg=c.FGC,
                        font=c.font)
        divider.grid(row=0,column=frame.grid_size()[0])

    headerButton = Button(frame, text=text, bg=c.BGC, fg=c.FGC,
              relief=FLAT, font=c.font, activebackground=c.BGC,
              activeforeground="white", bd=0)
    headerButton.grid(row=0, column=frame.grid_size()[0])
    headerButton.bind("<Button-1>", lambda e:action())
    changeFgOnHover(headerButton, "skyblue", c.FGC)

def createTooltip(button):
    #gets absolute position based on root window
    xpos = (button.master.winfo_x() +
            button.winfo_x() +
            button.winfo_width() + 10)
    ypos = button.master.winfo_y() + button.winfo_y()
    tt = LabelFrame(root, width=500, height=60, bg=c.BGC)
    ttext = Label(tt, text=button.tooltip, bg=c.BGC,
                  fg=c.FGC, font=c.font)
    ttext.grid(row=0,column=0,padx=10,pady=5)
    tt.place(x=xpos, y=ypos)
    button.tt = tt

def destroyTooltip(button):
    button.tt.destroy()

def buttonEnter(button):
    if not csm.active:
        createTooltip(button)
        button.config(bg=c.FGC)

def buttonLeave(button):
    if not csm.active:
        destroyTooltip(button)
        button.config(bg="grey")

def addResource(resource, label):
    if not csm.active:
        resource._set_amount(resource._get_amount() + 1)
        label.configure(text=(resource.name + ": " +
                              str(resource._get_amount())))

def initializeGame():
    root = Tk()
    rsm = ResourceManager()
    csm = CutsceneManager()
    root.title("Bones Incremental")
    root.configure(background="black")
    root.minsize(c.SCREEN_SIZE[0], c.SCREEN_SIZE[1])
    #checks if anywhere onscreen is clicked, to exit cutscenes
    #root.bind("<Button-1>", lambda e:csm._killCutscene())

    headerFrame = Frame(root, width=900, height=30, bg=c.BGC)
    headerFrame.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
    headerFrame.grid_propagate(0)

    addHeaderItem(headerFrame, "Save", saveGame)
    addHeaderItem(headerFrame, "Exit", exitGame)
                     
    resourceFrame = Frame(root, width=200, height=600, bg=c.BGC)
    resourceFrame.grid(row=1, column=0, padx=5, pady=5)
    resourceFrame.grid_propagate(0)

    initResources(rsm, resourceFrame)

    actionFrame = Frame(root, width=400, height=600, bg=c.BGC)
    actionFrame.grid(row=1, column=1, padx=5, pady=5)
    actionFrame.grid_propagate(0)
    actionFrame.grid_columnconfigure(0, weight=1)
    actionFrame.grid_columnconfigure(1, weight=1)

    actionHeader = Frame(actionFrame, bg=c.BGC, width=400, height=40)
    actionHeader.grid(row=0,column=0,columnspan=2)
    actionHeader.grid_propagate(0)
    addHeaderItem(actionHeader, "Graveyard")
    addHeaderItem(actionHeader, "Town")

    bonesButton = Button(actionFrame, text="Dig for bones.",
                         width=15, bg="grey", font=c.font)
    bonesButton.tooltip = "The damp earth contains\na grisly reward."
    buttonHoverConfig(bonesButton)
    bonesButton.bind("<Button-1>",
                     lambda e:rsm._gather("Bones"))
    bonesButton.grid(row=1, column=0, padx=10, pady=5)


    logFrame = Frame(root, width=300, height=600, bg=c.BGC)
    logFrame.grid(row=1, column=2, padx=5, pady=5)
    logFrame.grid_propagate(0)

    logTitle = Label(logFrame, text="Log", bg=c.BGC,
                     fg=c.FGC, font=c.titleFont, justify=LEFT)
    logTitle.grid(sticky='w', row=0, column=0, padx=5, pady=5)

    logItem = Label(logFrame, text="You are alone in an\novergrown graveyard.",
                    bg=c.BGC, fg=c.FGC, font=c.font, justify=LEFT)
    logItem.grid(row=1, column=0, padx=5, pady=5)

    return [root, rsm, csm]

if __name__ == "__main__":
    game = initializeGame()
    root = game[0]
    rsm = game[1]
    csm = game[2]
