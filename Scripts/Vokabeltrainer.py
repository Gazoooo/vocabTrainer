import random
import tkinter as tk
import Vokabelliste
import tools as tools



class Vokabeltrainer:
    """
    A class for creating a vocabulary trainer application using Tkinter.
    """
    
    def __init__(self, zu_lernende_sprache, uebersetzungsrichtung):
        """
        Initializes the Vokabeltrainer object.

        Parameters:
            zu_lernende_sprache : str
                The language to be learned.
            uebersetzungsrichtung : tuple
                A tuple indicating the translation direction (source language, target language).
        """
        self.uebersetzungsrichtung = uebersetzungsrichtung
        self.zu_lernende_sprache = zu_lernende_sprache
        self.ausgangssprache = uebersetzungsrichtung[0]
        self.zielsprache = uebersetzungsrichtung[1]
        self.zaehler_pro_durchgang = 0
        self.anzahl_durchgang = 0
        self.schwierige_vokabeln = []
        self.verlauf = []
        self.vokabelliste = tools.vokabelliste(self.zu_lernende_sprache,self.ausgangssprache)

        # Fenster wird in der Mitte des Monitors erstellt
        self.Fenster = tk.Tk()
        self.Breite_Fenster = 1000
        self.Hoehe_Fenster = 550
        self.Breite_Monitor = self.Fenster.winfo_screenwidth()
        self.Hoehe_Monitor = self.Fenster.winfo_screenheight()
        self.x = (self.Breite_Monitor/2) - (self.Breite_Fenster/2)
        self.y = (self.Hoehe_Monitor/2) - (self.Hoehe_Fenster/2)
        self.Fenster.geometry(f"{self.Breite_Fenster}x{self.Hoehe_Fenster}+{int(self.x)}+{int(self.y)}")
        self.Fenster.title("Vokabeltrainer")
        self.Fenster.configure(bg="#181818")
        self.icon_image = tk.PhotoImage(file=tools.find_source_path(f"{self.zu_lernende_sprache}.png"))
        self.Fenster.iconphoto(True, self.icon_image)

        # Variablen fuer Labels werden erstellt
        self.zaehler = tk.StringVar()
        self.zaehler.set(f"Insgesamt gibt es {tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache)} verschiedene Vokabeln.")

        self.zaehler_fuer_merkliste = tk.StringVar()
        self.zaehler_fuer_merkliste.set("0 Vokabeln in der Merkliste. ")

        # Labels, Buttons,... werden erstellt
        self.Neu = tk.Button(self.Fenster, text="Neue Vokabel", font=("Arial", 20), bg="#262626", fg="white", width=15, command=self.vokabel_anzeigen)
        self.Neu.place(x=350, y=20)

        self.back = tk.Button(self.Fenster, text="Vorherige Vokabel", font=("Arial", 20), bg="#262626", fg="white", width=20, command=self.back)
        self.back.place(x=10, y=15)

        self.Vokabelfeld = tk.Text(self.Fenster, font=("Arial", 20), bg="#262626", fg="white", width=55, height=2)
        self.Vokabelfeld.place(x=40, y=120)
        self.Vokabelfeld.tag_config('warning', foreground="red")

        self.uebersetzen = tk.Button(self.Fenster, text="Lösung anzeigen", font=("Arial", 20), bg="#262626", fg="white", width=15, command=self.loesung_anzeigen)
        self.uebersetzen.place(x=350, y=200)

        self.loesungsfeld = tk.Text(self.Fenster, font=("Arial", 20), bg="#262626", fg="white", width=55, height=2)
        self.loesungsfeld.place(x=40, y=270)
        self.loesungsfeld.tag_config('warning', foreground="red")

        self.vokabelzaehler = tk.Label(self.Fenster, textvariable=self.zaehler, font=("Arial", 20), bg="#262626", fg="white", width=45)
        self.vokabelzaehler.place(x=100, y=360)

        self.zur_Vokabelliste = tk.Button(self.Fenster, text="Zur Vokabelliste", font=("Arial", 20), bg="#262626", fg="white", width=15,command=self.zur_vokabelliste)
        self.zur_Vokabelliste.place(x=400, y=450)

        self.Reset = tk.Button(self.Fenster, text="Reset", font=("Arial", 20), bg="#262626", fg="white", width=15, command=self.Reset)
        self.Reset.place(x=100, y=450)

        self.Merken = tk.Button(self.Fenster, text="Merken", font=("Arial", 20), bg="#262626", fg="white", width=15, command=self.Merken)
        self.Merken.place(x=670, y=5)

        self.zaehler_merkliste = tk.Label(self.Fenster, textvariable=self.zaehler_fuer_merkliste, font=("Arial", 20), bg="#262626", fg="white", width=23)
        self.zaehler_merkliste.place(x=600, y=70)

        self.wiederholen = tk.Button(self.Fenster, text="Vokabeln wiederholen", font=("Arial", 20), bg="#262626", fg="white", width=20, command=self.wdh)
        self.wiederholen.place(x=650, y=200)

    def start(self):
        """
        Starts the Tkinter mainloop for the application.
        """
        self.Fenster.mainloop()

    def zur_vokabelliste(self):
        """
        Opens the vocabulary list window, where the user can view and manage their vocabulary.
        """
        Vokabelliste.Vokabelliste(self.zu_lernende_sprache, self.uebersetzungsrichtung)

    def vokabel_anzeigen(self):
        """
        Displays a new random word from the vocabulary list.
        Ensures that each word is only asked once per round.
        If all words have been asked, starts a new round.
        """
        # es wird sichergestellt, dass jede Vokabel (pro Durchgang) nur einmal abgefragt wird.
        if len(self.vokabelliste) == 0:
            self.anzahl_durchgang += 1
            tools.text_bearbeiten(self.Vokabelfeld,f'Du bist alle Vokabeln nun {self.anzahl_durchgang}-mal durchgegangen.\nDrücke "Neue Vokabel", um mit dem nächsten Durchgang zu starten.')
            self.zaehler.set(f"Insgesamt gibt es {tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache)} verschiedene Vokabeln.")
            self.zaehler_pro_durchgang = 0
            self.vokabelliste = tools.vokabelliste(self.zu_lernende_sprache,self.ausgangssprache) #neue Vokabelliste kreieren
        else:
            if self.loesungsfeld.compare("end-1c", "!=", "1.0") or len(self.verlauf) == 0 or "gemerkt" in self.Vokabelfeld.get("1.0","end"):
                tools.text_loeschen(self.Vokabelfeld, self.loesungsfeld)
                vokabel = random.choice(self.vokabelliste) #waehlt ein zufaelliges Element aus der Liste aus
                tools.text_bearbeiten(self.Vokabelfeld,str(vokabel))
                self.verlauf.append(vokabel)
                self.vokabelliste.pop(self.vokabelliste.index(vokabel)) # diese Zeile stellt sicher, dass die if-Abfrage durch eine immer kleiner werdende Liste funktioniert.
                self.zaehler_pro_durchgang += 1
                self.zaehler.set(f"{self.zaehler_pro_durchgang}. Vokabel des Durchlaufs.\nInsgesamt gibt es {tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache)} verschiedene Vokabeln.")
            else:
                tools.text_bearbeiten(self.loesungsfeld, 'Lasse dir erst die Lösung der aktuellen Vokabel anzeigen.','warning')

    def loesung_anzeigen(self):
        """
        Shows the translation of the current word. If the current word has no translation,
        a warning message is displayed.
        """
        tools.text_loeschen(self.loesungsfeld)
        wort = self.Vokabelfeld.get("1.0","end").rstrip('\n').replace('"','')
        if self.Vokabelfeld.compare("end-1c", "!=", "1.0") and tools.uebersetzung(self.zu_lernende_sprache,self.ausgangssprache,self.zielsprache,wort) != None: # wenn das Vokabelfeld nicht leer ist und das jeweilige wort in der DB ist:...
            vokabel = str(self.Vokabelfeld.get("1.0", "end").rstrip("\n"))
            if tools.stammformen(vokabel) != "": #wenn Vokabel keine Stammformen hat, soll diese direkt in der 1. Zeile ausgegeben werden
                tools.text_bearbeiten(self.loesungsfeld,f"{tools.stammformen(vokabel)}\n{tools.uebersetzung(self.zu_lernende_sprache,self.ausgangssprache,self.zielsprache,vokabel)}")
            else:
                tools.text_bearbeiten(self.loesungsfeld,f"{tools.uebersetzung(self.zu_lernende_sprache,self.ausgangssprache,self.zielsprache,vokabel)}")
        else:
            tools.text_bearbeiten(self.loesungsfeld,'Drücke erst die Taste "Neue Vokabel".', "warning")

    def Reset(self):
        """
        Resets the application, clearing the current round's data and settings.
        """
        tools.text_loeschen(self.Vokabelfeld, self.loesungsfeld)
        if self.schwierige_vokabeln != []: #wenn sich noch keine Vokabeln gemerkt wurden
            tools.text_bearbeiten(self.Vokabelfeld,'Wiederhole vor dem Reset noch die Vokabeln.')
        else:
            tools.text_bearbeiten(self.Vokabelfeld,'Zurückgesetzt. Drücke "Neue Vokabel", um anzufangen.')
            self.zaehler_pro_durchgang = 0
            self.anzahl_durchgang = 0

    def Merken(self):
        """
        Marks the current word as difficult for later repetition.
        If the word is already in the difficult list, a warning is displayed.
        """
        wort = str(self.Vokabelfeld.get("1.0", "end").rstrip('\n').replace('"',''))
        if self.Vokabelfeld.compare("end-1c", "!=", "1.0") and self.loesungsfeld.compare("end-1c", "!=", "1.0"): #s. o.
            vokabel = self.Vokabelfeld.get("1.0", "end")
            if not vokabel in self.schwierige_vokabeln:
                self.schwierige_vokabeln.append(vokabel)
                self.zaehler_fuer_merkliste.set(f"{len(self.schwierige_vokabeln)} Vokabeln in der Merkliste.")
                tools.text_loeschen(self.Vokabelfeld, self.loesungsfeld)
                tools.text_bearbeiten(self.Vokabelfeld, 'Vokabel "' + str(vokabel.rstrip('\n')) + '" gemerkt.')
            else:
                tools.text_loeschen(self.loesungsfeld)
                tools.text_bearbeiten(self.loesungsfeld, 'Vokabel "' + str(vokabel.rstrip('\n')) + '" bereits in Merkliste.', "warning")
        elif self.loesungsfeld.compare("end-1c", "==", "1.0"):
            tools.text_bearbeiten(self.loesungsfeld, 'Lasse dir erst die Lösung der jetzigen Vokabel anzeigen.','warning')

        else:
            tools.text_loeschen(self.loesungsfeld)
            tools.text_bearbeiten(self.loesungsfeld,'Drücke erst auf "Neue Vokabel", um eine Vokabel anzuzeigen.', 'warning')

    def wdh(self):
        """
        Repeats a previously marked difficult word.
        If no difficult words exist, a warning is displayed.
        """
        if self.schwierige_vokabeln != []:
            if self.loesungsfeld.compare("end-1c", "!=", "1.0") or ("gemerkt" in self.Vokabelfeld.get("1.0", "end")): #es soll nur eine Warnung (s. u.) ausgegeben werden, wenn der User die Loesung nicht angeguckt hat oder er davor die Taste "Merken" gedrueckt hat.
                tools.text_loeschen(self.Vokabelfeld, self.loesungsfeld)
                vokabel = random.choice(self.schwierige_vokabeln)
                tools.text_bearbeiten(self.Vokabelfeld,str(vokabel))
                self.verlauf.append(vokabel)
                self.schwierige_vokabeln.pop(self.schwierige_vokabeln.index(vokabel))
                self.zaehler_fuer_merkliste.set(f"{len(self.schwierige_vokabeln)} Vokabeln in der Merkliste.")
            else:
                tools.text_loeschen(self.loesungsfeld)
                tools.text_bearbeiten(self.loesungsfeld,'Lasse dir erst die Lösung der aktuellen Vokabel anzeigen.', "warning")

        else:
            tools.text_loeschen(self.loesungsfeld)
            tools.text_bearbeiten(self.loesungsfeld,'Druecke erst auf "Merken", um Vokabeln zu wiederholen.', "warning")

    def back(self):
        """
        Goes back to the previous word in the current session.
        If the current word has not been learned yet, a warning is displayed.
        """
        if self.loesungsfeld.compare("end-1c", "!=", "1.0") or "gemerkt" in self.Vokabelfeld.get("1.0","end"): #falls man "back" ausfuehrt, ohne zuvor die jetzige Vokabel gelernt zu haben, geht diese "verloren"
            jetzige_vokabel = self.Vokabelfeld.get("1.0", "end").rstrip("\n")
            if "gemerkt" in jetzige_vokabel: #falls mehr als die Vokabel im Textfeld steht, soll nur die Vokabel an sich genommen werden (Das wäre der Fall, wenn man sich direkt davor eine Vokabel gemerkt hat.)
                jetzige_vokabel_list = jetzige_vokabel.split(" ")[1:-1]
                jetzige_vokabel = " ".join(jetzige_vokabel_list).replace('"',"")
            vorherige_vokabel = self.verlauf[self.verlauf.index(jetzige_vokabel) - 1]
            tools.text_loeschen(self.Vokabelfeld, self.loesungsfeld)
            tools.text_bearbeiten(self.Vokabelfeld,vorherige_vokabel)
        else:
            tools.text_loeschen(self.loesungsfeld)
            tools.text_bearbeiten(self.loesungsfeld,"Lasse dir erst die Lösung zu der momentanen Vokabel anzeigen.", "warning")













