# Sytème solaire - Version 2 - 2014

from time import *
from tkinter import *
from math import *

#-------------------------------------------------------------------------
# variables globales
#-------------------------------------------------------------------------

# fenetre
#----------------------------------------
width = 600 #taille fenetre
scale = 20*width *1/(10**13) #echelle

state = False #play/stop = true/false

# constantes cosmoligique
#----------------------------------------
G = 6.67384*10**(-11) #N.m**2.kg**-2
t = 0 #unit : second
dt = 10**(2)  #unit : second

#-------------------------------------------------------------------------
# fonctions et classes
#-------------------------------------------------------------------------

# preliminaires : operations vectueurs
#----------------------------------------

def sum_vect(v1,v2):
    return [v1[0]+v2[0],v1[1]+v2[1],v1[2]+v2[2]]

def int_x_vect(integer,vecteur):
    return [integer*vecteur[0],integer*vecteur[1],integer*vecteur[2]]

def er_to_cart(vecteur): #convertion des coordonnées cylindriques en coordonnées cartésiennes
    return [vecteur[0]*cos(vecteur[1]),
                        vecteur[0]*sin(vecteur[1]),
                        vecteur[2]]

def e0_to_cart(vecteur): #convertion des coordonnées cylindriques en coordonnées cartésiennes
    return [vecteur[0]*-1*sin(vecteur[1]),
                        vecteur[0]*cos(vecteur[1]),
                        vecteur[2]]

# classe : definition astre
#----------------------------------------

class star ():

    def __init__(self,m,X,V,A): #X,V & A vecteurs
        self.name = "astre"
        self.color = "black"
        self.m = m
        self.X = X
        self.V = V
        self.A = A

    def __str__(self):
        return "#%s------------------------\nmasse : %f\nposition : (%f,%f,%f)\nvitesse : (%f,%f,%f)\nacceleration : (%f,%f,%f)" % (self.name,self.m,self.X[0],self.X[1],self.X[2],self.V[0],self.V[1],self.V[2],self.A[0],self.A[1],self.A[2])

    def distance(self,other_astre):
        return ((self.X[0]-other_astre.X[0])**2 +
                (self.X[1]-other_astre.X[1])**2 +
                (self.X[2]-other_astre.X[2])**2 )**(1/2)

    def axe(self,other_astre):
        norme = self.distance(other_astre)
        return int_x_vect(1/norme,sum_vect(self.X,int_x_vect(-1,other_astre.X)))

    def force(self,other_astre):
        k = G*self.m*other_astre.m/self.distance(other_astre)**2
        vecteur = int_x_vect(k,self.axe(other_astre))
        return int_x_vect(-1,vecteur)

    def new_position(self,sum_forces,dt):
        self.A = int_x_vect(1/self.m,sum_forces)
        self.V = sum_vect(self.V,int_x_vect(dt,self.A))
        self.X = sum_vect(self.X,int_x_vect(dt,self.V))

    
# mouvement astre
#----------------------------------------

def mouvement(liste,dt):
    new_liste = liste[:]
    for astre_i in new_liste :
        forces = [0,0,0]
        for astre_j in liste :
            if astre_i != astre_j :
                forces = sum_vect(forces,astre_i.force(astre_j))
        astre_i.new_position(forces,dt)
    return new_liste

def print_info(liste,t,dt):
    n = int(t/dt)
    for i in range (n):
        liste = mouvement(liste,dt)

# fenêtre
#----------------------------------------

def changement_repere(vecteur,echelle):
    [x_vect,y_vect,z_vect] = int_x_vect(echelle,vecteur)
    return [x_vect+width/2,width/2-y_vect,z_vect]

