import pymunk
import pygame
from getworkingpath import *


"""------------------------------------------------------"""
pig = pygame.image.load(getworkingpath()+"/pig.png") #loader bilde av pig
vertikale_planker = [] #Lager liste med de vertikale plankene
horisontale_planker = [] #Lager liste med de horisontale plankene
pigs = [] #Lager liste med grisene
"""------------------------------------------------------"""

class Pig(): #Class pig.
    def __init__(self, x, y, space): #__init__ gjør at den kjører seg selv når man calller Pig()
        #Gir grisen noen fysiske verdier
        mass = 2
        radius = 14
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        #Assibner en body og shape til grisen
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 2 #collision type 2
        space.add(body, shape) #legger til i space
        self.body = body #Hvis jeg caller Pig.body senere i koden vil jeg bå bodyen til grisen
        self.shape = shape

class vertikale(): #Class vertikale
    def __init__(self, x, y, space): #__init__ gjør at den kjører seg selv når man calller vertikale()
        #Gir planker noen fysiske verdier og body og shape
        mass = 5
        shape = pymunk.Poly.create_box(None, size = (25,90))
        moment = pymunk.moment_for_poly(mass, shape.get_vertices())
        body = pymunk.Body(mass, moment)
        shape.body = body
        body.position = x, y 
        shape.elasticity = 0.7
        shape.friction = 0.9
        shape.collision_type = 3 #collision type 3
        shape.color = (197, 86, 33, 255) #farge
        space.add(body, shape) #Legger til i space
        self.body = body
        self.shape = shape


class horisontale(): #class horisontale
    def __init__(self, x, y, space):#__init__ gjør at den kjører seg selv når man calller horisontale()
        #Gir planker noen fysiske verdier og body og shape
        mass = 5
        shape = pymunk.Poly.create_box(None, size = (90,25))
        moment = pymunk.moment_for_poly(mass, shape.get_vertices())
        body = pymunk.Body(mass, moment)
        shape.body = body
        body.position = x, y 
        shape.elasticity = 0.7
        shape.friction = 0.9
        shape.collision_type = 3 #collision type 3
        shape.color = (197, 86, 33, 255) #farge
        space.add(body, shape) #Legger til i space
        self.body = body
        self.shape = shape
"""
Kommer ikke til å kommentere all kode pr level. Kort sagt:
Når jeg skriver:
v1 = vertikale(600, 130, space) 
vertikale_planker.append(v1)
vil det legges til en vertikal planke i koordinatene (600, 130) i space
Denne planken legges også til i listen vertikale_planker.

Det er likt for horisontale planker og pig også.
De ulike delene og grisene danner en bane, som kjøres i hovedkoden
"""

