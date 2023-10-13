#Importerer nødvendige biblioteker
import pygame
import sys
import pymunk
import pymunk.pygame_util
from pygame.locals import *
from getworkingpath import *
from pygame_functions import *
import math
import time
from pymunk import Vec2d
from levels import *

"""------------------------------------------------"""
pygame.init() #Starter pygame
pygame.font.init() #Gjør at jeg kan skrive til skjerm
myfont = pygame.font.SysFont('font_angrybirds', 60) #definerer fonten min, som er en custon angrybirds font
background = pygame.image.load(getworkingpath()+"/bakgrunn.jpg") #Loader bakgrunnen
HEIGHT = background.get_size()[1] #høyde på skjermen er lik høyde bakgrunn
WIDTH = background.get_size()[0] #bredde på skjermen er lik høyde bakgrunn
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #pygame display er satt til HEIGHT og WIDTH
pygame.display.set_caption("Angry birds") #Setter overskrift på vinduet
clock = pygame.time.Clock() #definerer clock, bruker time biblioteket
space = pymunk.Space() #space er en funksjon i pymunk. Det funkerer ganske likt som pygame-vinduet, bare at koordinatsystemer er (0,0) nede i venstre hjørne. Man kan også legge til bla gravitasjon 
space.gravity = (0.0, -900.0) #Legger til gravitasjon i space
birds = [] #Liste med fuglene på skjermen
draw_options = pymunk.pygame_util.DrawOptions(screen) #Draw options vil tegne alt som settes inn i pymunk spacet i pygame vinduet
fugl = pygame.image.load(getworkingpath()+"/rødfugl3.png") #Loader bilde av fuglen
katapult_img = pygame.image.load(getworkingpath()+"/katapult.png") #Loader bilde av katapulten
static_fugler = [] #Liste med fugler som ikke flyr
katapult_venstre_koordinater = (190, 475) #Koordinatene til venstre katapult arm
katapult_høyre_koordinater = (210, 475) #Koordinatene til høyre katapult arm
katapult_x = 200 #Midtre x-verdi katapult
katapult_y = 475 #Midtre y-verdi katapult
startposisjon_fugl = (200, 475) #Startpos fugl
angle = 0 #Utskytingsvinkel
mouse_distance = 0 #lengde fra katapult
rope_lenght = 90 #Lengde på strikken man skyter fuglene med
mouse_y = 0 #brukes som koordinater for hvor musen er på skjermen senere
mouse_x = 0 ##brukes som koordinater for hvor musen er på skjermen senere
mouse_pressed = False 
dotted_line = [] #Liste med koordinater til der det skap tegnes hvite prikker. Blir banen til fuglene
antall_fugler = 4 
level_status = 7 #hvilket level
kjør = True #kjør = True som startverdi, da vil hovedloopen starte
total_score = 0 #Total score
bane_score = 0 #Score på aktuell bane
sling_status = False #Skal katapulten virke eller ikke. False = ikke
restart_knapp = pygame.image.load(getworkingpath()+"/button.png") #Loader restart knapp
restart_status = False #Standard, vil ikke restarte gamet hele tiden
resume_knapp = pygame.image.load(getworkingpath()+"/resume.png") #Loader resume knapp
bakgrunn_nedre = pygame.image.load(getworkingpath()+"/nedrebakgrunn.jpg") #Loader nedre del av bakgrunnen for å få det fremst i bildet
pause_knapp = pygame.image.load(getworkingpath()+"/pauseknapp.png") #Loader pause knapp
pause_knapp_koor = 20, 50 #Koordinater til pause knappen
pauseknapp_box = pygame.Rect(20, 50, pause_knapp.get_size()[0], pause_knapp.get_size()[1]) #Definerer et rect til pauseknappen slik at man kan trykke på den senere
skip_knapp = pygame.image.load(getworkingpath()+"/skipbutton.png") #Loader skip knappen
skip_box = pygame.Rect(550, 200, skip_knapp.get_size()[0], skip_knapp.get_size()[1]) #Definerer et rect til skip-knappen slik at man kan trykke på den senere
"""------------------------------------------------"""

