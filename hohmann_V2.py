from time import sleep
from tkinter import *
import numpy as np

root = Tk()
resX = 1000; resY = 700
cent = np.array([resX/2, resY/2], dtype= float)
canvas = Canvas(root, bg="black", height=resY, width=resX); canvas.pack()

const = {
    'dT' : 10,
    'G' : 6.67e-11,
    'km' : 1000,
    'tMin' : 0
}
const['G'] *= const['dT']
sF = const['km'] * 100
earth = { 
    'm' : 5.9e24,
    'r' : 6371 * const['km'],
}

satList = []
class satelite:
    def __init__(self, xy, Vxy, tAlt):
        self.state = np.array([xy, Vxy], dtype= float) 
        self.cAlt = np.hypot(self.state[0,0], self.state[0,1])
        self.tAlt = tAlt
        self.phase = 'parking'
        self.trail = []
    def fG(self):
        self.cAlt = np.hypot(self.state[0,0], self.state[0,1])
        if self.cAlt >= earth['r']:
            F = (const['G'] * earth['m']) / self.cAlt **2
            rHat = self.state[0] / self.cAlt
            self.state[1] -= F * rHat
    def park(self):
        mu = const['G']/ const['dT'] * earth['m'] 
        vT = np.sqrt(mu * ((2/self.cAlt) - (1/self.cAlt)))
        gh = self.state[0]/self.cAlt
        xh = gh[1]; yh = gh[0]; xh *= -1
        ph = np.array([xh, yh], dtype= float)
        self.state[1] = vT * ph
        self.phase = 'parking'
    def transfer(self):
        mu = (const['G'] * earth['m']) / const['dT']
        gh = self.state[0]/self.cAlt
        xh = gh[1]; yh = gh[0]; xh *= -1
        ph = np.array([xh, yh], dtype= float)
        R = self.cAlt; a = (self.tAlt + R)/2
        vT = np.sqrt(mu*((2/R) - (1/a)))
        self.state[1] = vT * ph
        self.phase = 'transfer'
    def altCheck(self):
        if self.cAlt//100000 != self.tAlt//100000:
            if self.phase != 'transfer':
                self.transfer()
        elif self.phase != 'parking':
            self.park()
    def satLoop(self):
        self.fG()
        self.altCheck()
        self.state[0] += self.state[1] * const['dT']

test = satelite([0,7000000], [0,0], 7000000)
satList.append(test)

def render():
    canvas.delete('all')
    p1 = earth['r']//sF; p2 = p1 *(-1)
    canvas.create_oval(p1+resX/2, p1+resY/2, p2+resX/2, p2+resY/2, fill= 'dark blue', outline= 'blue')
    for s in satList:
        P = (s.state[0]//sF) + cent
        if const['tMin'] % 20 == 0:
            s.trail.append(P[0]); s.trail.append(P[1])
            if len(s.trail) > 1000:
                s.trail.pop(0); s.trail.pop(0)
        x1 = P[0] + 5; x2 = P[0] - 5
        y1 = P[1] + 5; y2 = P[1] - 5
        c1 = cent[0] + s.tAlt//sF; c2 = cent[1] + s.tAlt//sF
        c3 = cent[0] - s.tAlt//sF; c4 = cent[1] - s.tAlt//sF
        canvas.create_oval(c1,c2,c3,c4, outline= 'green')
        if len(s.trail) >= 2 and test.markOn == True:
            canvas.create_line(*s.trail, P[0], P[1], fill= 'white')
        canvas.create_rectangle(x1, y1, x2, y2, fill= 'green')
        canvas.create_text(5, 5, anchor = 'nw', fill= 'white', text= s.cAlt//const['km'])
        canvas.create_text(5, 25, anchor = 'nw', fill= 'white', text= s.tAlt//const['km'])
        canvas.create_text(5, 45, anchor = 'nw', fill= 'white', text= s.phase)
        canvas.create_text(5, 680, anchor = 'sw', fill= 'white', 
                           text= 'Velocity: ' + str(np.hypot(s.state[1,0], s.state[1,1])//1/const['km']) + ' km/s' )
        if test.markOn == True:
            for m in marks:
                x1 = cent[0] + m; x2 = cent[0] - m
                y1 = cent[1] + m; y2 = cent[1] - m
                canvas.create_oval(x1,y1,x2,y2, outline= 'red')
    canvas.update()

def gLoop(tLim):
    while const['tMin'] < tLim:
        sleep(0.015)
        const['tMin'] += const['dT']
        for s in satList:
            s.satLoop()
        render()

def altP(event):
    test.park()
    test.tAlt += sF * 5
def altM(event):
    test.park()
    test.tAlt -= sF * 5
canvas.bind('<Button-4>', altP)
canvas.bind('<Button-5>', altM)

marks = []
test.markOn = False
def markAdd(event):
    marks.append(test.cAlt//sF)
    test.markOn = True
def clearMarks(event):
    marks.clear()
    test.markOn = False
canvas.bind('<Button-1>', markAdd)
canvas.bind('<Button-3>', clearMarks)

gLoop(100000)
mainloop()