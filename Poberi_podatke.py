# link:  https://en.wikipedia.org/wiki/#sezona*_FC_Barcelona_season
# leta: 2000-01, ..., 2018-19 in 2019-20
# 18-19 in 19-20 so drugačni kot ostali

from bs4 import BeautifulSoup
import requests
import orodja
import pandas as pd

#shranimo HTML datoteke pod imeni transfer20xy (glede na leto), v mapo html s pomočjo datoteke 'orodja'

link = r'C:\Users\marsovc\Desktop\Fmf\Financna tretji letnik\Programiranje 1\Projektna-naloga-PROG1\html\transfer'

""" 
for i in range(2000,2020):
    if i < 2009:
        shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-0' + str(i-1999) +'_FC_Barcelona_season', link + str(i), vsili_prenos=False)
    else:
        shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-' + str(i-1999) +'_FC_Barcelona_season', link + str(i), vsili_prenos=False)
 """
#s pomočjo orodja poberem vsebino
tekst = orodja.vsebina_datoteke(link+'2000')
#dodam v BSoup
soup = BeautifulSoup(tekst, 'html.parser')

#table transfer out
table = soup.find('table',class_='wikitable sortable', style="text-align: center;").tbody

rows = table.find_all('tr')

columns = [v.text.replace('\n','') for v in rows[0].find_all('th')]

df = pd.DataFrame(columns=columns)
for i in range(1, len(rows)-1):
    tds = rows[i].find_all('td')
    values =[td.text.replace('\n','') for td in tds]

    df = df.append(pd.Series(values, index = columns), ignore_index = True)
    del df['Source']
    del df['Ends']
    del df['EU']
    print(df)

df.to_csv(r'C:\Users\marsovc\Desktop\Fmf\Financna tretji letnik\Programiranje 1\Projektna-naloga-PROG1\\'+'data.csv',index=False)

#Cilj: poberem title, če title ne obstaja poberem vsebino td, sicer ne poberem nič
