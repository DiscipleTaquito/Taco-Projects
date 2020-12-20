import random as rand
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()

C = {
    'G' : 1, #6.67e-11 meters, kg, seconds
    'dT' : 1,
    'eT' : 0,
    'tLim' : 3000,
    'km' : 1000
}

aList = [] #active
dList = [] #disabled

def cullList():
    temp = []
    for a in aList:
        if a.active == True:
            temp.append(a)
        else:
            dList.append(a)
    aList.clear()
    for a in temp:
        aList.append(a)

class body:
    def __init__(self, xy, v, mass):
        self.xy = np.array(xy, dtype= float)
        self.v = np.array(v, dtype= float)
        self.mass = mass
        self.rad = (mass / 3.14)**(1/3)
        self.active = True
        self.xLog = []
        self.yLog = []
    def fG(self):
        if self.active == True:
            for b in aList:
                if b.active == True and b != self:
                    dist = b.xy - self.xy
                    r = np.hypot(dist[0], dist[1])
                    if r > (self.rad + b.rad)*C['dT']:
                        mu = C['G'] * C['dT'] * self.mass * b.mass
                        fG = (mu / r**2) * (dist / r)
                        self.v += fG / self.mass
                    else:
                        cM = self.mass + b.mass
                        cxy = (self.xy + b.xy)/2
                        cv = ((self.mass * self.v) + (b.mass * b.v))//cM
                        b.active = False
                        self.mass = cM
                        self.xy = cxy
                        self.v = cv
                        self.rad = (cM / 3.14)**(1/3)
                        print('Strike')                 
    def translate(self):
        if self.active == True:
            self.xy += self.v * C['dT']
            self.xLog.append(self.xy[0])
            self.yLog.append(self.xy[1])

for i in range(0, 25):
    x = rand.randrange(-5000, 5000); y = rand.randrange(-5000, 5000) 
    x *= C['km']; y *= C['km']
    vx = rand.randrange(-1000, 1000); vy = rand.randrange(-1000, 1000) 
    aList.append(body([x,y], [vx,vy], 1e12))
    plt.plot(x, y, "b.")

while C['eT'] < C['tLim'] and len(aList) > 1:
    C['eT'] += C['dT']
    if C['eT']%60 == 0:
        prog = ((C['eT'] / C['tLim'])*100)//1
        print(prog)
    cullList()
    for a in aList:
        a.fG()
    for a in aList:
        a.translate()

for a in aList:
    x = a.xLog; y = a.yLog
    plt.plot(x,y)
    plt.plot(a.xy[0], a.xy[1], "ro")
for a in dList:
    x = a.xLog; y = a.yLog
    plt.plot(x,y, ls= '--')
plt.axis('equal')
plt.show()