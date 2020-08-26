# link:  https://en.wikipedia.org/wiki/#sezona*_FC_Barcelona_season
# leta: 2000-01, ..., 2018-19 in 2019-20
# 18-19 in 19-20 so drugačni kot ostali

from bs4 import BeautifulSoup
import requests
from orodja import *
import pandas as pd

#kam shranim
path = 'C:\\Users\\marsovc\\Desktop\\Fmf\\Dodiplomsko\\Financna 3. letnik\\Programiranje 1\\Projektna-naloga-PROG1\\html\\'

 # from 2k to 2020, probably calendar year 🤔
def shrani_html():
    #s pomočjo orodja.py shranim spletne strani
    for i in range(2000,2020):
        if i < 2009:
            shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-0' + str(i-1999) +'_FC_Barcelona_season', path + str(i), vsili_prenos=False)
        else:
            shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-' + str(i-1999) +'_FC_Barcelona_season', path + str(i), vsili_prenos=False)

def ustvari_df(vrstice,df,i,kam):
    #vrstice vsi table row v tabeli
    #df je ustvarjen dataframe s pandas
    #i letnica
    #kam = IN ali OUT (string)

    for j in range(1, len(vrstice)):
        td = vrstice[j].find_all('td')

        if i > 2017: #posebne wiki tabele
            if len(td) >0:
                #.text ne vrne drzave saj je samo ikona (flagicon) zato izluščim title
                drzava = str(td[4]).split('title=')
                drzava = drzava[1].split('"><img alt=')
                drzava = drzava[0].replace('"','') 

                vrednost = [k.text.replace('\n','') for k in td]

                #čiščenje vrednosti klub presledki pred in za imenom
                if str(vrednost[4])[-1] == ' ':
                    vrednost[4]=str(vrednost[4])[:-1]

                if str(vrednost[4])[0] == ' ':
                    vrednost[4]=str(vrednost[4])[1:]

                #preurejanje vrednosti prestopa
                vrednost[5]=vrednost[5].replace(',','')
                vrednost[5]=vrednost[5].replace('€','')
                if str(vrednost[5])[-1]==']':
                    vrednost[5] = str(vrednost[5])[:-3]
                if str(vrednost[5])[1]=='U':
                    vrednost[5] = str('Neznano')
                
                #če je vrednost prestopa ni znana ni int => try/except
                try:
                    vrednost[5] = str('€'+str(int(vrednost[5])/10**6)+'M')
                except ValueError:
                    vrednost[5] = 'Neznana' 
                

                #če vrednost fee zavzame neke vrednosti  => je loan => ne upoštevam v analizi
                if str(vrednost[5]) != 'N/A' and str(vrednost[5]) != 'Loan' and str(vrednost[5]) != '—':
                    vrednost = [vrednost[3], drzava, vrednost[1],vrednost[4],vrednost[5],i]
                    df.loc[j-1] = vrednost
        
        else:
            #drzava je le flagicon zato iscem iz title
            drzava = str(td[2]).split('title=')
            drzava = drzava[1].split('"><img alt=')
            drzava = drzava[0].replace('"','')

            #list posameznih vrednosti ('stolpcev')
            vrednost = [k.text.replace('\n','') for k in td]

            #čiščenje vrednosti klub
            if vrednost[6] != '':
                if str(vrednost[6])[-1] == ' ':
                    vrednost[6]=str(vrednost[6])[:-1]

                if str(vrednost[6])[0] == ' ':
                    vrednost[6]=str(vrednost[6])[1:]
            
            else:
                vrednost[6]=42

            #če imamo transfer OUT je wiki tabela krajša za 1 stolpec
            if kam == 'OUT':
                if int(i)==2002:
                    if str(vrednost[9])!='Free' and str(vrednost[9])!='Loan':
                        vrednost[9]=vrednost[9].replace(',','')
                        vrednost[9]=vrednost[9].replace('€','')
                        vrednost[9] = str('€'+str(int(vrednost[9])/10**6)+'M')

                 #pri ceni je pri novejših še referenca, ki jo odstranim
                if str(vrednost[9])[-1] == ']':
                    vrednost[9] = str(vrednost[9])[:-5]

                if str(vrednost[9]) != 'N/A' and str(vrednost[9]) != 'Loan' and str(vrednost[9]) != '—' and str(vrednost[7]) != 'Loan' and str(vrednost[7]) != 'Loan return' and vrednost[6]!=42:
                    vrednost = [vrednost[3], drzava, vrednost[1],vrednost[6],vrednost[9],i]
                    df.loc[j-1] = vrednost   
            else:
                #leto 2002, 2018 in 2019 imajo vrednosti prestopov z ',' torej npr 10,000,000
                if int(i)==2002:
                    if str(vrednost[10])!='Free' and str(vrednost[10])!='Loan':
                        vrednost[10]=vrednost[10].replace(',','')
                        vrednost[10]=vrednost[10].replace('€','')
                        vrednost[10] = str('€'+str(int(vrednost[10])/10**6)+'M')

                #zapišemo v vrstico, če je prestop samo posoja ga ne upoštevam
                if str(vrednost[10]) != 'N/A' and str(vrednost[10]) != 'Loan' and str(vrednost[10]) != '—' and str(vrednost[7]) != 'Loan' and str(vrednost[7]) != 'Loan return':
                    vrednost = [vrednost[3], drzava, vrednost[1],vrednost[6],vrednost[10],i]
                    df.loc[j-1] = vrednost   

    df.to_csv(str(str(i)+kam+'.csv'), index=False)   

