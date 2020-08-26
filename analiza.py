import pandas as pd

#najprej bo potrebnega nekaj čiščenja cene so oblike €...M ali pa celo string

path = 'C:\\Users\\marsovc\\Desktop\\Fmf\\Dodiplomsko\\Financna 3. letnik\\Programiranje 1\\Projektna-naloga-PROG1\\podatki\\'

#združimo csvje v 2 df-ja: prihod in odhod
stolpci = ['Ime', 'Državljanstvo', 'Pozicija', 'Klub', 'Cena', 'Leto']
prihod = pd.DataFrame(columns=stolpci)
odhod = pd.DataFrame(columns=stolpci)

for i in range (2000,2020):
    transferIN = pd.read_csv(str(path+str(i)+'IN.csv'))
    prihod=prihod.append(transferIN)

    transferOUT = pd.read_csv(str(path+str(i)+'OUT.csv'))
    odhodDF=odhod.append(transferOUT)
