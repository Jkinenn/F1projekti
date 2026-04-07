# 🏎️ F1 Fantasy Team Planner

Tämä repositorio sisältää kaksi Python-työkalua, joiden avulla voit optimoida ja suunnitella tiimisi virallisessa [F1 Fantasy](https://fantasy.formula1.com/) -pelissä. Skriptit hakevat reaaliaikaiset hinta- ja pistetiedot suoraan F1:n rajapinnasta ja laskevat matemaattisesti optimaalisimmat tiimiyhdistelmät.

## 🚀 Ominaisuudet

Repositorio sisältää kaksi eri skriptiä eri käyttötarkoituksiin:

### 1. `F1TeamPlanner.py` (Uuden tiimin luonti)
Tämä skripti on tarkoitettu tilanteeseen, jossa olet rakentamassa täysin uutta tiimiä (esim. kauden alussa tai kun käytät Wildcardin).
* Etsii kaikkien mahdollisten yhdistelmien joukosta parhaan 5 kuskin ja 2 tallin kombinaation.
* Pitää huolen, ettei 100 miljoonan dollarin budjetti ylity.
* Maksimoi odotusarvoiset pisteet nykyisen datan perusteella.

### 2. `F1TeamChangePlanner.py` (Nykyisen tiimin päivitys ja vaihdot)
Tämä skripti auttaa optimoimaan olemassa olevan tiimin tekemällä vain sallitun määrän vaihtoja kisaviikonloppujen välillä.
* Ottaa huomioon nykyisen tiimisi ja etsii parhaat mahdolliset vaihdot (oletuksena max 2 vaihtoa).
* **DRS Boost -logiikka:** Tunnistaa automaattisesti tiimisi parhaan kuskin ja antaa hänelle 2x-pisteet (DRS Boost).
* Näyttää tulosteessa selkeästi, ketkä kuskit tai tallit ovat uusia (🔄) ja kenellä on DRS Boost (🔥).

## 🛠️ Asennus ja vaatimukset

Koodin ajamiseen tarvitset [Pythonin](https://www.python.org/) (versio 3.6 tai uudempi). Lisäksi sinun tulee asentaa ulkoinen `requests`-kirjasto datan hakemista varten.

