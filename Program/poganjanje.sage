import json

seconds = time.time()
st=2
print(st)
nn=20
res = []
for i in range(st,nn):
    ar=[]
    cas=0
    for j in range(3):
        seconds = time.time()
        a = Metoda ()
        a.postavi_polje(i)
        a.ustvari_daljice_v2(i)
        a.seka(a.daljice[0],a.daljice[1])
        b=a.program(i)
        ar.append(b)
     
        seconds1 = time.time()
        cas +=  seconds1-seconds
        
    mm= max(ar)
    print (str(i), "-daljic",str(   "presecisc "),str(   mm ),"   C: ", str(float(mm/sqrt(i))), "cas: ", cas/ (3))
    res.append((int(i), float(mm), float(cas)))
    with open("poganjanje-%d.json" % nn, "w") as f:
        json.dump(res, f)