def level1(space):
    global pigs
    v1 = vertikale(600, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(650, 130, space) 
    vertikale_planker.append(v2)
    pig1 = Pig(620, 100, space)
    pigs.append(pig1)
    h1 = horisontale(630, 200, space)
    horisontale_planker.append(h1)

def level2(space):
    global pigs
    v1 = vertikale(600, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(650, 130, space) 
    vertikale_planker.append(v2)
    v3 = vertikale(720, 130, space) 
    vertikale_planker.append(v3)
    pig1 = Pig(620, 100, space)
    pigs.append(pig1)
    pig2 = Pig(670, 100, space)
    pigs.append(pig2)
    h1 = horisontale(630, 200, space)
    horisontale_planker.append(h1)
    h2 = horisontale(720, 200, space)
    horisontale_planker.append(h2)

def level3(space):
    global pigs
    v1 = vertikale(600, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(650, 130, space) 
    vertikale_planker.append(v2)
    v3 = vertikale(720, 130, space) 
    vertikale_planker.append(v3)
    v4 = vertikale(650, 220, space) 
    vertikale_planker.append(v4)
    v5 = vertikale(720, 220, space) 
    vertikale_planker.append(v5)

    pig1 = Pig(620, 100, space)
    pigs.append(pig1)
    pig2 = Pig(670, 100, space)
    pigs.append(pig2)
    pig3 = Pig(685, 320, space)
    pigs.append(pig3)

    h1 = horisontale(630, 200, space)
    horisontale_planker.append(h1)
    h2 = horisontale(720, 200, space)
    horisontale_planker.append(h2)
    h3 = horisontale(670, 290, space)
    horisontale_planker.append(h3)

def level4(space):
    global pigs
    v1 = vertikale(600, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(680, 130, space)     
    vertikale_planker.append(v2)
    v3 = vertikale(760, 130, space)     
    vertikale_planker.append(v3)
    v4 = vertikale(840, 130, space)     
    vertikale_planker.append(v4)
    v5 = vertikale(840, 220, space)     
    vertikale_planker.append(v5)

    h1 = horisontale(630, 190, space)
    horisontale_planker.append(h1)
    h2 = horisontale(710, 190, space)
    horisontale_planker.append(h2)

    pig1 = Pig(635, 150, space)
    pigs.append(pig1)
    pig2 = Pig(720, 150, space)
    pigs.append(pig2)
    pig3 = Pig(840, 285, space)
    pigs.append(pig3)

def level5(space):
    global pigs
    h1 = horisontale(500, 120, space)
    horisontale_planker.append(h1)
    h2 = horisontale(500, 150, space)
    horisontale_planker.append(h2)
    h3 = horisontale(500, 180, space)
    horisontale_planker.append(h3)
    h4 = horisontale(500, 210, space)
    horisontale_planker.append(h4)
    h5 = horisontale(500, 240, space)
    horisontale_planker.append(h5)
    h6 = horisontale(500, 270, space)
    horisontale_planker.append(h6)
    h7 = horisontale(500, 300, space)
    horisontale_planker.append(h7)
    h8 = horisontale(500, 330, space)
    horisontale_planker.append(h8)

    h9 = horisontale(650, 120, space)
    horisontale_planker.append(h9)
    h10 = horisontale(650, 150, space)
    horisontale_planker.append(h10)
    h11 = horisontale(650, 180, space)
    horisontale_planker.append(h11)
    h12 = horisontale(650, 210, space)
    horisontale_planker.append(h12)
    h13 = horisontale(650, 240, space)
    horisontale_planker.append(h13)
    h14 = horisontale(650, 270, space)
    horisontale_planker.append(h14)
    h15 = horisontale(650, 300, space)
    horisontale_planker.append(h15)
    h16 = horisontale(650, 330, space)
    horisontale_planker.append(h16)

    v1 = vertikale(580, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(580, 210, space) 
    vertikale_planker.append(v2)

    pig1 = Pig(1000, 140, space)
    pigs.append(pig1)
    pig2 = Pig(1050, 140, space)
    pigs.append(pig2)
    pig3 = Pig(950, 140, space)
    pigs.append(pig3)

def level6(space):
    global pigs
    pig1 = Pig(400, 140, space)
    pigs.append(pig1)
    pig2 = Pig(480, 140, space)
    pigs.append(pig2)
    pig3 = Pig(560, 140, space)
    pigs.append(pig3)
    pig4 = Pig(640, 140, space)
    pigs.append(pig4)
    pig5 = Pig(720, 140, space)
    pigs.append(pig5)
    pig6 = Pig(800, 140, space)
    pigs.append(pig6)
    pig7 = Pig(880, 140, space)
    pigs.append(pig7)

    v1 = vertikale(440, 130, space) 
    vertikale_planker.append(v1)
    v2 = vertikale(520, 130, space) 
    vertikale_planker.append(v2)
    v3 = vertikale(600, 130, space) 
    vertikale_planker.append(v3)
    v4 = vertikale(680, 130, space) 
    vertikale_planker.append(v4)
    v5 = vertikale(760, 130, space) 
    vertikale_planker.append(v5)
    v6 = vertikale(840, 130, space) 
    vertikale_planker.append(v6)
    v7 = vertikale(360, 130, space) 
    vertikale_planker.append(v7)


