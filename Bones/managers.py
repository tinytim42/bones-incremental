#Resource Manager
from tkinter import *
from objects import *
import constants as c



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

#class for managing action frame
class ActionManager:
    def __init__(self, root, rsm):
        self.root = root
        self.rsm = rsm
        self.tabs = []
        self.activeTab = None
        actionFrame = Frame(self.root, width=400, height=600, bg=c.BGC)
        actionFrame.grid(row=1, column=1, padx=5, pady=5)
        actionFrame.grid_propagate(0)

        actionHeader = Frame(actionFrame, bg=c.BGC, width=400, height=40)
        actionHeader.grid(row=0,column=0)
        actionHeader.grid_propagate(0)
    
        self.frame = actionFrame
        self.header = actionHeader
    
    def _addTab(self, tab):
        self.tabs.append(tab)
    
    def _changeTab(self):
        pass


#Tab class is for displaying and containing buttons in actionFrame
class Tab:
    def __init__(self, name, parent):
        self.name = name
        self.frame = Frame(parent, width=400, height=540, bg=c.BGC)
        self.parent = parent
        self.btn = None
        self.active = False
        #2D list [widget, row, column]
        self.contents = []
    
    def _addContent(self, widget, col, row):
        self.contents.append([widget, col, row])
    
    def _activateTab(self):
        if not self.active:
            self.active
            self.frame.grid(row=1,column=0)
    
    def _deactivateTab(self):
        if self.active:
            self.active = False
            for content in self.contents:
                content[0].ungrid()






if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager(root)
    lm = LogManager(root)


