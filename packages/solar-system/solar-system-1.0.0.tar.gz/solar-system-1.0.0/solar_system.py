#!/usr/bin/env python3
"""
Solar system simulation using the
approximation method from Feynman-lectures,
p.9-8, using turtlegraphics.

Planet has a circular orbit, moon a stable
orbit around the planet.

Press Ctrl+"+" or Ctrl+"-" to zoom.
Press key ↑,↓,←,→ to move.
Press key "+" or key "-" to increase
or decrease the speed.

You can hold the movement temporarily by
pressing the left mouse button with the
mouse over the scrollbar of the canvas.

"""
from random import randrange
from turtle import Shape, Turtle, update, Screen, Terminator, Vec2D as Vec

__author__="七分诚意 qq:3076711200"
__email__="3416445406@qq.com"
__version__="1.0.0"

G = 8
#the mass of planets
SUN_MASS=1000000

MERCURY_MASS=125
VENUS_MASS=3000
EARTH_MASS=4000
MOON_MASS=30
MARS_MASS=600
PHOBOS_MASS=2
DEIMOS_MASS=1

JUPITER_MASS=7000
SATURN_MASS=6000
URANUS_MASS=9000
NEPTUNE_MASS=8000

scale=1
scr_x=0
scr_y=0

class GravSys(object):
    def __init__(self):
        self.planets = []
        self.removed_planets=[]
        self.t = 0
        self.dt = 0.01 # speed
        #frameskip: How many frames this program skips before drawing one.
        self.frameskip=5
    def init(self):
        for p in self.planets:
            p.init()
    def start(self):
        while True:
            for _ in range(self.frameskip):
                self.t += self.dt
                for p in self.planets:
                    p.step()

            for p in self.planets:
                p.update()
            update()

class Star(Turtle):
    def __init__(self, gravSys, m, x, v,
                 shape,shapesize=1,orbit_color=None,can_switchpen=True):
        Turtle.__init__(self)
        self.shape(shape)
        self.size=shapesize
        self.shapesize(shapesize)
        if orbit_color is not None:
            self.pencolor(orbit_color)
        self.penup()
        self.m = m
        self._pos=x
        self.setpos(x)
        self.v = v
        self.can_switchpen=can_switchpen
        gravSys.planets.append(self)
        self.gravSys = gravSys
        self.resizemode("user")
    def init(self):
        if self.can_switchpen:
            self.pendown()
        dt = self.gravSys.dt
        self.a = self.acc()
        self.v = self.v + 0.5*dt*self.a
    def acc(self):
        a = Vec(0,0)
        for planet in self.gravSys.planets:
            if planet is not self:
                v = planet._pos-self._pos
                try:
                    a += (G*planet.m/abs(v)**3)*v
                except ZeroDivisionError:pass
        return a
    def step(self):
        dt = self.gravSys.dt
        self._pos += dt*self.v
        
        self.a = self.acc()
        self.v = self.v + dt*self.a
    def update(self):
        self.setpos((self._pos+(scr_x,scr_y))*scale)
        if self.size>0.05:
            self.setheading(self.towards(self.gravSys.planets[0]))
        if abs(self._pos[0])>10000 or abs(self._pos[1])>10000:
            self.gravSys.removed_planets.append(self)
            self.gravSys.planets.remove(self)
            self.hideturtle()

##    def init(self):
##        dt = self.gravSys.dt
##        self.a = self.acc()
##        self.v = self.v + 0.5*dt*self.a
##    def acc(self):
##        a = Vec(0,0)
##        for planet in self.gravSys.planets:
##            if planet is not self:
##                v = planet.pos()-self.pos()
##                a += (G*planet.m/abs(v)**3)*v
##        return a
##    def step(self):
##        dt = self.gravSys.dt
##        self.setpos(self.pos() + dt*self.v)
##        self.setheading(self.towards(self.gravSys.planets[0]))
##        self.a = self.acc()
##        self.v = self.v + dt*self.a
####        if -100000<self.v[0]<100000 or -100000<self.v[1]<100000:
####            self.gravSys.planets.remove(self)

class Sun(Star):
    def step(self):
        pass
    def update(self):
        if self.size*scale<0.08:
            self.shapesize(0.08)
        self.setpos((self._pos+(scr_x,scr_y))*scale)
        #Star.update(self)

def main():
    scr=Screen()
    #scr.screensize(10000,10000)
    try:
        scr._canvas.master.state("zoomed")
    except:pass
    scr.bgcolor("black")
    scr.tracer(0,0)

    # create compound two-color turtleshape for planets
    s = Turtle()
    s.reset()
    s.getscreen().tracer(0,0)
    s.ht()
    s.pu()
    s.fd(6)
    s.lt(90)
    s.begin_poly()
    s.circle(8, 180)
    s.end_poly()
    _light = s.get_poly()
    s.begin_poly()
    s.circle(8, 180)
    s.end_poly()
    _dark = s.get_poly()
    s.begin_poly()
    s.circle(8)
    s.end_poly()
    _circle = s.get_poly()
    
    s.hideturtle()
    def create_shape(screen,name,light,dark=None):
        shape = Shape("compound")
        if dark is not None:
            shape.addcomponent(_light,light)
            shape.addcomponent(_dark,dark)
        else:
            shape.addcomponent(_circle,light)
        screen.register_shape(name, shape)
