#Resource Manager
from tkinter import *
import constants as c

class Resource:
    def __init__(self, name, frame, initAmt=0, max = 200):
        self.name = name
        self.amount = initAmt
        self.max = max
        self.unlocked = True
        self.multiplier = 1
        self.label = Label(frame, text=(name + ": " + str(self.amount)),
                           font=c.font, bg=c.BGC, fg=c.FGC)

    def _get_amount(self):
        return self.amount

    def _set_amount(self, amount):
        self.amount = amount
        self.flarp = 1
        self.label.configure(text=(self.name + ": " + str(self.amount)))

class ResourceManager:
    def __init__(self, root):
        self.keys = []
        self.resources={}
        self.root = root
        resourceFrame = Frame(self.root, width=200, height=600, bg=c.BGC)
        resourceFrame.grid(row=1, column=0, padx=5, pady=5)
        resourceFrame.grid_propagate(0)
        self.resourceFrame = resourceFrame

        bones = Resource("Bones", self.resourceFrame)
        sanity = Resource("Sanity", self.resourceFrame, 100)
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
        self.resources[name].label.grid(row=(self.keys.index(name) + 1),
                                        column=0,
                                        sticky='w',
                                        padx=5)

    def _gather(self, resource):
        amt = self.resources[resource]._get_amount()
        self.resources[resource]._set_amount(amt + 1)


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
        self.frame.place(x=200, y=100)
        self.frame.lift()

    def _destroy(self):
        self.frame.place_forget()

class CutsceneManager:
    def __init__(self, root):
        self.root = root
        self.cutscenes = []
        self.flags = []
        self.active = None
    
    def _createCutscene(self, title='Title',text="It's a cutscene!"):
        self.cutscenes.append(Cutscene(title, text))

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
                           wraplength=290, padx=5)

class LogManager:
    def __init__(self,root):
        self.root = root
        #stack of all logs to be displayed onscreen
        self.logStack = []
        self.frame = Frame(self.root, width=300, height=600, bg=c.BGC)
        self.frame.grid(row=1, column=2, padx=5, pady=5)
        self.frame.grid_propagate(0)

        logTitle = Label(self.frame, text="Log", bg=c.BGC,
                        fg=c.FGC, font=c.titleFont, justify=LEFT)
        logTitle.grid(sticky='w', row=0, column=0, padx=5, pady=5)

        logItem = Log(self.frame, text="You are alone in an overgrown graveyard.")
        self.logStack.append(logItem)
        self._displayLogs()
    
    def _displayLogs(self):
        for log in self.logStack:
            log.label.grid(row=(self.logStack.index(log) + 1), column=0,
                     sticky='w')

    

if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager(root)
    lm = LogManager(root)