def draw_stars(canvas,liste,echelle):
    canvas.delete(ALL) 
    for astre in liste :
        [x,y,z] = changement_repere(astre.X,echelle)#position
        [xt0,yt0,zt0] = er_to_cart([2**.5*astre.distance(sun),3/4*pi,0])#trajectoire
        [xt1,yt1,zt1] = changement_repere([xt0,yt0,zt0],echelle)#trajectoire
        [xt2,yt2,zt2] = changement_repere(int_x_vect(-1,[xt0,yt0,zt0]),echelle)#trajectoire
        canvas.create_oval(xt1,yt1 ,xt2 ,yt2 , fill="white") #trajectoire
        canvas.create_oval(x-5,y-5 ,x+5 ,y+5 , fill=astre.color) #ATTENTION : changement de repère
        canvas.create_text(x+10,y+10,text=astre.name)
        temps['text']="jour(s) : "+str(int(t/(24*3600)*10)/10)

def iteration (canvas,dt,echelle) :
    global state,systeme_solaire,t
    if state :
        for i in range (1000):
            t += dt
            systeme_solaire = mouvement(systeme_solaire,dt)
        draw_stars(canvas,systeme_solaire,echelle)
        canvas.after(50, lambda : iteration(canvas,dt,echelle))
        
def run (canvas,dt,echelle):
    global state 
    state = True
    iteration(canvas,dt,echelle)
        
def stop () :
    global state
    state = False

#-------------------------------------------------------------------------
# Programme
#-------------------------------------------------------------------------


# astres systeme solaire (initial au 6avril2016)
#----------------------------------------
sun = star(1.989*10**30,[0,0,0],[0,0,0],[0,0,0])
sun.name = "sun"
sun.color = "yellow"
mercure = star(330.2*10**21,er_to_cart([57909176*10**3,340.5/360*2*pi,0]),e0_to_cart([(G*sun.m/(57909176*10**3))**(1/2),340.5/360*2*pi,0]),[0,0,0])
mercure.name = "mercure"
venus = star(4.8685*10**24,er_to_cart([108208930*10**3,243.02/360*2*pi,0]),e0_to_cart([(G*sun.m/(108208930*10**3))**(1/2),243.02/360*2*pi,0]),[0,0,0])
venus.name = "venus"
earth = star(5.972*10**24,er_to_cart([149597887.5*10**3,102.76/360*2*pi,0]),e0_to_cart([(G*sun.m/(149597887.5*10**3))**(1/2),102.76/360*2*pi,0]),[0,0,0])
earth.name = "earth"
earth.color = "blue"
mars = star(641.85*10**21,er_to_cart([227936637*10**3,125.21/360*2*pi,0]),e0_to_cart([(G*sun.m/(227936637*10**3))**(1/2),125.21/360*2*pi,0]),[0,0,0])
mars.name = "mars"
jupiter = star(1.8986*10**27,er_to_cart([778412027*10**3,77.39/360*2*pi,0]),e0_to_cart([(G*sun.m/(778412027*10**3))**(1/2),77.39/360*2*pi,0]),[0,0,0])
jupiter.name = "jupiter"
saturne = star(568.46*10**24,er_to_cart([1429394069*10**3,158.8/360*2*pi,0]),e0_to_cart([(G*sun.m/(1429394069*10**3))**(1/2),158.8/360*2*pi,0]),[0,0,0])
saturne.name = "saturne"
uranus = star(8.681*10**25,er_to_cart([2870658186*10**3,288.04/360*2*pi,0]),e0_to_cart([(G*sun.m/(2870658186*10**3))**(1/2),288.04/360*2*pi,0]),[0,0,0])
uranus.name = "uranus"
neptune = star(102.43*10**24,er_to_cart([4503443661*10**3,246.83/360*2*pi,0]),e0_to_cart([(G*sun.m/(4503443661*10**3))**(1/2),246.83/360*2*pi,0]),[0,0,0])
neptune.name = "neptune"

systeme_solaire = [neptune,uranus,saturne,jupiter,mars,earth,venus,mercure,sun]


# fenêtre
#----------------------------------------
window=Tk()

canvas = Canvas(window,width = width, height = width, bg="white")
temps = Label(window,text="jour(s) : 0")
button_run = Button(window, text="Run", command = lambda : run (canvas,dt,scale))
button_stop = Button(window, text="Stop", command = stop)
button_quit = Button(window, text="Quitter", command=window.quit)

temps.pack()
canvas.pack()
button_run.pack()
button_stop.pack()
button_quit.pack()

window.mainloop()
window.destroy()
