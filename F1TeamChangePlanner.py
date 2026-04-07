import requests
import itertools

def turvallinen_numero(arvo):
    """Apufunktio, joka muuttaa F1:n tekstit (esim '11.00' tai '') oikeiksi numeroiksi"""
    try:
        if not arvo: return 0.0
        return float(arvo)
    except (ValueError, TypeError):
        return 0.0

def hae_ja_kasittele_data():
    url = "https://fantasy.formula1.com/feeds/drivers/2_en.json?buster=20260309135405"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print("Haetaan dataa F1:n palvelimelta...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Virhe verkkoyhteydessä!")
        return [], []
        
    data = response.json()
    pelaajalista = data.get('Data', {}).get('Value', [])
    
    kuskit = []
    tallit = []
    
    for p in pelaajalista:
        pelaaja = {
            "nimi": p.get('FUllName', p.get('FirstName', 'Tuntematon')),
            "hinta": turvallinen_numero(p.get('Value')),
            "pisteet": turvallinen_numero(p.get('OverallPpints')),
            "tiimi": p.get('TeamName', '')
        }
        
        rooli = p.get('PositionName', '')
        
        if rooli == 'DRIVER':
            kuskit.append(pelaaja)
        elif rooli == 'CONSTRUCTOR':
            tallit.append(pelaaja)
            
    return kuskit, tallit

def etsi_paras_tiimi(kuskit, tallit, nykyiset_kuskit, nykyiset_tallit, budjetti=100.0, max_vaihtoja=2):
    print(f"\nEtsitään parasta tiimiä (Max vaihdot: {max_vaihtoja}, Budjetti: ${budjetti}m)...")
    
    paras_tiimi = None
    maksimipisteet = -1
    
    kuski_yhdistelmat = list(itertools.combinations(kuskit, 5))
    talli_yhdistelmat = list(itertools.combinations(tallit, 2))
    
    # Tehdään nykyisistä nimistä "joukkoja" (set), jotta vertailu on nopeaa
    nykyiset_k_set = set(nykyiset_kuskit)
    nykyiset_t_set = set(nykyiset_tallit)
    
    for kuski_kombo in kuski_yhdistelmat:
        # Laske montako kuskia vaihtuu
        uudet_k_set = set(k["nimi"] for k in kuski_kombo)
        kuskivaihdot = len(uudet_k_set - nykyiset_k_set)
        
        # Jos jo kuskeja vaihtuu liikaa, hylätään tämä yhdistelmä heti (nopeuttaa koodia)
        if kuskivaihdot > max_vaihtoja:
            continue
            
        for talli_kombo in talli_yhdistelmat:
            # Laske montako tallia vaihtuu
            uudet_t_set = set(t["nimi"] for t in talli_kombo)
            tallivaihdot = len(uudet_t_set - nykyiset_t_set)
            
            yhteensa_vaihtoja = kuskivaihdot + tallivaihdot
            
            # Tarkistetaan vaihdosten kokonaismäärä
            if yhteensa_vaihtoja > max_vaihtoja:
                continue
                
            kokonaishinta = sum(k["hinta"] for k in kuski_kombo) + sum(t["hinta"] for t in talli_kombo)
            
            if kokonaishinta <= budjetti:
                # DRS BOOST LOKIIKKA:
                # Etsitään tämän tiimin paras kuski, ja annetaan hänelle tuplapisteet
                paras_kuski = max(kuski_kombo, key=lambda k: k["pisteet"])
                
                peruspisteet_kuskit = sum(k["pisteet"] for k in kuski_kombo)
                pisteet_tallit = sum(t["pisteet"] for t in talli_kombo)
                
                # Kokonaispisteet = kaikkien pisteet + sen parhaan kuskin pisteet vielä kerran (eli x2)
                kokonaispisteet = peruspisteet_kuskit + paras_kuski["pisteet"] + pisteet_tallit
                
                if kokonaispisteet > maksimipisteet:
                    maksimipisteet = kokonaispisteet
                    paras_tiimi = {
                        "kuskit": kuski_kombo,
                        "tallit": talli_kombo,
                        "hinta": kokonaishinta,
                        "pisteet": kokonaispisteet,
                        "drs_kuski": paras_kuski["nimi"],
                        "vaihdot": yhteensa_vaihtoja
                    }
                    
    return paras_tiimi

def main():
    print("====================================")
    print("   🏎️ F1 FANTASY TEAM PLANNER 🏎️   ")
    print("====================================")
    
    kuskit, tallit = hae_ja_kasittele_data()
    
    if not kuskit or not tallit:
        print("Datan käsittely epäonnistui. Tarkista URL!")
        return
        
    print(f"Löydettiin {len(kuskit)} kuskia ja {len(tallit)} tallia.")
    
    # ---------------------------------------------------------
    # TÄYTÄ TÄHÄN OMA NYKYINEN TIIMISI!
    # Varmista, että nimet on kirjoitettu täsmälleen oikein.
    # ---------------------------------------------------------
    OMA_TIIMI_KUSKIT = [
        "Pierre Gasly", 
        "Oliver Bearman", 
        "Gabriel Bortoleto", 
        "Max Verstappen", 
        "Arvin Lindblad"
    ]
    
    OMA_TIIMI_TALLIT = [
        "Mercedes", 
        "Racing bulls"
    ]
    # ---------------------------------------------------------
    
    BUDJETTI = 100.0 
    MAX_VAIHDOT = 2
    
    paras = etsi_paras_tiimi(kuskit, tallit, OMA_TIIMI_KUSKIT, OMA_TIIMI_TALLIT, BUDJETTI, MAX_VAIHDOT)
    
    if paras:
        print("\n🏆 OPTIMAALINEN TIIMI SEURAAVAAN KISAAN 🏆")
        print("====================================")
        print("KUSKIT:")
        for k in paras["kuskit"]:
            # Lisätään DRS-merkintä tuplatulle kuskille
            drs_merkki = "🔥 (DRS BOOST 2X)" if k['nimi'] == paras['drs_kuski'] else ""
            
            # Merkitään myös, onko kuski uusi (vaihdettu)
            uusi_merkki = "🔄 UUSI" if k['nimi'] not in OMA_TIIMI_KUSKIT else ""
            
            print(f" 🏎️ {k['nimi']} ({k['tiimi']}) - ${k['hinta']}m | {k['pisteet']} pts {drs_merkki} {uusi_merkki}")
            
        print("\nTALLIT:")
        for t in paras["tallit"]:
            uusi_merkki = "🔄 UUSI" if t['nimi'] not in OMA_TIIMI_TALLIT else ""
            print(f" 🏭 {t['nimi']} - ${t['hinta']}m | {t['pisteet']} pts {uusi_merkki}")
            
        print("====================================")
        print(f"KOKONAISHINTA: ${round(paras['hinta'], 1)}m / ${BUDJETTI}m")
        print(f"ODOTETUT PISTEET: {round(paras['pisteet'], 1)} pts")
        print(f"TEHDYT VAIHDOT: {paras['vaihdot']} / {MAX_VAIHDOT}")
    else:
        print("\nYhtään budjettiin sopivaa tiimiä ei löytynyt näillä vaihtorajoituksilla.")
        print("Tarkista, että OMA_TIIMI -listoissa olevat nimet on kirjoitettu täsmälleen oikein!")

if __name__ == "__main__":
    main()