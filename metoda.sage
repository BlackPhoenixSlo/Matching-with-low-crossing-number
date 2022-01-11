#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Cilj je narest probram k bo ustvaril n tock in zracunal koliko je najvecje stavilo k presecisc ene premice  vsemi daljicami.
from random import randint
import math
import time
#seconds = time.time()
#print("Zacetek programa: ", seconds)	



###############################
#Metoda je klass kjer je napisan algoritem za izracunavo c 
class Metoda : 
    #stevilo_pik _ default
    n=5
    #sirina_okvirja _ default
    sirina=100 

    ############################
    # postavimo vse parametre 
    polje= [] #polje tock
    tocke=[] #arraj za permutacijo daljic
    daljice=[] #trenutna permutacija na kateri racunam
    ar_daljice=[] #vse mozne permutacije daljic

    ############################
    #postavi random tocko v polje z sirino width
    def random_tocka(self,width, krog=False):
        if krog==True:
            return self.random_tocka_v_krogu(width)

        i = randint(0,width)
        j = randint(0,width)
        return i,j

    ############################
    #postavi random tocko v krog z polmerom width/2
    def random_tocka_v_krogu(self,width):
        i = randint(0,width)
        j = randint(0,width)
        w = width / 2
        ps = math.sqrt(j*j + (w-i)*(w-i))
        while (ps > w):
            j = randint(0,width)
            ps = math.sqrt(j*j + (w-i)*(w-i))
        return i,j

    ############################
    # to tocko zapisemo v array
    def dodaj_tocko(self,i,j):
    
        self.polje.append([i,j])
    
    def pobrisi_polje(self):
        self.polje = []
        #print(self.polje)

    def izpisi_polje (self):
        #print(self.polje)
        pass

    ############################
    # Z pomocjo zgornih funkcij zapise v arraj 2n tock
    def postavi_polje(self,stevilo_pik= 5, sirina_okvirja=100,krog=False): ## tu dodaj parametre

        self.pobrisi_polje()
        stevilo_pik *= 2

        for _ in range(stevilo_pik) :
            #self.izpisi_polje()

            i,j = self.random_tocka(sirina_okvirja,krog)
            while [i,j] in Metoda.polje :
                i,j = self.random_tocka(sirina_okvirja,krog)
            self.dodaj_tocko(i,j)
        #self.izpisi_polje()


    ############################
    
    #Matriko naredi za presek premice in daljice
    #vzemi 2 točke na premici in eno na daljici 
    #vzemi 2 tocke na premico in eno na dalciji (tadrugo)
    #rabita ime nasprotni prednak
    
    def seka(self,l,d):
        #print (l)
        x = l[0]
        y = l[1]
        z1 = d[0]
        z2 = d[1]
        #print(self.polje[x][0])
        #print(self.polje[x][1])
        #print()
        #print()
        
        D1=matrix(SR, 3, [self.polje[x][0],self.polje[x][1],1,self.polje[y][0],self.polje[y][1],1,self.polje[z1][0],self.polje[z1][1],1])
        D2=matrix(SR, 3, [self.polje[x][0],self.polje[x][1],1,self.polje[y][0],self.polje[y][1],1,self.polje[z2][0],self.polje[z2][1],1])
        
        #print(D1)
        #print(D1.det())
        #print(D2)
        #print(D2.det())
        if D2.det() * D1.det() < 0 :
            return true 
        else:
            return false
        
    
    
    def ustvari_daljice_v2 (self,n):
        self.daljice = [Set([i,j]) for i in range(2*n) for j in range(i+1, 2*n)] 
        
    
    def program (self,n=5):
        p = MixedIntegerLinearProgram(maximization = False)
        
        
        x=p.new_variable(binary=True)

        p.set_objective(p["t"])

        for i in range(2*n): 
            p.add_constraint(sum(x[Set([i,j])] for j in range(2*n) if i != j) == 1)

        for l in self.daljice :
            p.add_constraint(sum(x[d] for d in self.daljice if self.seka(l,d)) <= p["t"] )

           # ({3,4}, set([5,6]))
        #print (p.get_values(x)) # vrne vrednost x a)
        a = p.solve()
        #print (a) # vrne vrednost t ja
        return a