#Class bird. Når denne calles vil en fugl tegnes på skjermen.
class Bird():
    def __init__(self, distance, angle, x, y, space): #__init__ gjør at funksjonen caller seg selv
        #Gir fuglen en rekke fysiske verdier
        mass = 5
        radius = 12
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        #Må definere en body til fuglen. Det er slik pymunk biblioteket kan regne ut posisjonen.
        body = pymunk.Body(mass, inertia)
        body.position = x, y #Gir en startposisjon
        power = distance * 53 #Power = avstanden fra fuglen til katapulten, ganget med en konstant som får fuglen til å følge en fin bane
        impulse = power * Vec2d(1, 0) #impulsen fuglen påføres når den blir slengt ut av katapulten. VEC2d er en del av pymunk, som brukes for å regne med vektorer
        angle = -angle #Graden som man skyter ut med måtte være minus den jeg fant ellers vil den skytes feil vei
        body.apply_impulse_at_local_point(impulse.rotated(angle)) #applyer impulsen i en vinkel på fuglen for å skyten den ut fra katapulten. (Gir fuglen en startfart)
        #Pumunk trenger også en shape. Tar variabler som elasitet = hvor mye den vil sprette og friksjon = kraft som virker mot fartsretning.
        shape = pymunk.Circle(body, radius, (0, 0)) 
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1 #Gir fuglen collisjon_type 1. Brukes senere når man skal regne rundt kollisjon mellom fugl og gris
        space.add(body, shape) #Legger til bodyen og shapen i space. Tegner til space
        self.body = body #Self gjør at jeg senere kan skrive f. eks. Bird.body, for å få bodyen til grisen.
        self.shape = shape

#Liten funksjon som tar to punkter og returnerer vekturen mellom den
def vector(p0, p1): 
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return (a, b)

#Funksjon som returnerer en enhetsvektor
def enhetsvektor(v):
    h = math.sqrt((v[0]**2)+(v[1]**2))
    if h == 0:
        h = 0.000000000000001
    ua = v[0] / h
    ub = v[1] / h
    return (ua, ub)

#Regner ut avstanden fra fuglen til katapulten
def distance(xo, yo, x, y):
    dx = x - xo
    dy = y - yo
    d = math.sqrt((dx ** 2) + (dy ** 2))
    return d

#Funksjonen legger til en statisk linje på bakken, gir linjen en body og shape, slik at pymunk vil regne med dette. Fuglene vil ikke gå under bakken: Spretter opp igjen
def add_segment(space):
    global WIDTH
    body = pymunk.Body(body_type = pymunk.Body.STATIC) #Når en body er STATIC i pymunk, betyr det at den ikke beveger seg. De andre bodyene er default kinetic som bla fuglen, plankene og grisen
    body.position = (0, 80) 
    shape = pymunk.Segment(body, (0,0), (WIDTH, 0), 10) 
    shape.elasticity = 0.9
    shape.friction = 1.0
    shape.collision_type = 4 #collisjonstype 4
    space.add(body, shape) # Legger til i pymunk spacen

add_segment(space)

