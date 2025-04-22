import sqlite3

#Definiton von Funktionen, welche für das Hauptprogramm wichtig sind

def daten_aus_DB(sql_statement): #Definition einer Funktion zum Bekommen der Daten aus der DB mit einem SQL-Parameter
    verbindung = sqlite3.connect(r"Vokabeln.db")
    zeiger = verbindung.cursor()
    data = zeiger.execute(sql_statement)
    inhalt_raw = zeiger.fetchone()
    if inhalt_raw is not None: #Prüft, ob jeweiliger Datenwert in der DB existiert
        inhalt = inhalt_raw[0]
        verbindung.close()
        return inhalt
    else:
        return None #Wenn nicht, wird "None" ausgegeben


anzahl_vokabeln_insgesamt = daten_aus_DB("SELECT COUNT(*) FROM Vokabeln_Latein") #zählt die Anzahl der Vokabeln in der DB


def vokabelliste_latein(): #macht aus der DB eine Liste nur mit den lateinischen Vokabeln
    liste_latein = []
    verbindung = sqlite3.connect(r"Vokabeln.db")
    zeiger = verbindung.cursor()
    data = zeiger.execute("SELECT Fremdsprache FROM Vokabeln_Latein")
    inhalt = zeiger.fetchall()
    for i in inhalt:
        liste_latein.append(i[0])
    verbindung.close()
    return liste_latein


def vokabel_latein(index):
    vokabel_latein = daten_aus_DB("SELECT Fremdsprache FROM Vokabeln_Latein WHERE ID =" + str(index))
    return vokabel_latein

def stammformen(lateinische_vokabel):
    anderes = daten_aus_DB('SELECT Stammformen FROM Vokabeln_Latein WHERE Fremdsprache = "' + str(lateinische_vokabel) + '"')
    if anderes != None: #prüft, ob aktuelle Vokabel Stammformen hat
        return anderes
    else:
        return ""

def übersetzung(lateinische_vokabel):
    übersetzung = daten_aus_DB('SELECT Übersetzung FROM Vokabeln_Latein WHERE Fremdsprache = "' + str(lateinische_vokabel) + '"')
    return übersetzung