def table_IN(i,soup): #kje se nahaja tabela wiki za transfer
    #i je letnica
    #soup je html datoteka pripravljena za beautifulsoup branje
    if i in [2000,2001,2002,2003,2004,2005,2009]: 
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[0]
        table = table.tbody
    elif i == 2013:
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[2]
        table = table.tbody
    elif i == 2018:
        table = soup.find_all('table',class_='wikitable sortable')[1]
        table = table.tbody
    elif i == 2019:
        table = soup.find_all('table',class_='wikitable sortable')[2]
        table = table.tbody
    else:
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[1]
        table = table.tbody
    return table

def table_OUT(i,soup): #ogromno specificnih strani
    if i in [2000,2001,2002,2003,2004,2005,2009]: 
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[1]
        table = table.tbody
    elif i == 2013:
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[3]
        table = table.tbody
    elif i == 2018:
        table = soup.find_all('table',class_='wikitable sortable')[2]
        table = table.tbody
    elif i == 2019:
        table = soup.find_all('table',class_='wikitable sortable')[3]
        table = table.tbody
    else:
        table = soup.find_all('table',class_='wikitable sortable', style="text-align: center;")[2]
        table = table.tbody
    return table

def shrani(i): #čas za zapisovanje tabel
    #i je letnica

    #poiščem shranjeno datoteko (iz orodja.py)
    tekst = vsebina_datoteke(path+str(i))

    #dodam v BSoup
    soup = BeautifulSoup(tekst, 'html.parser')

    #table transfer IN
    tableIN = table_IN(i,soup)
    vrsticeIN = tableIN.find_all('tr')
    stolpciIN = ['Ime', 'Državljanstvo', 'Pozicija', 'Klub', 'Cena', 'Leto']
    dfIN = pd.DataFrame(columns=stolpciIN)

    #table transfer OUT
        #analogno za transfer IN (zgoraj)
    #shranim tabelo pod tableOUT
    tableOUT = table_OUT(i,soup) 
    #poiščem vse vrstice
    vrsticeOUT = tableOUT.find_all('tr')  
    #poimenujem stolpce
    stolpciOUT = ['Ime', 'Državljanstvo', 'Pozicija', 'Klub', 'Cena', 'Leto'] 
    #ustvari df s pandas
    dfOUT = pd.DataFrame(columns=stolpciOUT)

    ustvari_df(vrsticeIN,dfIN,i,'IN')
    ustvari_df(vrsticeOUT,dfOUT,i,'OUT')

for i in range(2000,2020): #leta za katera iščem
    shrani(i)