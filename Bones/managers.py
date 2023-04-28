#Resource Manager
from tkinter import *
import constants as c

class Resource:
    def __init__(self, name, frame, initAmt=0):
        self.name = name
        self.active = True
        self.amount = initAmt
        #Remember to set parent to ResourceFrame when constructing
        self.label = Label(frame, text=(name + ": " + str(self.amount)),
                           font=c.font, bg=c.BGC, fg=c.FGC)

    def _get_amount(self):
        return self.amount

    def _set_amount(self, amount):
        self.amount = amount
        self.flarp = 1
        self.label.configure(text=(self.name + ": " + str(self.amount)))

class ResourceManager:
    def __init__(self):
        self.keys = []
        self.resources={}

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

    def _destroy(self):
        self.frame.destroy()

class CutsceneManager:
    def __init__(self):
        self.cutscenes = []
        self.flags = []
        self.active = None

    def _killCutscene(self):
        self.active.destroy()
        self.active = None

def initResources(rsm, frame):
    bones = Resource("Bones", frame)
    sanity = Resource("Sanity", frame, 100)
    resourceTitle = Label(frame, text="Resources",
                          bg=c.BGC, fg=c.FGC,
                          font=c.titleFont)
    resourceTitle.grid(sticky='w', row=0, column=0,
                       padx=5, pady=5)
    rsm._addResource(bones)
    rsm._addResource(sanity)
    rsm._addToFrame(bones)
    rsm._addToFrame(sanity)
    

if __name__ == "__main__":
    root = Tk()
    rsm = ResourceManager()
    initResources(rsm, root)


