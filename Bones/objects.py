from tkinter import *
from textwrap import dedent
import constants as c

class Resource:
    def __init__(self, name, initAmt=0, max = 200, unlocked=True):
        self.name = name
        self.amt = initAmt
        self.clickMult = 1
        self.autoMult = 1
        self.max = max
        self.unlocked = unlocked
        self.nameLabel = Label(text=(name + ":"),
                               font=c.font, bg=c.BGC, fg=c.FGC)
        self.amtLabel = Label(text=str(self.amt),
                                 font=c.font, bg=c.BGC, fg=c.FGC)
        if self.max != -1:
            maxText = '/' + str(self.max)
        else:
            maxText = " "
        self.maxLabel = Label(text= (maxText),
                              font=c.font, bg=c.BGC, fg=c.FGC)

    def _getAmt(self):
        return self.amt

    def _setAmt(self, amt):
        self.amt = amt
        self.flarp = 1
        self.amtLabel.configure(text=(str(self.amt)))
    
    def _getMult(self, src="Click"):
        if src == "Click":
            return self.clickMult
        else:
            return self.autoMult
    
    def _setMult(self, mult, src="Click"):
        if src == "Click":
            self.clickMult = mult
        else:
            self.autoMult = mult

class Upgrade:
    def __init__(self, name, resource, mult=1, src="Click"):
        self.name = name
        self.resource = resource
        self.mult = mult
        self.src = src
        self.unlocked = False

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

    def _destroy(self):
        self.frame.place_forget()

class Log:
    def __init__(self, frame, text="It's a log!"):
        self.text = text
        self.frame = frame
        self.label = Label(frame, text=self.text, bg=c.BGC,
                           fg=c.FGC, font=c.font, justify=LEFT,
                           wraplength=240, padx=5)


class Btn(Button):
    def __init__(self, parent, dict, **kwargs):
        self.text = dict['text']
        self.root = parent.winfo_toplevel()
        #interactable (deactivated for cutscenes)
        self.active = True

        #style attributes
        self.bgc = c.IVORY
        self.fgc = c.BLACK
        #active color
        self.ac = c.AC

        #tooltip helpers
        self.tttext = dict['tttext']
        self.ttActive = False
        self.tooltip = LabelFrame(self.root, width=100, height=60, bg=c.BGC)

        self.label = Label(self.tooltip, text=self.tttext, bg=c.BGC,
                             fg=c.FGC, font=c.font, justify=LEFT,
                             wraplength=150)
        self.label.grid(row=0,column=0,padx=10,pady=5)
        #gets absolute position below button
        super().__init__(parent, text=dict['text'], 
                         width=15, bg=self.bgc, 
                         font=c.font, fg=self.fgc,
                         **kwargs)
        
        self.xpos = 0
        self.ypos = 0

        self.bind("<Enter>", lambda e:self._enter())
        self.bind("<Leave>", lambda e:self._leave())
    
    def _enter(self):
        self.config(bg=self.ac)
        if not self.ttActive:
            self._activateTooltip()
    
    def _leave(self):
        self.config(bg=self.bgc)
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