def sling_action():
    #Importerer en rekke globale variabler
    global mouse_distance
    global rope_lenght
    global angle
    global mouse_x
    global mouse_y
    global katapult_høyre_koordinater
    global katapult_venstre_koordinater

    v = vector((katapult_høyre_koordinater[0], katapult_høyre_koordinater[1]), (mouse_x, mouse_y)) #v = vektoren fra punnktet der musen er til det katapulten er

    uv = enhetsvektor(v) #Gjør v om til en enhetsvektor. Dette er for at man ikke skap kunne dra fuglen så langt bak som man vil
    uv1 = uv[0] #uv1 = x-verdien i enhetsvektoren
    uv2 = uv[1] #uv2 = y-verdien i enhetsvektoren

    mouse_distance = distance(katapult_høyre_koordinater[0], katapult_høyre_koordinater[1], mouse_x, mouse_y) #Avstanden fra musen til katapulten

    pu = (uv1*rope_lenght+katapult_høyre_koordinater[0], uv2*rope_lenght+katapult_høyre_koordinater[1]) #pu = pos fugl når lengden fra fuglen til katapulten er større enn lengden på tauet
    bigger_rope = 102 #Den ene delen av katapulten er lengde unna fuglen

    #pos fugl fikses til posisjonen til musen minus 20 i x og y, fordi bildet tegnes oppe i venstre hjærne av fuglen. Gjelder bare når avstanden til katapulten fra musen er mindre enn lengden på tauet
    x_fugl = mouse_x - 20 
    y_fugl = mouse_y - 20

    if mouse_distance > rope_lenght: #hvis man har dratt musen lengde unna en lengden på tauet:
        #Gir posisjonen til fuglen nye verdier, siden den tegnes fra høyre hjørne på bildet. Så tar minus raduisen på y og x
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy #pul er posisjonen der fuglen skal tegnes til skjermen

        pu2 = (uv1*bigger_rope+katapult_høyre_koordinater[0], uv2*bigger_rope+katapult_høyre_koordinater[1]) #pu2 er koordinatet linjen fra katapulten til fuglen skall tegnes til

        pygame.draw.line(screen, (0, 0, 0), (katapult_høyre_koordinater[0], katapult_høyre_koordinater[1]), pu2, 5) #Tegn linje fra katapult høyre arm til fuglen
        screen.blit(fugl, pul) #tegn fuglen, over linjen for å skape dybde
        pygame.draw.line(screen, (0, 0, 0), (katapult_venstre_koordinater[0], katapult_venstre_koordinater[1]), pu2, 5) #Tegn linje fra katapult venstre arm til fuglen
    else:
        mouse_distance += 10 #Setter mouse distance +10 for at linjen skal tegnes på kanten av fuglen, og ikke midt i. Måtte teste litt rundt hva som ble bra.
        pu3 = (uv1*mouse_distance+katapult_høyre_koordinater[0], uv2*mouse_distance+katapult_høyre_koordinater[1]) #Koordinater der fuglen skal tegnes
        pygame.draw.line(screen, (0, 0, 0), (katapult_høyre_koordinater[0], katapult_høyre_koordinater[1]), pu3, 5) #Tegn linje fra katapult høyre arm til fuglen
        screen.blit(fugl, (x_fugl, y_fugl)) #tegn fuglen, over linjen for å skape dybde
        pygame.draw.line(screen, (0, 0, 0), (katapult_venstre_koordinater[0], katapult_venstre_koordinater[1]), pu3, 5)#Tegn linje fra katapult venstre arm til fuglen

    #Regn ut utgangsvinkelen
    dy = mouse_y - katapult_høyre_koordinater[1]
    dx = mouse_x - katapult_høyre_koordinater[0]
    if dx == 0: #sørger for at man ikke deler på 0
        dx = 0.00000000000001  

    angle = math.atan((float(dy))/dx) #Bruker trigonometri for å finne utskytningsvinkelen

    
def to_pygame(p): #Gjør om fra pymunk koordinater til pygame koordinater. tar en pymunk position argument (p, for position)
    return int(p.x), int(-p.y+600)

def draw_dotted_line(): #Funksjonen tegner inn banene til fuglene i 
    global birds #bruker variablen birds, som inneholder fuglene som tegnes til skjerm
    for bird in birds:
        pos = to_pygame(bird.body.position) #Finner posisjonen til der fuglene er
        dotted_line.append(pos) #legger posisjonen til i en liste
    for dot in dotted_line:
        pygame.draw.circle(screen, (255,255,255), (dot[0], dot[1]+50), 5) #Tegner en hvit sirkel hvor hver posisjon som er lagt til i listen



