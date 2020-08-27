# link:  https://en.wikipedia.org/wiki/#sezona*_FC_Barcelona_season
# leta: 2000-01, ..., 2018-19 in 2019-20
# 18-19 in 19-20 so drugačni kot ostali

from bs4 import BeautifulSoup
import requests
from orodja import *
import pandas as pd

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
                if str(vrednost[5]) == 'Free':
                    vrednost[5]=0

                #če je vrednost prestopa ni znana ni int => try/except
                try:
                    vrednost[5] = str(str(int(vrednost[5])/10**6))
                except ValueError:
                    vrednost[5] = 'Neznana' 
                
                

                #če vrednost fee zavzame neke vrednosti  => je loan => ne upoštevam v analizi
                if str(vrednost[5]) != 'N/A' and str(vrednost[5]) != 'Loan' and str(vrednost[5]) != '—' and vrednost[5]!= 'Neznana':
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
                #kar nekaj ne pretirano lepih reči v vrednosti prestopa
                vrednost[9]=vrednost[9].replace(',','')
                vrednost[9]=vrednost[9].replace('€','')
                vrednost[9]=vrednost[9].replace('M','')
                vrednost[9]=vrednost[9].replace('m','')
                vrednost[9]=vrednost[9].replace('in variables','')
                vrednost[9]=vrednost[9].replace('purchase option','')
                vrednost[9]=vrednost[9].replace('[107]','')
                vrednost[9]=vrednost[9].replace('variables','')
                vrednost[9]=vrednost[9].replace(' ','')
                vrednost[9]=vrednost[9].split('+')

                vrednost_prestop = 0
                for fee in vrednost[9]:
                    if fee not in ['N/A', 'Free', 'Loan', '—', 'Youthsyste', '']:
                        vrednost_prestop += float(fee)
                vrednost[9] = vrednost_prestop

                if i in [2002, 2005]:
                    if str(vrednost[9]) not in ['Free','Loan','N/A']:
                        vrednost[9] = str(int(vrednost[9])/10**6)

                #pri ceni je pri novejših še referenca, ki jo odstranim
                if str(vrednost[9])[-1] == ']':
                    vrednost[9] = str(vrednost[9])[:-5]

                if str(vrednost[9])=='Free':
                    vrednost[9] = 0

                if str(vrednost[9]) not in ['N/A','Loan','—'] and str(vrednost[7]) != 'Loan' and str(vrednost[7]) != 'Loan return' and vrednost[6]!=42:
                    vrednost = [vrednost[3], drzava, vrednost[1],vrednost[6],vrednost[9],i]
                    df.loc[j-1] = vrednost   
            else:
                #kar nekaj ne pretirano lepih reči v vrednosti prestopa
                vrednost[10]=vrednost[10].replace(',','')
                vrednost[10]=vrednost[10].replace('€','')
                vrednost[10]=vrednost[10].replace('M','')
                vrednost[10]=vrednost[10].replace('m','')
                vrednost[10]=vrednost[10].replace('in variables','')
                vrednost[10]=vrednost[10].replace(' ','')
                vrednost[10]=vrednost[10].replace(str('+SauelEto\'o[22]'),'')
                vrednost[10]=vrednost[10].replace('+variables','')
                vrednost[10]=vrednost[10].replace('+Suárezloan','')
                vrednost[10]=vrednost[10].replace('variables','')
                vrednost[10]=vrednost[10].replace('[a]','')
                vrednost[10]=vrednost[10].split('+')

                vrednost_prestop = 0
                for fee in vrednost[10]:
                    if fee not in ['N/A', 'Free', 'Loan', '—', 'Youthsyste', '']:
                        vrednost_prestop += float(fee)
                vrednost[10] = vrednost_prestop
                    

                #leto 2002, 2018 in 2019 imajo vrednosti prestopov z ',' torej npr 10,000,000
                if i == 2002:
                    if str(vrednost[10])!='Free' and str(vrednost[10])!='Loan':
                        vrednost[10] = str(int(vrednost[10])/10**6)

                elif str(vrednost[10]) == 'Free':
                    vrednost[10] = 0

                #zapišemo v vrstico, če je prestop samo posoja ga ne upoštevam
                if str(vrednost[10]) != 'N/A' and str(vrednost[10]) != 'Loan' and str(vrednost[10]) != '—' and str(vrednost[7]) != 'Loan' and str(vrednost[7]) != 'Loan return':
                    vrednost = [vrednost[3], drzava, vrednost[1],vrednost[6],vrednost[10],i]
                    df.loc[j-1] = vrednost   

    df.to_csv(str('.\\podatki\\'+str(i)+kam+'.csv'), index=False)   

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
    tekst = vsebina_datoteke('.\\html\\'+str(i))

    #dodam v BSoup
    soup = BeautifulSoup(tekst, 'html.parser')

    #poimenujem stolpce df
    stolpci = ['Ime', 'Državljanstvo', 'Pozicija', 'Klub', 'Cena', 'Leto']

    #table transfer IN
    tableIN = table_IN(i,soup)
    vrsticeIN = tableIN.find_all('tr')
    dfIN = pd.DataFrame(columns=stolpci)

    #table transfer OUT
        #analogno za transfer IN (zgoraj)
    #shranim tabelo pod tableOUT
    tableOUT = table_OUT(i,soup) 
    #poiščem vse vrstice
    vrsticeOUT = tableOUT.find_all('tr')  
    #ustvari df s pandas
    dfOUT = pd.DataFrame(columns=stolpci)

    ustvari_df(vrsticeIN,dfIN,i,'IN')
    ustvari_df(vrsticeOUT,dfOUT,i,'OUT')

for i in range(2000,2020): #leta za katera iščem
    shrani(i)