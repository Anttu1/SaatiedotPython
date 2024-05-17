import sqlite3
import requests 
from datetime import datetime

# Lokikirjoitus
def saa_loki(viesti):
    aika = datetime.now()
   
    tiedosto = open("saaloki.txt", "a")
    rivi = str(aika) + " " + viesti
   
    tiedosto.write(rivi + "\r")
    tiedosto.close()

paikkakunta = ""
print("Haluatko vaihtaa paikkakuntia, joista lämpötilatiedot haetaan?")
syöte = input("Vastaa K/Kyllä tai X/Ei : ")

#if-silmukka, lisää syötettäviä kuntia tietokantaan
if syöte.upper() == "K":
    
    conn = sqlite3.connect('Kunnat.db')
    print()
    print("Kunnat tietokantaan yhdistetty.")
    sql2 = """DROP TABLE IF EXISTS Paikkakunnat"""
    kursori = conn.cursor()
    kursori.execute(sql2)
    sql = """CREATE TABLE IF NOT EXISTS Paikkakunnat(
        paikkakunta text)"""
    print()    
    print("Lisätään uusi Paikkakunnat taulu tietokantaan.")    
    kursori = conn.cursor()
    kursori.execute(sql)
    print()
    print("Taulu lisätty.")
    print()

    #Jatkuu kunnes käyttäjä syöttää 'X'
    while paikkakunta.upper() != "X":
        paikkakunta = input("Anna paikkakunta: ")
        if paikkakunta != "X": 
            sql = f'INSERT INTO Paikkakunnat VALUES ("{paikkakunta}")'
            kursori.execute(sql)
            conn.commit()
            print("Paikkakunta tallennettu. Paina 'X' kun olet syöttänyt kaikki haluamasi paikkakunnat.")
            print()

        else:
            continue
print("Haetaanko lämpötilatiedot?")
syöte2 = input("K/Kyllä  X/Ei : ")
print()

tulos = 0
#Haku Kunnat.db Paikkakunnat-taulun sisältöä vastaavien kuntien lämpötilat
if syöte2.upper() == "K":
    conn = sqlite3.connect('Kunnat.db')
    kursori = conn.cursor()
    print("Tässä valitsemiesi paikkakuntien hakutulos:")
    sql = "SELECT paikkakunta FROM Paikkakunnat"
    for rivi in kursori.execute(sql):
        
        paikkakuntaStr = str(rivi)

        paikkakunta = paikkakuntaStr[2:-3] 

        #Haetaan dataa annetuilla määreillä ilmatieteenlaitoksen sivuilta     
        url = f"https://www.ilmatieteenlaitos.fi/saa/{paikkakunta}"
               
        vastaus = requests.get(url, params={"encoding": "utf-8"})
        vastauksen_status = vastaus.status_code
        tulos += 1
        if vastauksen_status == 200:
            html = str(vastaus.text)
            indeksi = html.index('Temperature')
            alku = indeksi + 11 
            loppu = alku + 5 
            html2 = html[alku:loppu]
            print(f"Paikkakunnan {paikkakunta} lämpötila on {html2}°C")      
            
        elif vastauksen_status == 500:
            saa_loki(f"{paikkakunta} Hakuvirhe")
        else:
            print("VIRHE. Ohjelma päättyy")
            
               
elif syöte2.upper() == "X":
    print("Näkemiin!")
    
else:
    print("Virheellinen vastaus!")

saa_loki(f"Löydettiin {tulos} tulosta.")    
conn.close()
print()
print("Haku valmis, ensi kertaan!")