def pause_game(): #Når man trykker ESC eller pause-knappen vil dette kjøre (pause spillet)
    #Tar en rekke globale variabler
    global total_score
    global kjør
    global WIDTH
    global HEIGHT
    global mouse_pressed
    global total_score
    global bane_score
    global restart_knapp
    global resume_knapp

    pause = True #Setter pause = True, da kjører loopen
    pos_x = 540 #posisjon til x-posisjonen til der knappene skal tegnes
    pos_y= 200 #posisjon til y-posisjonen til der knappene skal tegnes
    box_resume = pygame.Rect(pos_x, pos_y + 100, resume_knapp.get_size()[0], resume_knapp.get_size()[1]) #Lager et pygame rect for resume knappen
    box_restart = pygame.Rect(pos_x, pos_y, restart_knapp.get_size()[0], restart_knapp.get_size()[1]) #Lager et pygame rect for restart knappen
    while pause:
        for event in pygame.event.get():
            if event.type == QUIT: #Hvis man trykker kryss
                sys.exit(0) #slutter programmet
            elif event.type == KEYDOWN and event.key == K_ESCAPE: #hvis man trykker ned ned esc key
                pause = False #Slutt på pause
            elif box_resume.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]: #Hvis man trykker på pauseknappen
                mouse_pressed = False #Setter mouse pressed til false for at det ikke skal henge opp noe annet i koden
                pause = False #slutt på pause
            elif pygame.mouse.get_pressed()[0] and box_restart.collidepoint(pygame.mouse.get_pos()): #hvis man trykker på restart knappen
                total_score -= bane_score
                level_restart(space) #kjører level_restart funksjonen jeg har laget lengre ned
                pause = False #Slutt på pause

        text = myfont.render("Dine totale score er: " + str(total_score) , False, (0, 0, 0)) #lager en sort tekst 
        screen.blit(text, (10,10)) #Tegner teksten til skjermen
        text2 = myfont.render("Dine score på banen er: " + str(bane_score) , False, (0, 0, 0)) #lager en sort tekst 
        screen.blit(text2, (10,130)) #Tegner teksten til skjermen
        screen.blit(restart_knapp, (pos_x, pos_y)) #tegner restart knapp til skjerm
        screen.blit(resume_knapp, (pos_x, pos_y+100)) #tegner resume knapp til skejrm
        pygame.display.flip() #tegner tingene til skejrmen

def resultat(): #Funksjonen skal kjøres når en bane er ferdig
    #Trenger noen variabler
    global skip_box
    global skip_knapp
    global level_status
    global restart_knapp
    global bane_score
    global total_score

    resultat = True #Setter resulatat til True for å kjøre loopen
    box_restart = pygame.Rect(550, 280, restart_knapp.get_size()[0], restart_knapp.get_size()[1]) #Lager en pygame.Rect for restartknappen
    while resultat:
        for event in pygame.event.get():
            if event.type == QUIT:#Hvis man trykker kryss
                sys.exit(0)#slutter programmet
            elif pygame.mouse.get_pressed()[0] and skip_box.collidepoint(pygame.mouse.get_pos()): #hvis man trykker på skip knappen
                level_status +=1  #level_status + 1, da kjøres neste level
                level_restart(space) #Slett det som er på skjermen og kjør levelet
                resultat = False #Avslutt loopen
            elif pygame.mouse.get_pressed()[0] and box_restart.collidepoint(pygame.mouse.get_pos()): #hvis man trykker på restart knappen
                total_score -=bane_score
                level_restart(space) #Slett det som er på skjermen, og kjør levelet på nytt
                resultat = False #Avslutt loopen
        screen.blit(restart_knapp, (550, 280)) #Tegn restart knapp til skjerm
        screen.blit(skip_knapp, (550, 200)) #Tegn skip knapp til skjerm
        pygame.display.flip() #Tegner tingene til skjermen
                

