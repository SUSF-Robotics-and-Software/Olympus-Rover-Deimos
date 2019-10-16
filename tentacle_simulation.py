from tkinter import *
from math import *
import time
#INPUT PARAMETERS
H1 = 50 + 80 #distance between socket and base
L1 = 10 + 20 #extra base from cord
R1 = 50 + 50 #radius of hemi-sphere
R2 = 30 + 50 #radius of socket
R3 = 80 + 50 #radius of base

#number of articulations
n=6

#scaling for each ball
multiplier = 0.7

global li
li = []

class coord():
    def __init__(self,x,y):
        self.x = x
        self.y = y

class sock_ball():
    def __init__(self,center,theta,multiplier,n):
        self.center = center
        self.angle = theta
        #INPUT PARAMETERS
        self.h1 = H1*multiplier**n
        self.l1 = L1*multiplier**n
        self.r1 = R1*multiplier**n
        self.r2 = self.r1*multiplier
        self.r3 = R3*multiplier**n
        self.plate_left = 0
        self.plate_right = 0

    def draw(self,canvas,origin):
        theta = self.angle
        #PLATE
        self.plate_left = coord(self.center.x - (self.r3)*cos(theta), self.center.y + (self.r3)*sin(theta))
        self.plate_right = coord(self.center.x + (self.r3)*cos(theta), self.center.y - (self.r3)*sin(theta))
        x1 = self.center.x - (self.r3+self.l1)*cos(theta)
        x2 = self.center.x + (self.r3+self.l1)*cos(theta) 
        y1 = self.center.y + (self.r3+self.l1)*sin(theta)
        y2 = self.center.y - (self.r3+self.l1)*sin(theta) 
        canvas.create_line(x1,y1,x2,y2)

        #SOCKET
        x1 = self.center.x - self.h1*cos(pi/2-theta) - self.r2
        x2 = self.center.x - self.h1*cos(pi/2-theta) + self.r2
        y1 = self.center.y - self.h1*sin(pi/2-theta) - self.r2
        y2 = self.center.y - self.h1*sin(pi/2-theta) + self.r2
        canvas.create_oval(x1, y1, x2, y2, width = 1, fill = "white")
        

        #Base and hemi-sphere
        x1 = self.center.x - self.r1
        x2 = self.center.x + self.r1
        y1 = self.center.y - self.r1
        y2 = self.center.y + self.r1
        canvas.create_arc(x1, y1, x2, y2, start=0+(theta/pi)*180, extent=180, width = 1, fill = "white")

        return coord(self.center.x - self.h1*cos(pi/2-theta), self.center.y - self.h1*sin(pi/2-theta))


        
#tkinter initialisation
root = Tk()
canvas = Canvas(root,height=1000,width=1000)
origin = coord(800,900)


objs = []
center = origin
objs.append(sock_ball(center,0,multiplier,0))
center = objs[-1].draw(canvas,origin)
canvas.pack()



#calc largest possible angle

angs = []
try:
    angs.append(asin(H1/(R3+L1)))
except:
    print("Plates never touch")

    
try:
    angs.append(pi/2-asin(R1/H1))
except:
    print("Plates never touch orbs")
    
ang = min(angs)
curr_ang = 0
in_range = True
x = 0

#while angle in acceptable range
while in_range == True:
    center = origin
    x += 1
    objs = []
    #create initial joint
    objs.append(sock_ball(center,0,multiplier,0))
    center = objs[-1].draw(canvas,origin)

    #create joints a seperation of curr_ang
    for i in range(1,n,1):    
        objs.append(sock_ball(center,objs[-1].angle+curr_ang,multiplier,i))
        center = objs[-1].draw(canvas,origin)
        canvas.pack()


    length_left = 0
    length_right = 0
    #draw cords
    for i in range (len(objs)-1):
        length_left +=  sqrt((objs[i].plate_left.x - objs[i+1].plate_left.x)**2 + (objs[i].plate_left.y - objs[i+1].plate_left.y)**2)
        canvas.create_line(objs[i].plate_left.x,objs[i].plate_left.y, objs[i+1].plate_left.x, objs[i+1].plate_left.y)
        length_right += sqrt((objs[i].plate_right.x - objs[i+1].plate_right.x)**2 + (objs[i].plate_right.y - objs[i+1].plate_right.y)**2)
        canvas.create_line(objs[i].plate_right.x,objs[i].plate_right.y, objs[i+1].plate_right.x, objs[i+1].plate_right.y)
    


    #calculate difference in cord length
    print(abs(length_left-length_right))
    #print(length_left/length_right)

        


    #list centres
    li.append([center.x,center.y])
    #increment angle
    curr_ang = x*pi/(360*4)
    #draw centres - can create lag
    """for item in li:
        canvas.create_oval(item[0]-2,item[1]-2,item[0]+2,item[1]+2,fill="red")
        canvas.pack()"""
    #update frame
    canvas.update()
    if curr_ang > ang:
        in_range = False
    else:
        canvas.delete("all")


#max x displacement marker
small_ang_disp = center.x - origin.x
"""canvas.create_line(origin.x,origin.y,origin.x+small_ang_disp,origin.y,fill = "red")
canvas.pack()"""