##    def gas_giant_shape(screen,name,light,dark):
##        # create shapes for gas-giant planets
        

    create_shape(scr,"mercury","gray70","grey50")
    create_shape(scr,"venus","gold","brown")
    create_shape(scr,"earth","blue","blue4")
    create_shape(scr,"moon","gray70","grey30")
    create_shape(scr,"mars","red","red4")
    create_shape(scr,"jupiter","burlywood1","burlywood4")
    create_shape(scr,"saturn","khaki1","khaki4")
    create_shape(scr,"uranus","light blue","blue")
    create_shape(scr,"neptune","blue","dark slate blue")

    # setup gravitational system
    gs = GravSys()
    sun = Sun(gs,SUN_MASS, Vec(0,0), Vec(0,0),
               "circle",1.8,can_switchpen=False)
    sun.color("yellow")
    sun.penup()

    mercury = Star(gs,MERCURY_MASS, Vec(60,0), Vec(0,330),
                 "mercury",0.5, "gray30")
    venus = Star(gs,VENUS_MASS, Vec(-130,0), Vec(0,-250),
                 "venus",0.7, "gold4")
    earth = Star(gs,EARTH_MASS, Vec(260,0), Vec(0,173),
                 "earth",0.8, "blue")
    moon = Star(gs,MOON_MASS, Vec(269,0), Vec(0,230),
                "moon",0.5, can_switchpen=False)

    mars = Star(gs,MARS_MASS, Vec(0,430), Vec(-140, 0),
                 "mars",0.6, "red")
    phobos = Star(gs,PHOBOS_MASS, Vec(0,436), Vec(-166, 0),
                 "circle",0.1, "orange", can_switchpen=False)
    phobos.fillcolor("orange")
    deimos = Star(gs,DEIMOS_MASS, Vec(0,439), Vec(-164, 0),
                 "circle",0.05, "yellow", can_switchpen=False)
    deimos.fillcolor("orange")
    # create asteroids
    for i in range(15):
        ast=Star(gs,1,Vec(0,0),Vec(0,0),
                      "circle",0.05,can_switchpen=False)
        ast.setheading(randrange(360))
        ast.forward(randrange(700,800))
        pos=ast._pos=ast.pos()
        ast.v=Vec(-pos[1]/7, pos[0]/7)
        ast.pu()
        ast.color("gray")

    jupiter = Star(gs, JUPITER_MASS, Vec(1100,0), Vec(0, 86),
                   "jupiter", 1.2, "darkgoldenrod4")
    saturn = Star(gs, SATURN_MASS, Vec(2200,0), Vec(0, 60),
                   "saturn", 1.0, "khaki2")
    uranus = Star(gs, URANUS_MASS, Vec(0, 4300), Vec(-43, 0),
                   "uranus", 0.8, "blue")
    neptune = Star(gs, NEPTUNE_MASS, Vec(7500,0), Vec(0, 34),
                   "neptune", 0.8, "midnight blue")
                   
    #bind key events
    def increase_speed(event):
        gs.dt+=0.001
    def decrease_speed(event):
        gs.dt-=0.001
    def zoom(event):
        global scale
        if event.keysym=="equal":
            # Zoom in
            scale*=1.33
        else:
            # Zoom out
            scale/=1.33
        for planet in gs.planets:
            planet.shapesize(planet.size*scale)
        scr.ontimer(clear_scr, 10)
    def clear_scr():
        for planet in gs.planets:
            planet.clear()

    def up(event=None):
        global scr_y
        scr_y-=50
        scr.ontimer(clear_scr, 10)
    def down(event=None):
        global scr_y
        scr_y+=50
        scr.ontimer(clear_scr, 10)
    def left(event=None):
        global scr_x
        scr_x+=50
        scr.ontimer(clear_scr, 10)
    def right(event=None):
        global scr_x
        scr_x-=50
        scr.ontimer(clear_scr, 10)

    cv=scr.getcanvas()
    cv.bind_all("<Key-Up>",up)
    cv.bind_all("<Key-Down>",down)
    cv.bind_all("<Key-Left>",left)
    cv.bind_all("<Key-Right>",right)
    cv.bind_all("<Key-equal>",increase_speed)
    cv.bind_all("<Key-minus>",decrease_speed)
    cv.bind_all("<Control-Key-equal>",zoom) #Ctrl+"+"
    cv.bind_all("<Control-Key-minus>",zoom) #Ctrl+"-"
    #scr.tracer(1,0)
    def switchpen(x,y):
        for planet in gs.planets+gs.removed_planets:
            if not planet.can_switchpen:
                continue
            if planet.isdown():
                planet.penup()
            else:planet.pendown()
            planet.clear()

    scr.onclick(switchpen)
    gs.init()
    gs.start()

if __name__ == '__main__':
    main()
    mainloop()
