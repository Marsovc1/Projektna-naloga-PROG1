# link:  https://en.wikipedia.org/wiki/#sezona*_FC_Barcelona_season
# leta: 2000-01, ..., 2018-19

from bs4 import BeautifulSoup
import requests
import orodja
import pandas

#shranimo HTML dadoteke pod imeni transfer20xy (glede na leto), v mapo html s pomočjo datoteke 'orodja'

link = r'C:\Users\marsovc\Desktop\Fmf\Financna tretji letnik\Programiranje 1\Projektna-naloga-PROG1\html\transfer'

""" 
for i in range(2000,2020):
    if i < 2009:
        shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-0' + str(i-1999) +'_FC_Barcelona_season', link + str(i), vsili_prenos=False)
    else:
        shrani_spletno_stran('https://en.wikipedia.org/wiki/'+ str(i) + '-' + str(i-1999) +'_FC_Barcelona_season', link + str(i), vsili_prenos=False)
 """

# <h3><span class="mw-headline" id="Transfers">Transfers</span><span class - oblika teksta pri transferju

tekst = orodja.vsebina_datoteke(link+'2000')
soup = BeautifulSoup(tekst, 'lxml')

tekst = soup.find('table',class_='wikitable sortable', style="text-align: center;")
ahref = tekst.find_all('a')
transfer_in = []
for link in ahref:
    neki.append(link.get('title'))
neki = neki[3:]
print(neki)

