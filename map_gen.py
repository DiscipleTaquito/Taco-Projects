from tkinter import *
import random as rand

root = Tk()
resX = 1000; resY = 500
canvas = Canvas(root, bg="blue", height=resY, width=resX); canvas.pack()

map = {
    'xy': [200, 100],
    'cLevel': 0,
    'nodes': [],
    'seed': 10,
    'Choice': [-100, 200]
}

class node:
    def __init__(self, xy):
        self.xy = xy
        self.el = 0
        self.temp = 0         
        self.neighbors = []
        self.active = True   
    def render(self):
        if self.el <= (-25):
            color = 'dark blue'
        elif self.el <= map['cLevel']:
            color = 'blue'
        elif self.el <= 25 and self.temp <=0:
            color = 'light grey'
        elif self.el <= 25 and self.temp <=5:
            color = 'green'
        elif self.el <= 25 and self.temp <=10:
            color = 'dark green'
        elif self.el <= 25 and self.temp <=100:
            color = 'yellow'
        else:
            color = 'white'
        a = self.xy[0]*5; b = self.xy[1]*5
        c = a + 5; d = b + 5
        canvas.create_rectangle(a,b,c,d, fill= color, outline= color)

def genNodes():
    for i in range(map['xy'][0]):
        for j in range(map['xy'][1]):
            map['nodes'].append(node([i,j]))
print('Gen')
genNodes()

def getNeighbors():
    temp = []
    for n in map['nodes']:
        temp.append(n)
    for n1 in map['nodes']:
        temp.pop(0)
        for n2 in temp:
            if n1 != n2:
                if n1.xy[0] == n2.xy[0]:
                    if n2.xy[1] == n1.xy[1] + 1:
                        n1.neighbors.append(n2)
                elif n1.xy[1] == n2.xy[1]:
                    if n2.xy[0] == n1.xy[0] + 1:
                        n1.neighbors.append(n2)
                if len(n1.neighbors) >= 2:
                    break

print('Getting Neighbors')
getNeighbors()

def seed():
    for n in map['nodes']:
        if 40 < n.xy[0] < 160:
            if 20 < n.xy[1] < 80:
                if rand.randint(0, 1000) <= map['seed']:
                    n.el = rand.choice(map['Choice'])
                    n.temp = rand.choice(map['Choice'])

print('Seeding')
seed()

def setActive():
    for n in map['nodes']:
        n.active = True

def smoothMap():
    for n1 in map['nodes']:
        n1.active = False
        for n2 in n1.neighbors:
            if n2.active == True:
                if n1.el != n2.el:
                    if rand.randrange(0, 100) < 5:
                        a = (n1.el + n2.el)/2
                        n1.el = a
                        n2.el = a
                    elif rand.randrange(0, 100) < 5:
                        a = (n1.temp + n2.temp)/2
                        n1.temp = a
                        n2.temp = a

def raiseLand():
    for n in map['nodes']:
        if n.el > 0:
            if rand.randrange(0, 100) < 1:
                n.el += 100
def lowerSea():
    for n in map['nodes']:
        if n.el <= 0:
            if rand.randrange(0, 100) < 1:
                n.el -= 100
def raiseTemp():
    for n in map['nodes']:
        if n.el > 0:
            if rand.randrange(0, 100) < 1:
                n.temp += 10

def process1():
    setActive()
    smoothMap()
def process2():
    setActive()
    lowerSea()
    canvas.delete('all')
def process3():
    setActive()
    raiseLand()  
def process4():
    setActive()
    raiseTemp()

    
print('0')
for i in range(100):
    process1()
    process4()
print('1')
for i in range(15):
    process2()
    process3()
print('2')
for i in range(100):
    process1()

canvas.delete('all')
for n in map['nodes']:
    n.render()
canvas.update()

mainloop()
