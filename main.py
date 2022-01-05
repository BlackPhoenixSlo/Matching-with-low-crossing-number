#Cilj je narest probram k bo ustvaril n tock in zracunal koliko je najvecje stavilo k presecisc ene premice  vsemi daljicami.
from random import randint
import math
import time
seconds = time.time()
print("Zacetek programa: ", seconds)	


###############################
#Funkcija izvede vse mozne permutacije daljic na po_tockah
#znacilno je da vrne le en zacetek dalcij iz vu 
def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                
                a=indices[:r]
                dd=True
                for p in range(len(a)/2):
                    if a[p*2] > a[p*2+1] :
                        dd=False
                if dd:
                    yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

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
        print(self.polje)

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

    def array_tock_daljic(self,stevilo_pik=5):
        self.tocke=[]
        for i in range(stevilo_pik*2):
            self.tocke.append(i)
        #print (self.tocke)

    ############################
    # S pomocjo zgornjih funkcij razporedi tocke v daljice 
    def ustvari_daljice(self,tock):
        if len(tock) == len(self.tocke) :
            self.daljice =[] 
        if len(tock) == 0:
            return


        i = randint(0,len(tock)-1)
        
        j = randint(0,len(tock)-1)
        while j ==i :
            j = randint(0,len(tock)-1)
        
        self.daljice.append((tock[i],tock[j]))

        copy_tocke= list(tock)
        
        copy_tocke.remove(tock[j])
        copy_tocke.remove(tock[i])

        self.ustvari_daljice(copy_tocke)

    ############################
    # Zracunam koeficiente premice
    def koeficienti_funkcije(self,x1,y1,x2,y2):
        if x2 == x1:
            return False,x1
        k1 = (y2-y1)/(x2-x1)
        n1 = y1 - k1 * x1
        return k1,n1

    ############################
    # Zracunam preseke premic
    def presek_premic(self,x1,y1,x2,y2): #podane so 4 tocke
       
        
        xx1 , yy1 = x1
        xx2 , yy2 = y1
        #print("1")
        #print(x1 , y1)
        k1, n1 = self.koeficienti_funkcije(xx1,yy1,xx2,yy2)
        
        xx1 , yy1 = x2
        xx2 , yy2 = y2
        #print("2")
        #print(x2 , y2)
        k2, n2 = self.koeficienti_funkcije(xx1,yy1,xx2,yy2)

        
        if k1 == k2  or k1 == False or k2 == False:
            return False, False
        #print (k1,k2)
        x = (n2-n1)/(k1-k2)
        y = k1 * x + n1 
        #print("xy")
        #print (x,y)
        return x,y

    ############################
    # pogledam ali je presec 2h premic znotraj daljice
    def ali_je_presek_v_daljici (self,x,y,x1,y1,x2,y2):
        #print(x,y,x1,y1,x2,y2)
        if (x>=x1 and x<=x2 and y>=y1 and y<=y2) or (x>=x1 and x<=x2 and y<=y1 and y>=y2) or (x<=x1 and x>=x2 and y>=y1 and y<=y2) or (x<=x1 and x>=x2 and y<=y1 and y>=y2):
            return True
        else:
            return False

    #########################
    # generator premic
    def ustvari_premice(self,stevilo_pik):
        for i in range(stevilo_pik*2):
            for j in range(i+1,stevilo_pik*2): 
                yield self.polje[i] , self.polje[j] # vraca tocke ene premice
    
    ############################
    # S pomocjo zgornjih 5 funkcij ugotovim koliko daljic seka moja mnozica premice
    def koliko_daljic_seka_premica(self,x1,y1):
        count = 0
        for i in self.daljice :
            x2,y2 = i 
            x2,y2 = self.polje[x2], self.polje[y2]
            x,y = self.presek_premic( x1,y1,x2,y2)
            
            if  x and  y :
                #print(x,y)
                if self.ali_je_presek_v_daljici(x,y,x2[0],x2[1],y2[0],y2[1]) :
                    count +=1
        return count

    ############################
    # z uporabo zgornjih funkcij in generatorja, ponovim za vse metode
    def najvec_presecisc_vseh_premic(self,st_tock):
        count = 0
        simple_generator = self.ustvari_premice(st_tock)
        for x1,y1 in simple_generator:
            x = self.koliko_daljic_seka_premica(x1,y1)
            if x > count :
                count = x
        return count
    
    ############################
    # Glavna metoda za zapis podatkov in zdruzevanje celega poteka izvajanja na eni metodi
    def min_presecisc_po_razporedu_daljic_z_maz_presekom_premice(self, stevilo_pik= 5,krog=False):
        self.postavi_polje(stevilo_pik=stevilo_pik,krog=krog)
        #self.izpisi_polje()
        self.array_tock_daljic(stevilo_pik)
        #print(self.tocke)
        min_count = stevilo_pik
        
        if len(self.ar_daljice) < stevilo_pik-2 :
            
            cas1= time.time()
            self.ar_daljice.append( list(permutations(range(stevilo_pik*2))))
            cas2= time.time()
            print("Casovna poraba za izracun n="+str(stevilo_pik*2)+" permutacij je: " + str(cas2 - cas1) + " sekund.")


        for permutacija in self.ar_daljice[stevilo_pik-3]:
            #print(permutacija)
            self.daljice=[]
            for i in range(stevilo_pik):
                self.daljice.append((permutacija[i*2],permutacija[i*2+1]))


            ###############################
            # Opcija ce zelimo najljucno generirati daljice    
            #self.ustvari_daljice(self.tocke)
        

            
            
            count =self.najvec_presecisc_vseh_premic(stevilo_pik)
            if count < min_count:
                min_count = count
           
            #print(min_count)
            
        return min_count

    ############################
    # malo igranja z permutacijami in racunanja casovne razlike
    def brisi_permutacije(self,stevilo_pik):
        
        for per in self.ar_daljice:
            for i in range(stevilo_pik):
                
                if per[i*2] > per[i*2+1]:
                    #print(per)
                    self.ar_daljice.remove(per)
                    break
        print(len(self.ar_daljice))
        