def level_restart(space): #Funksjonen fjerner alt som er på skejrmen og loader levelet på nytt
    #Bruker noen globale variabler
    global birds
    global pigs
    global horisontale_planker
    global vertikale_planker
    global dotted_line
    global antall_fugler
    global total_score
    global bane_score


    bane_score = 0 #Setter scoren på banen til 0

    antall_fugler = 4 #Refresher antall fugler
    dotted_line.clear() #Fjerner fuglebanene

    #Lager lister med tingene som skal slettes fra skjermen
    pig_del = []
    bird_del = []
    vplanker_del = []
    hplanker_del = []

    
    for pig in pigs: #Legger til elementene som skal slettes i liste
        pig_del.append(pig)
    for pig2 in pig_del: #Sletter elementene i listen fra listen og fra spacen
        pigs.remove(pig2)
        space.remove(pig2.shape, pig2.shape.body)

    #Samme som over
    for bird in birds:
        bird_del.append(bird)
    for bird2 in bird_del:
        space.remove(bird2.shape, bird2.shape.body)
        birds.remove(bird2)
    #Samme
    for v_planker in vertikale_planker:
        vplanker_del.append(v_planker)
    for v_planker2 in vplanker_del:
        space.remove(v_planker2.shape, v_planker2.shape.body)
        vertikale_planker.remove(v_planker2)
    #Samme
    for h_planker in horisontale_planker:
        hplanker_del.append(h_planker)
    for h_planker2 in hplanker_del:
        space.remove(h_planker2.shape, h_planker2.shape.body)
        horisontale_planker.remove(h_planker2)
    level() #Loader nytt level

def endgame():
    global total_score
    global bane_score
    global restart_knapp
    global level_status
    global background
    endgame = True
    box_restart = pygame.Rect(550, 200, restart_knapp.get_size()[0], restart_knapp.get_size()[1])
    while endgame:
        for event in pygame.event.get():
            if event.type == QUIT: #Hvis man trykker kryss
                sys.exit(0) #slutter programmet
            elif pygame.mouse.get_pressed()[0] and box_restart.collidepoint(pygame.mouse.get_pos()): #hvis man trykker på restart knappen
                level_status = 1
                bane_score = 0
                total_score = 0
                level_restart(space) #kjører level_restart funksjonen jeg har laget lengre ned
                endgame = False #Slutt på endgame
        screen.blit(background, (0,0))
        text = myfont.render("Du fikk: " + str(total_score) + ' poeng', False, (0, 0, 0))
        screen.blit(text, (400, 120))
        text2 = myfont.render("Trykk på restart knappen for å prøve på nytt", False, (0, 0, 0))
        screen.blit(text2, (200, 160))
        screen.blit(restart_knapp, (550, 200))
        pygame.display.flip()

def distance_to_startpos(): #Regner ut avstanden til fuglens startposisjonen far musen
    global mouse_x
    global mouse_y
    katapult_koor = (200,470)
    
    delta_x = abs(mouse_x-katapult_koor[0])
    delta_y = abs(mouse_y-katapult_koor[1])
    avstand = int(math.sqrt(delta_x**2 + delta_y**2))
    return avstand #Return avstanden

def draw_static_birds(): #Tegner fuglene som venter i linje
    global antall_fugler
    global fugl
    for i in range (0, antall_fugler - 1): #Kjør for loopen antallfuglen minus en gang. I dette tilfellet er antall fugler 4, så kjøres 3 ganger
        screen.blit(fugl, (130 - i*40, 523)) #Tegner fugl i gitte koordinater. Avstand 40 mellom hver fugl

def draw_birds(): #Tegner fuglene til posisjonen til fuglen i space
    global birds
    global fugl
    for yeet in birds:
        pos_x = yeet.body.position.x
        pos_y = yeet.body.position.y
        screen.blit(fugl, (pos_x-20, -pos_y + 630))

def draw_pigs(): #Tegner grisene til posisjonen til fuglen i space
    global pigs
    global pig
    for yeet in pigs:
        pos_x = yeet.body.position.x
        pos_y = yeet.body.position.y
        screen.blit(pig, (pos_x-20, -pos_y + 620))


def level(): #Funksjonen sjekker hvilket level som skal kjøres, og kjører det.
    global level_status
    if level_status == 1:
        level1(space)
    elif level_status == 2:
        level2(space)
    elif level_status == 3:
        level3(space)
    elif level_status == 4:
        level4(space)
    elif level_status == 5:
        level5(space)
    elif level_status == 6:
        level6(space)
    elif level_status > 6:
        endgame() 
level() #Kjører det første levelet en gang


