import sqlite3
import os
import sys

# Diese Datei ermöglicht dem Hauptprogramm durchg Funktionen mit Datenbankern zu kommunizieren + erleichtert das
# Bearbeiten der Textfelder


def find_source_path(file):
    # determine if application is a script file or frozen exe + using absolute path (relative doenst work for .exe files)
    if getattr(sys, 'frozen', False):
        path_to_root = os.path.dirname(sys.executable)
    elif __file__:
        path_to_root = os.path.split(os.path.dirname(__file__))[0]
            
    sources_path = os.path.join(path_to_root, "Sources")
    specific_path = os.path.join(sources_path, file)
    return specific_path

directionary = os.path.join(find_source_path("Vokabeln.db")) #Der genaue Pfad zur DB wird ermittelt.

#Definiton von Funktionen, welche fuer das Hauptprogramm wichtig sind
def daten_aus_DB(sql_statement): #Definition einer Funktion zum Bekommen der Daten aus der DB mit einem SQL-Parameter
    verbindung = sqlite3.connect(directionary)
    zeiger = verbindung.cursor()
    data = zeiger.execute(sql_statement)
    inhalt_raw = zeiger.fetchone()
    if inhalt_raw is not None: #Prueft, ob jeweiliger Datenwert in der DB existiert
        inhalt = inhalt_raw[0]
        verbindung.close()
        return inhalt
    else:
        return None #Wenn nicht, wird "None" ausgegeben


def anzahl_vokabeln_insgesamt(zu_lernende_sprache):
    ges = daten_aus_DB(f"SELECT COUNT(*) FROM Vokabeln_{zu_lernende_sprache}") #zaehlt die Anzahl der Vokabeln in der DB
    return ges


def vokabelliste(zu_lernende_Sprache,ausgangssprache): #macht aus der DB eine Liste nur mit den Vokabeln
    vokabelliste = []
    verbindung = sqlite3.connect(directionary)
    zeiger = verbindung.cursor()
    data = zeiger.execute(f"SELECT {ausgangssprache} FROM Vokabeln_{zu_lernende_Sprache}")
    inhalt = zeiger.fetchall()
    for i in inhalt:
        vokabelliste.append(i[0])
    verbindung.close()
    return vokabelliste


def stammformen(lateinische_vokabel):
    anderes = daten_aus_DB(f'SELECT Stammformen FROM Vokabeln_Latein WHERE Latein = "{lateinische_vokabel}"')
    if anderes != None: #prueft, ob aktuelle Vokabel Stammformen hat
        return anderes
    else:
        return ""

def uebersetzung(zu_lernende_sprache,ausgangssprache,zielsprache,vokabel):
    uebersetzung = daten_aus_DB(f'SELECT {zielsprache} FROM Vokabeln_{zu_lernende_sprache} WHERE {ausgangssprache} = "{vokabel}"')
    return uebersetzung

def vok_ausgangssprache(index,zu_lernende_sprache,ausgangssprache):
    vokabel = daten_aus_DB(f"SELECT {ausgangssprache} FROM Vokabeln_{zu_lernende_sprache} WHERE ID ={str(index)}")
    return vokabel

# um den Code leserlicher zu machen, wurd eine extra Funktion für das bearbeiten + löschen des Texts definiert

def text_bearbeiten(feld, *text):
    feld.config(state="normal") #Die config - Methode kann den Status des Textfeldes ändern. Bei "Normal" kann man den Text im Feld bearbeiten.
    if len(text) >= 2:
        feld.insert("end", text[0],text[1])
    else:
        feld.insert("end", text[0])
    feld.config(state="disabled") #Bei "disabled" kann man den Text im Feld nicht bearbeiten.

def text_loeschen(*felder):
    for i in felder:
        i.config(state="normal")
        i.delete('1.0', "end")
        i.config(state="disabled")