a = Metoda ()

n=30
start=3
ponovitve=3

ar_krog=[]
ar_kvadrat=[]
######
#klicem izvedbo funkcij
for i in range(start,n):


    arr=[]
    cas_n1 = time.time()
    cas_kv1= time.time()
    for _ in range(ponovitve):
        
        cas1= time.time()
        arr.append(a.min_presecisc_po_razporedu_daljic_z_maz_presekom_premice(stevilo_pik=i, krog=False))
        cas2= time.time()
        print("Casovna poraba za izracun po n="+str(i*2)+" tockah v kvadratu je: " + str(cas2 - cas1) + " sekund.")
        #print (str(i)+ ": kvadrat: "+ str(max(arr))+" - C= "+str(max(arr)/math.sqrt(i)))
    cas_kv2= time.time()
    print("Povpracna Casovna poraba za izracun po n="+str(i*2)+" tockah v kvadratu je: " + str(cas_kv2/ponovitve - cas_kv1/ponovitve) + " sekund.")
    
    

        
    ar_kvadrat.append(arr)
   
    arr=[]
    cas_kr1= time.time()
    for _ in range(ponovitve):
        cas1= time.time()

        arr.append(a.min_presecisc_po_razporedu_daljic_z_maz_presekom_premice(stevilo_pik=i, krog=True))
        cas2= time.time()
        print("Casovna poraba za izracun po n="+str(i*2)+" tockah v krogu je: " + str(cas2 - cas1) + " sekund.")
        #print (str(i)+ ": krog: "+ str(max(arr))+" - C= "+str(max(arr)/math.sqrt(i)))
    cas_kr2= time.time()
    print("Povpracna Casovna poraba za izracun po n="+str(i*2)+" tockah v krogu je: " + str(cas_kr2/ponovitve - cas_kr1/ponovitve) + " sekund.")

    ar_krog.append(arr)

    cas_n2 = time.time()
    print("Casovna poraba za izracun po n="+str(i*2)+" tockah v kvadratu z "+str(ponovitve)+" ponovirvami kvadra in kroga je: " + str(cas_n2 - cas_n1) + " sekund.")

    print (str(i)+ ": kvadrat: "+ str(max(ar_kvadrat[i-start]))+" - C= "+str(max(ar_kvadrat[i-start])/math.sqrt(i))+ "<-> krog: " + str(max(ar_krog[i-start])) +" - C= "+str(max(ar_krog[i-start])/math.sqrt(i)))
    print(ar_kvadrat, ar_krog)


print(ar_kvadrat, ar_krog)
for i in range(len(ar_kvadrat)):
    print (str(i+start)+ ": kvadrat: "+ str(max(ar_kvadrat[i]))+ "<-> krog: " + str(max(ar_krog[i])) )