def kollisjon_bird_pig(arbiter, space, data): #Lager en collison hander mellom fugl og gris, så hvis det er kollisjon vil loopen kjøre
    global total_score 
    global bane_score
    
    bane_score += 10000 #Legger til score til banescore
    total_score += 10000 #Legger til score til totalscoren
    a, b = arbiter.shapes #sjekker hvilken shape som blir truffet. b, vil her være grisen
    body = b.body # setter b, er shape for gris lik body gris
    pigs_del = [] #Liste med griser som skal fjærnes
    for pig in pigs:
        if body == pig.body: #Side det er flere griser i spacet, må man finne riktig gris, og legge det til i listen
            pigs_del.append(pig)
            pigs.remove(pig)
        for pig2 in pigs_del: #Fjerner grisene fra space og listen med grisene
            space.remove(pig2.shape, pig2.shape.body)


def kollisjon_bird_planker(arbiter, space, data):
    planker_del = [] #Liste med planker som skal fjernes
    if arbiter.total_impulse.length > 1200: #hvis impulsen mellom fugl og planke når de kolliderer er over 1200
        a, b = arbiter.shapes #Sjekker hvilken shape det er som blir truffet, b er shape for planken
        space.remove(b, b.body) #Fjerner gjeldene shape fra space
        for i in vertikale_planker: #Sjekker gjennom de vertikale plankene
            if b == i.shape:#Sjekker om det er en shape i vertikale planker
                planker_del.append(i) #Legger til i listen med planker som skal fjernes
        for j in horisontale_planker:#Sjekker gjennom de horisontale plankene
            if b == j.shape:#Sjekker om det er en shape i horisontale planker
                planker_del.append(j) #Legger til i listen med planker som skal fjernes
        for poly in planker_del: #Sjekker gjennom de plankene som skal fjærnes
            #Fjærner fra enten de vertikale eller horisontale plankene basert på hvilke blir truffet
            if poly in vertikale_planker:
                vertikale_planker.remove(poly)
            if poly in horisontale_planker:
                horisontale_planker.remove(poly)
        global total_score 
        global bane_score
        total_score += 5000 #Legger til score
        bane_score += 5000 #Legger til total score



def kollisjon_pig_planker(arbiter, space, data):
    global pigs
    a, b = arbiter.shapes #Sjekker hvilken shape som blir truffet
    pig_del = [] #Liste med fugler som skal slettes
    if arbiter.total_impulse.length > 800: #Hvis impulsen er over 800 i støttet
        for pig in pigs: #Sjekker gjennom listen med fugler
            if a == pig.shape: #Hvis shapen er en av grisene
                pig_del.append(pig)  #Legg til i grisene som skal slettes
        for pig2 in pig_del: #Sletter grisene fra listen og space
            space.remove(pig2.shape, pig2.shape.body)
            pigs.remove(pig2)



def kollisjon_pig_bakke(arbiter, space, data):
    global pigs
    a, b = arbiter.shapes #Får hvilken shape som blir truffet
    pig_del = [] #Liste med griser som skal fjærnes
    if arbiter.total_impulse.length > 1400: #Hvis impulsen is støtet er mer enn 1400
        for pig in pigs: #Sjekker gjennom lsiten med griser
            if b == pig.shape: #Sjekker hvilken gris har shape lig den som blir truffet
                pig_del.append(pig) #Legger til i listen som skal slettes
        for pig2 in pig_del: #Sletter grisen fra listen med griser og space
            space.remove(pig2.shape, pig2.shape.body)
            pigs.remove(pig2)

space.add_collision_handler(1, 2).post_solve=kollisjon_bird_pig #Legger til collision handler mellom gris og fugl i space
space.add_collision_handler(1, 3).post_solve=kollisjon_bird_planker #Legger til collision handler mellom gris og planke i space
space.add_collision_handler(2, 3).post_solve=kollisjon_pig_planker #Legger til collision handler mellom fugl og planke i space
space.add_collision_handler(4, 2).post_solve=kollisjon_pig_bakke #Legger til collision handler mellom fugl og bakke i space


        
            



