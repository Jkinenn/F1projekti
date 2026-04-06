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
    # Sinun löytämäsi oikea osoite
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
        # Poimitaan tiedot käyttäen F1:n omia (hassusti kirjoitettuja) otsikoita
        pelaaja = {
            "nimi": p.get('FUllName', p.get('FirstName', 'Tuntematon')),
            "hinta": turvallinen_numero(p.get('Value')),
            "pisteet": turvallinen_numero(p.get('OverallPpints')),
            "tiimi": p.get('TeamName', '')
        }
        
        rooli = p.get('PositionName', '')
        
        # Erotellaan kuskit ja tallit toisistaan
        if rooli == 'DRIVER':
            kuskit.append(pelaaja)
        elif rooli == 'CONSTRUCTOR':
            tallit.append(pelaaja)
            
    return kuskit, tallit

def etsi_paras_tiimi(kuskit, tallit, budjetti=100.0):
    print(f"Etsitään parasta 5 kuskin ja 2 tallin yhdistelmää (Budjetti: ${budjetti}m)...")
    print("Tämä voi kestää muutaman sekunnin, kokeillaan satoja tuhansia yhdistelmiä...")
    
    paras_tiimi = None
    maksimipisteet = -1
    
    kuski_yhdistelmat = list(itertools.combinations(kuskit, 5))
    talli_yhdistelmat = list(itertools.combinations(tallit, 2))
    
    for kuski_kombo in kuski_yhdistelmat:
        for talli_kombo in talli_yhdistelmat:
            
            kokonaishinta = sum(k["hinta"] for k in kuski_kombo) + sum(t["hinta"] for t in talli_kombo)
            
            if kokonaishinta <= budjetti:
                kokonaispisteet = sum(k["pisteet"] for k in kuski_kombo) + sum(t["pisteet"] for t in talli_kombo)
                
                if kokonaispisteet > maksimipisteet:
                    maksimipisteet = kokonaispisteet
                    paras_tiimi = {
                        "kuskit": kuski_kombo,
                        "tallit": talli_kombo,
                        "hinta": kokonaishinta,
                        "pisteet": kokonaispisteet
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
    
    BUDJETTI = 100.0 
    paras = etsi_paras_tiimi(kuskit, tallit, BUDJETTI)
    
    if paras:
        print("\n🏆 OPTIMAALINEN TIIMI LÖYDETTY 🏆")
        print("====================================")
        print("KUSKIT:")
        for k in paras["kuskit"]:
            print(f" 🏎️ {k['nimi']} ({k['tiimi']}) - ${k['hinta']}m | {k['pisteet']} pts")
            
        print("\nTALLIT:")
        for t in paras["tallit"]:
            print(f" 🏭 {t['nimi']} - ${t['hinta']}m | {t['pisteet']} pts")
            
        print("====================================")
        print(f"KOKONAISHINTA: ${round(paras['hinta'], 1)}m / ${BUDJETTI}m")
        print(f"YHTEENSÄ PISTEITÄ: {round(paras['pisteet'], 1)} pts")
    else:
        print("Yhtään budjettiin sopivaa tiimiä ei löytynyt.")

if __name__ == "__main__":
    main()