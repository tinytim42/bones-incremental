#Resource Manager
from tkinter import *
import constants as c

class Resource:
    def __init__(self, name, frame, initAmt=0, max = 200):
        self.name = name
        self.amount = initAmt
        self.max = max
        self.unlocked = True
        self.nameLabel = Label(frame, text=(name + ":"),
                               font=c.font, bg=c.BGC, fg=c.FGC)
        self.amountLabel = Label(frame, text=str(self.amount),
                                 font=c.font, bg=c.BGC, fg=c.FGC)
        if self.max != -1:
            maxText = '/' + str(self.max)
        else:
            maxText = " "
        self.maxLabel = Label(frame, text= (maxText),
                              font=c.font, bg=c.BGC, fg=c.FGC)

    def _getAmount(self):
        return self.amount

    def _setAmount(self, amount):
        self.amount = amount
        self.flarp = 1
        self.amountLabel.configure(text=(str(self.amount)))

class ResourceManager:
    def __init__(self, root):
        self.keys = []
        self.resources={}
        self.root = root
        resourceFrame = Frame(self.root, width=250, height=600, bg=c.BGC)
        resourceFrame.grid(row=1, column=2, padx=5, pady=5)
        resourceFrame.grid_propagate(0)
        resourceFrame.grid_columnconfigure(0, weight=2)
        resourceFrame.grid_columnconfigure(1, weight=1)
        resourceFrame.grid_columnconfigure(2, weight=1)
        self.resourceFrame = resourceFrame

        bones = Resource("Bones", self.resourceFrame)
        sanity = Resource("Sanity", self.resourceFrame, 100, -1)
        resourceTitle = Label(self.resourceFrame, text="Resources",
                            bg=c.BGC, fg=c.FGC,
                            font=c.titleFont)
        resourceTitle.grid(sticky='w', row=0, column=0,
                        padx=5, pady=5)
        self._addResource(bones)
        self._addResource(sanity)
        self._addToFrame(bones)
        self._addToFrame(sanity)

    def _addResource(self, resource):
        self.keys.append(resource.name)
        self.resources[resource.name] = resource

    def _addToFrame(self, resource):
        name = resource.name
        rsc = self.resources[name]
        row = self.keys.index(name) + 1
        rsc.nameLabel.grid(row=row,
                           column=0,
                           sticky='w',
                           padx=5)
        rsc.amountLabel.grid(row=row,
                             column=1,
                             sticky='w',
                             padx=5)
        rsc.maxLabel.grid(row=row,
                          column=2,
                          sticky='w',
                          padx=5)

    def _gather(self, resource, mult=1):
        amt = self.resources[resource]._getAmount()
        self.resources[resource]._setAmount(amt + mult)


class Cutscene:
    def __init__(self, title="Title", text="Cutscene."):
        text = text.replace('\n', " ")
        self.frame = Frame(width=500, height=400, bg=c.BGC,
                           highlightbackground="black",
                           highlightthickness=5)
        self.frame.grid_propagate(0)
        self.title = Label(self.frame, text=title,
                           bg=c.BGC, fg=c.FGC,
                           font=c.titleFont)
        self.text = Label(self.frame, text=text,
                          bg=c.BGC, fg=c.FGC,
                          font=c.font, justify=LEFT,
                          wraplength=490)
        self.title.grid(row=0, column=0, sticky='w',
                        padx=5, pady=5)
        self.text.grid(row=1, column=0, sticky='w',
                       padx=5)
        #self.frame.place(x=200, y=100)
        #self.frame.lift()

    def _destroy(self):
        self.frame.place_forget()

class CutsceneManager:
    def __init__(self, root):
        self.root = root
        self.cutscenes = {}
        self.active = None
    
    def _createCutscene(self, csText):
        #csText is a three-item list containing key, title, and text
        self.cutscenes[csText[0]] = (Cutscene(csText[1], csText[2]))
    
    def _activateCutscene(self, key):
        self.cutscenes[key].frame.place(x=200, y=100)
        self.cutscenes[key].frame.lift()
        self.active = self.cutscenes[key]

    def _endCutscene(self):
        if self.active:
            self.active._destroy()
            self.active = None

class Log:
    def __init__(self, frame, text="It's a log!"):
        self.text = text
        self.frame = frame
        self.label = Label(frame, text=self.text, bg=c.BGC,
                           fg=c.FGC, font=c.font, justify=LEFT,
                           wraplength=240, padx=5)

class LogManager:
    def __init__(self, root):
        self.root = root
        #stack of all logs to be displayed onscreen
        self.logStack = []
        self.frame = Frame(self.root, width=250, height=600, bg=c.BGC)
        self.frame.grid(row=1, column=0, padx=5, pady=5)
        self.frame.grid_propagate(0)

        logTitle = Label(self.frame, text="Log", bg=c.BGC,
                        fg=c.FGC, font=c.titleFont, justify=LEFT)
        logTitle.grid(sticky='w', row=0, column=0, padx=5, pady=5)

        logItem = Log(self.frame, text="You are alone in an overgrown graveyard.")
        self.logStack.append(logItem)
        self._displayLogs()
    
    def _createLog(self, text="It's a created log!"):
        logItem = Log(self.frame, text=text)
        self.logStack.append(logItem)
        self._displayLogs()
    
    def _displayLogs(self):
        for log in self.logStack:
            log.label.grid(row=(self.logStack.index(log) + 1), column=0,
                     sticky='w')

class ActionManager:
    def __init__(self, rsm):
        pass
    

if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager(root)
    lm = LogManager(root)