while kjør: #Hovedloopen, kjører når kjør==True
    #Kjører noen funksjoner i starten
    distance_to_startpos() 
    screen.blit(background, (0,0)) #Tegner bakgrunn
    draw_static_birds()
    draw_dotted_line()
    screen.blit(katapult_img, (150, HEIGHT-190)) #Tegner katapult
    screen.blit(pause_knapp, pause_knapp_koor) #Tegner pauseknapp
    mouse_x, mouse_y = pygame.mouse.get_pos() #Finenr mouse pos x og y, bed pygame innebygd funksjon pygame.mouse.get_pos()

    for event in pygame.event.get(): #Event in pygame
        if event.type == QUIT: #Hvis man trykker på kryss
            sys.exit(0) #Slutt programmet
        
        elif (pygame.mouse.get_pressed()[0] and sling_status == False and distance_to_startpos() < 20 and antall_fugler > 0): #hvis man trykker på fuglen i katapulten
            mouse_pressed = True
            sling_status = True #Slynge == True betyr katapulten skal kjøres

        elif (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_pressed): #Hvis man slipper fuglen, skal fuglen skytes
            mouse_pressed = False
            xo = 200 #x for utganspos
            yo = 170 #y for utganspos
            antall_fugler -=1 #minus 1 antall fugler
            if mouse_distance > rope_lenght:  #Mouse distance skal ikke være større enn tauet, for å få riktig kraft
                mouse_distance = rope_lenght 
            if mouse_x < katapult_høyre_koordinater[0] + 5: #Måtte skille mellom hvor musen var for at den skulle skytes i riktig retning
                bird = Bird(mouse_distance, angle, xo, yo, space) #Tegner en fugl til space
                birds.append(bird) #Legger til denne fuglen i listen med fugler
            else:
                bird = Bird(-mouse_distance, angle, xo, yo, space) #Tegner en fugl til space
                birds.append(bird) #Legger til denne fuglen i listen med fugler
            sling_status = False #Etter katapulten har skutt blir den igjen passiv
        elif event.type == KEYDOWN and event.key == K_ESCAPE:#Hvis man trykker på ESC, skal gamet pause
            pause_game()
            mouse_pressed = False
        elif pygame.mouse.get_pressed()[0] and pauseknapp_box.collidepoint(pygame.mouse.get_pos()): #Hvis man trykker på pause knappen, skal gamet pause
            pause_game()
            mouse_pressed = False


    if sling_status: #hvis sling_status == True skal fuglen dras mot musen
        sling_action()

    elif sling_status == False and antall_fugler > 0: #Hvis katapulten er passiv og det er flere fugler, skal det tegnes en fugl i startposisjonen
        screen.blit(fugl, (180, 455)) 
       
    mouse_pos_converted = (int(mouse_x), int(-mouse_y+644)) #Mouse posisjon i pymunk koordinater
    
    text1 = myfont.render('total score: ' + str(total_score) , False, (0, 0, 0)) #text1 er lik totalscore 
    screen.blit(text1, (0, 0)) #tegn teksten til skjerm
    text2 = myfont.render("bane score: " + str(bane_score) , False, (0, 0, 0)) #lager en sort tekst 
    screen.blit(text2, (0,130)) #Tegner teksten til skjermen

    if len(pigs) == 0: #hvis det er 0 griser igjen, skal resultatvinduet poppe opp
        resultat()
    
    space.debug_draw(draw_options) #Tegner alle pymunk objektene til pygame vinduet
    draw_birds() #Tegn fuglene
    draw_pigs() #Tegn grisene
    screen.blit(bakgrunn_nedre, (0,555)) #Tegn nedre del av bakgrunne, siden dette skal være over linjen i pymunk, må dette være etter man tegner pymunk objektene
    space.step(1/50.0) #Oppdateres space 50 ganger i sekundet
    pygame.display.flip() #Tegner alle pygame objektene
    clock.tick(50) #Oppdaterer pygame vinduet 50 ganger i sekundet
    pygame.display.set_caption("Angry birds     FPS: " + str(clock.get_fps())) #Setter en overskrift som viser FPSen