class BuyBtn(Btn):
    def __init__(self, parent, mgr, dict, **kwargs):
        self.mgr = mgr
        self.cost = dict['cost']
        #placeholder for thing to buy, must be Resource, Building, 
        #Unlock, or Upgrade class
        self.target = dict['target']
        #bool to set text color of text when not buyable
        #also checked when calling _buy()
        self.buyable = True
        #for one-time purchases, deactivates
        #button from purchasing but leaves tooltip enabled
        self.purchased = False
        #bool for one-time purchases
        self.oneTime = dict["oneTime"]
        #saves just flavor text in a separate attribute
        #to remove resource cost after one-time purchase
        self.flavorText = dict["tttext"]
        self.flavorText.replace("\t", "")
        self.flavorText.replace("\n", " ")
        tttext = self.flavorText + "\n----------------\n"
        for resource in self.cost.items():
            #formats cost tooltip
            tttext = (tttext + resource[0] + 
                      ": " + str(resource[1]) + "\n")
        
        dict['tttext'] = tttext
            
        super().__init__(parent, dict, **kwargs)
        self.bind("<Button-1>", lambda e: self._buy())
    
            
    def _buy(self):
        global game
        rsm = self.mgr.rsm
        ugm = self.mgr.ugm
        if self.buyable and not self.purchased:
            for resource in self.cost.items():
                amt = rsm.resources[resource[0]]._getAmt()
                amt -= resource[1]
                rsm.resources[resource[0]]._setAmt(amt)
            if self.oneTime:
                self.purchased = True
                self._setPurchased()
            if self.target in rsm.keys:
                rsm._gather(self.target)
            elif self.target in ugm.keys:
                ugm._activateUpgrade(self.target)
            else:
                print(self.target)

    def _setPurchased(self):
        self.configure(bg=c.INACTIVE_COLOR, activebackground=c.INACTIVE_COLOR)
        self.tttext = self.flavorText
        self.label.configure(text=self.tttext)
        self.active = False
        self.ac = c.INACTIVE_COLOR
        self.bgc = c.INACTIVE_COLOR
        self.state = 'disabled'
    
    def _setBuyable(self):
        for resource in self.cost.items():
            cost = resource[1]
            amt = self.mgr.rsm.resources[resource[0]]._getAmt()
        if not self.purchased:
            if self.buyable:
                if cost > amt:
                    self.buyable = False
                    self.configure(fg=c.UNBUYABLE_COLOR, bg=c.INACTIVE_COLOR,
                                activebackground=c.INACTIVE_COLOR,
                                activeforeground=c.UNBUYABLE_AC)
                    self.ac = c.INACTIVE_COLOR
                    self.bgc = c.INACTIVE_COLOR
                    self.fgc = c.UNBUYABLE_COLOR
            else:
                if cost <= amt:
                    self.buyable = True
                    self.configure(fg=c.BLACK, bg=c.IVORY)
                    self.bgc = c.IVORY
                    self.fgc = c.BLACK
                    self.ac = c.AC

#Tab class is for displaying and containing buttons in actionFrame
class Tab:
    def __init__(self, name):
        self.name = name
        self.frame = Frame(width=400, height=540, bg=c.BGC)
        self.frame.grid_propagate(0)
        self.parent = None
        self.btn = None
        self.active = False
        #2D list [widget, row, column]
        self.contents = {}
    
    def _addContent(self, widget, name, row, col):
        self.contents[name] = (widget, row, col)
    
    def _addToFrame(self, widgetName):
        content = self.contents[widgetName]
        content[0].grid(in_=self.frame,
                        row=content[1],
                        column=content[2],
                        padx=10, pady=5)
    
    def _activateTab(self):
        if not self.active:
            self.active = True
            self.frame.grid(in_=self.parent, row=1,column=0)
            self.frame.grid_propagate(0)
            if self.btn:
                self.btn.configure(font=c.boldFont)
    
    def _deactivateTab(self):
        if self.active:
            self.active = False
            self.frame.grid_forget()
            if self.btn:
                self.btn.configure(font=c.font)

buyBtns = {
    "Shovel1": {
        "text": "A Better Shovel.",
        "tttext":  "Dr. Ost has generously offered to trade " +
                   "a better shovel for your hard-earned bones. " +
                   "What could he want with them? Research, perhaps.",
        "cost": {"Bones": 100},
        "target": "Shovel1",
        "oneTime": True
    },
    "Turnip": {
        "text": "Buy Turnip",
        "tttext":  "Buy a juicy turnip!",
        "cost": {"Bones": 5},
        "target": "Turnips",
        "oneTime": False
    }
}

btns = {
    "Bones": {
        "text": "Dig for bones.",
        "tttext": "The damp earth contains a grisly reward."
    }
}
