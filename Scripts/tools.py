import sqlite3
import os
import sys

# Diese Datei ermöglicht dem Hauptprogramm durchg Funktionen mit Datenbankern zu kommunizieren + erleichtert das
# Bearbeiten der Textfelder


def find_source_path(file):
    """
    Determines the absolute path to the source file.

    Checks whether the script is being run as a standalone executable or from a script,
    and then calculates the absolute path to the source folder where files are located.

    Args:
        file (str): The filename for which the path is needed.

    Returns:
        str: The absolute path to the source file.
    """
    if getattr(sys, 'frozen', False):
        path_to_root = os.path.dirname(sys.executable)
    elif __file__:
        path_to_root = os.path.split(os.path.dirname(__file__))[0]
            
    sources_path = os.path.join(path_to_root, "Sources")
    specific_path = os.path.join(sources_path, file)
    return specific_path

directionary = os.path.join(find_source_path("Vokabeln.db")) #Der genaue Pfad zur DB wird ermittelt.

def daten_aus_DB(sql_statement):
    """
    Retrieves data from the database based on a given SQL query.

    Executes the provided SQL statement on the database and returns the first result.

    Args:
        sql_statement (str): The SQL query to be executed.

    Returns:
        str or None: The data retrieved from the database or None if no data is found.
    """
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
    """
    Returns the total number of vocabulary words in the specified language.

    Args:
        zu_lernende_sprache (str): The language to count vocabulary words for.

    Returns:
        int: The total number of vocabulary words in the specified language.
    """
    ges = daten_aus_DB(f"SELECT COUNT(*) FROM Vokabeln_{zu_lernende_sprache}") #zaehlt die Anzahl der Vokabeln in der DB
    return ges


def vokabelliste(zu_lernende_Sprache,ausgangssprache):
    """
    Retrieves a list of vocabulary words from the database for the specified language.

    Args:
        zu_lernende_Sprache (str): The language for which to retrieve vocabulary words.
        ausgangssprache (str): The source language column to retrieve vocabulary words from.

    Returns:
        list: A list of vocabulary words from the specified language.
    """
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
    """
    Retrieves the stem forms for a given Latin vocabulary word.

    Args:
        lateinische_vokabel (str): The Latin vocabulary word to retrieve stem forms for.

    Returns:
        str: The stem forms of the Latin vocabulary word, or an empty string if none are found.
    """
    anderes = daten_aus_DB(f'SELECT Stammformen FROM Vokabeln_Latein WHERE Latein = "{lateinische_vokabel}"')
    if anderes != None: #prueft, ob aktuelle Vokabel Stammformen hat
        return anderes
    else:
        return ""

def uebersetzung(zu_lernende_sprache,ausgangssprache,zielsprache,vokabel):
    """
    Retrieves the translation of a vocabulary word for the specified languages.

    Args:
        zu_lernende_sprache (str): The language of the vocabulary word.
        ausgangssprache (str): The source language column to get the vocabulary word.
        zielsprache (str): The target language column for the translation.
        vokabel (str): The vocabulary word to translate.

    Returns:
        str: The translated word in the target language.
    """
    uebersetzung = daten_aus_DB(f'SELECT {zielsprache} FROM Vokabeln_{zu_lernende_sprache} WHERE {ausgangssprache} = "{vokabel}"')
    return uebersetzung

def vok_ausgangssprache(index,zu_lernende_sprache,ausgangssprache):
    """
    Retrieves a vocabulary word from the source language table using its index.

    Args:
        index (int): The index of the vocabulary word.
        zu_lernende_sprache (str): The language of the vocabulary word.
        ausgangssprache (str): The source language column for the vocabulary word.

    Returns:
        str: The vocabulary word from the source language.
    """
    vokabel = daten_aus_DB(f"SELECT {ausgangssprache} FROM Vokabeln_{zu_lernende_sprache} WHERE ID ={str(index)}")
    return vokabel

def text_bearbeiten(feld, *text):
    """
    Edits the content of a text field by inserting text.

    Allows text to be inserted into a text field in a Tkinter GUI, either with or without custom tags.

    Args:
        feld (tk.Text): The text field to be edited.
        *text (str or tuple): The text to insert into the field, with optional formatting.
    """
    feld.config(state="normal") #Die config - Methode kann den Status des Textfeldes ändern. Bei "Normal" kann man den Text im Feld bearbeiten.
    if len(text) >= 2:
        feld.insert("end", text[0],text[1])
    else:
        feld.insert("end", text[0])
    feld.config(state="disabled") #Bei "disabled" kann man den Text im Feld nicht bearbeiten.

def text_loeschen(*felder):
    """
    Clears the content of one or more text fields.

    Args:
        *felder (tk.Text): The text fields to be cleared.
    """
    for i in felder:
        i.config(state="normal")
        i.delete('1.0', "end")
        i.config(state="disabled")