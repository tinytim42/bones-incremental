#Resource Manager
from tkinter import *
from objects import *
import constants as c
import text



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
        for key in text.csEvents.keys():
            self._createCutscene(key, text.csEvents[key])
        self.active = None
    
    def _createCutscene(self, csTitle, csText):
        #csText is a three-item list containing key, title, and text
        self.cutscenes[csTitle] = (Cutscene(csText[0], csText[1]))
    
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
    def __init__(self, root, rsm, ugm):
        self.root = root
        self.rsm = rsm
        self.ugm = ugm
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
        #self._addToFrame(1)
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
        bonesBtn = Btn(graveyard.frame, btns["Bones"])
        bonesBtn.bind("<Button-1>", 
                      lambda e:self.rsm._gather("Bones", "Click"))
        graveyard._addContent(bonesBtn, "bonesBtn", 0, 0)
        graveyard._addToFrame("bonesBtn")
        turnipBtn = BuyBtn(graveyard.frame, self, buyBtns["Turnip"])
        graveyard._addContent(turnipBtn, "turnipBtn", 0, 1)
        #graveyard._addToFrame("turnipBtn")
        tabList.append(graveyard)
        town = Tab("Town")
        town.frame.grid_columnconfigure(0, weight=1)
        town.frame.grid_columnconfigure(1, weight=1)
        shovel1Btn = BuyBtn(town.frame, self, buyBtns["Shovel1"])
        town._addContent(shovel1Btn, "shovel1Btn", 0, 0)
        town._addToFrame("shovel1Btn")
        tabList.append(town)
        return tabList

class UpgradeManager:
    def __init__(self, root, rsm):
        self.root = root
        self.rsm = rsm
        self.keys = []
        self.upgradeList = {}
        self._createUpgrades()
    
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

class FlagManager:
    def __init__(self, rsm, csm, afm, ugm, lm):
        self.rsm = rsm
        self.csm = csm
        self.afm = afm
        self.ugm = ugm
        self.lm = lm
        self.flags = {"START": False,
                      "UNLOCK_TURNIP": False}
        self.triggers = {"START": False,
                         "UNLOCK_TURNIP": False}
    
    def _checkTriggers(self):
        for trigger in self.triggers.keys():
            unlock = True
            resources = {}
            flags = []
            match trigger:
                case "START":
                    if self.flags["START"]:
                        unlock = False
                case "UNLOCK_TURNIP":
                    resources["Bones"] = 10
                    flags.append('START')
            #checks resources for unlock amount
            if len(resources.keys()) > 0:
                for r in resources.keys():
                    if self.rsm.resources[r]._getAmt() < resources[r]:
                        unlock = False
            #checks if all flag requirements are met
            if len(flags) > 0:
                for flag in flags:
                    if not self.flags[flag]:
                        unlock = False
            
            if unlock:
                self.triggers[trigger] = True

        for trigger in self.triggers.keys():
            if self.triggers[trigger]:
                self._resolveTriggers(trigger)

    def _resolveTriggers(self, trigger):
        match trigger:
            case "START":
                self.csm._activateCutscene('Introduction')
            case "UNLOCK_TURNIP":
                self.afm.tabs[0]._addToFrame("turnipBtn")

        self.triggers[trigger] = False
        self.flags[trigger] = True
        




if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager(root)
    ugm = UpgradeManager(root, rsm)
    lm = LogManager(root)
    afm = ActionManager(root, rsm, ugm)


