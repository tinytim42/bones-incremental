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
        self.frame = resourceFrame

        resourceTitle = Label(self.frame, text="Resources",
                            bg=c.BGC, fg=c.FGC,
                            font=c.titleFont)
        resourceTitle.grid(sticky='w', row=0, column=0,
                        padx=5, pady=5)
        for resource in self._createResources():
            self._addResource(resource)
        self._addToFrame("Sanity")
        self._addToFrame("Bones")

    def _addResource(self, resource):
        self.keys.append(resource.name)
        self.resources[resource.name] = resource

    def _addToFrame(self, name):
        rsc = self.resources[name]
        row = self.keys.index(name) + 1
        rsc.nameLabel.grid(in_=self.frame,
                           row=row,
                           column=0,
                           sticky='w',
                           padx=5)
        rsc.amtLabel.grid(row=row,
                          column=1,
                          sticky='w',
                          padx=5,
                          in_=self.frame)
        rsc.maxLabel.grid(row=row,
                          column=2,
                          sticky='e',
                          padx=5,
                          in_=self.frame)

    def _gather(self, resource, src="Click"):
        rsc = self.resources[resource]
        if src == "Click":
            mult = rsc.clickMult
        else:
            mult = rsc.autoMult
        amt = rsc._getAmt()
        rsc._setAmt(amt + mult)
        if rsc.unlocked == False:
            rsc.unlocked == True
            self._addToFrame(rsc.name)
    
    def _createResources(self):
        resourceList = [
            Resource("Sanity",
                    max=-1,
                    initAmt=100),
            Resource("Bones", 
                    max=200, 
                    initAmt=0),
            Resource("Turnips", 
                    max=1000,
                    initAmt = 0,
                    unlocked=False),
            Resource("Golden Turnips",
                    max=10,
                    initAmt=0,
                    unlocked=False)
        ]
        return resourceList

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

        for tab in self._createTabs():
            self._addTab(tab)
        self._addToFrame(0)
        self._changeTab(0)
    
    def _addTab(self, tab):
        tab.parent = self.frame
        self.tabs.append(tab)
    
    def _changeTab(self, tabIndex):
        for i in range(len(self.tabs)):
            if i != tabIndex:
                self.tabs[i]._deactivateTab()
        self.tabs[tabIndex]._activateTab()
        self.activeTab = self.tabs[tabIndex]

    def _addToFrame(self, tabIndex):
        tab = self.tabs[tabIndex]
        if self.header.grid_size()[0] > 0:
            divider = Label(self.header, text="|", bg=c.BGC, fg=c.FGC,
                            font=c.font)
            divider.grid(row=0,column=self.header.grid_size()[0])

        headerBtn = HeaderBtn(self.header, text=tab.name, action=lambda e:self._changeTab(tabIndex))
        tab.btn = headerBtn
        headerBtn.grid(row=0, column=self.header.grid_size()[0])
    
    def _createTabs(self):
        tabList = []
        graveyard = Tab("Graveyard")
        graveyard.frame.grid_columnconfigure(0, weight=1)
        graveyard.frame.grid_columnconfigure(1, weight=1)
        bonesBtn = Btn(graveyard.frame, text="Dig for bones.",
                       tttext="The damp earth contains\na grisly reward.")
        bonesBtn.bind("<Button-1>", 
                      lambda e:self.rsm._gather("Bones", "Click"))
        graveyard._addContent(bonesBtn, 0, 0)
        graveyard._addToFrame(0)

        turnipBtn = BuyBtn(graveyard.frame)
        turnipBtn.bind("<Button-1>", lambda e:turnipBtn._buy(self.rsm))
        graveyard._addContent(turnipBtn, 0, 1)
        graveyard._addToFrame(1)
        tabList.append(graveyard)
        town = Tab("Town")
        tabList.append(town)
        return tabList

class UpgradeManager:
    def __init__(self, root, rsm):
        self.root = root
        self.rsm = rsm
        self.keys = []
        self.upgradeList = {}
    
    def _createUpgrades(self):
        ug = Upgrade("Shovel1", "Bones", 1, "Click")
        self._addUpgrade(ug)
    
    def _addUpgrade(self, upgrade):
        self.upgradeList[upgrade.name] = upgrade
        self.keys.append(upgrade.name)
    
    def _activateUpgrade(self, name):
        ug = self.upgradeList[name]
        resource = self.rsm.resources[ug.resource]
        mult = ug.mult
        src = ug.src
        currentMult = resource._getMult(src)
        newMult = currentMult + mult
        resource._setMult(newMult, src)



if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager(root)
    lm = LogManager(root)
    afm = ActionManager(root, rsm)


