import pandas as pd

#najprej bo potrebnega nekaj čiščenja cene so oblike €...M ali pa celo string

path = 'C:\\Users\\marsovc\\Desktop\\Fmf\\Dodiplomsko\\Financna 3. letnik\\Programiranje 1\\Projektna-naloga-PROG1\\podatki\\'
i=2000
transfer = pd.read_csv(str(path+str(i)+'IN.csv'))
print(transfer["Cena"])