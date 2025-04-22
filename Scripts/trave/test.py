import random
import tkinter as tk
import Vokabelliste
import DB_Kommunikation as db
from tkinter import ttk

# komplettes 1. Fenster wird innerhalb einer Klasse erstellt
class Vokabeltrainer:
    def __init__(self):
        # Variablen werden deklariert
        self.zähler_pro_durchgang = 0
        self.anzahl_durchgang = 0
        self.schwierige_vokabeln = []
        self.verlauf = []
        self.vokabelliste_latein = db.vokabelliste_latein()

        # Fenster wird in der Mitte des Monitors erstellt und andere sachen gemacht
        self.Fenster = tk.Tk()
        self.Breite_Fenster = 1920
        self.Höhe_Fenster = 1080
        self.Breite_Monitor = self.Fenster.winfo_screenwidth()
        self.Höhe_Monitor = self.Fenster.winfo_screenheight()
        self.percentage_width = self.Breite_Monitor / (self.Breite_Fenster / 100)
        self.percentage_height = self.Höhe_Monitor / (self.Höhe_Fenster / 100)
        self.scale_factor = ((self.percentage_width + self.percentage_height) / 2) / 100
        self.x = (self.Breite_Monitor / 2) - (self.Breite_Fenster / 2)
        self.y = (self.Höhe_Monitor / 2) - (self.Höhe_Fenster / 2)
        self.Fenster.geometry(f"{self.Breite_Fenster}x{self.Höhe_Fenster}+{int(self.x)}+{int(self.y)}")
        #self.Fenster.overrideredirect(True)
        #self.Fenster.overrideredirect(False)
        #self.Fenster.attributes("-fullscreen", True)
        self.Fenster.title("Vokabeltrainer")
        #self.Fenster.configure(bg="#181818")
        self.fontsize = int(14 * self.scale_factor)
        self.minimum_size = 8
        if self.fontsize < self.minimum_size:
            self.fontsize = self.minimum_size

        # Erstellt einen Stil für die Buttons
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", self.fontsize))
        self.style.configure("TButton", font=("Arial", self.fontsize))

        # Variablen für Labels werden erstellt
        self.zähler = tk.StringVar()
        self.zähler.set("Insgesamt gibt es " + str(db.anzahl_vokabeln_insgesamt) + " verschiedene Vokabeln.")

        self.zähler_für_merkliste = tk.StringVar()
        self.zähler_für_merkliste.set("0 Vokabeln in der Merkliste. ")

        # Labels, Buttons,... werden erstellt
        #self.frame = tk.Frame(self.Fenster)
        self.Neu = ttk.Button(self.Fenster, text="Neue Vokabel", style="TButton", command=self.vokabel_anzeigen)
        self.Neu.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.3)

        self.back = ttk.Button(self.Fenster, text="Vorherige Vokabel", style="TButton", command=self.back)
        self.back.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.1)

        self.Vokabelfeld = tk.Text(self.Fenster, font=("Arial", 20), width=55, height=2)
        self.Vokabelfeld.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.3)
        self.Vokabelfeld.tag_config('warning', foreground="red")

        self.Übersetzen = ttk.Button(self.Fenster, text="Lösung anzeigen", style="TButton", command=self.lösung_anzeigen)
        self.Übersetzen.place(relwidth=0.2, relheight=0.1, relx=0.7, rely=0.3)

        self.lösungsfeld = tk.Text(self.Fenster, font=("Arial", 20), width=55, height=2)
        self.lösungsfeld.place(relwidth=0.4, relheight=0.1, relx=0.3, rely=0.6)
        self.lösungsfeld.tag_config('warning', foreground="red")

        self.vokabelzähler = ttk.Label(self.Fenster, textvariable=self.zähler, style="TLabel")
        self.vokabelzähler.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.1)

        self.zur_Vokabelliste = ttk.Button(self.Fenster, text="Zur Vokabelliste", style="TButton", command=self.zur_vokabelliste)
        self.zur_Vokabelliste.place(relwidth=0.2, relheight=0.1, relx=0.1, rely=0.5)

        self.Reset = ttk.Button(self.Fenster, text="Reset", style="TButton", command=self.Reset)
        self.Reset.place(relwidth=0.2, relheight=0.1, relx=0.7, rely=0.5)

        self.Merken = ttk.Button(self.Fenster, text="Merken", style="TButton", command=self.Merken)
        self.Merken.place(relwidth=0.2, relheight=0.1, relx=0.7, rely=0.1)

        self.zähler_merkliste = ttk.Label(self.Fenster, textvariable=self.zähler_für_merkliste, style="TLabel")
        self.zähler_merkliste.place(relwidth=0.2, relheight=0.05, relx=0.4, rely=0.05)

        self.wiederholen = ttk.Button(self.Fenster, text="Vokabeln wiederholen", style="TButton", command=self.wdh)
        self.wiederholen.place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.5)

        #self.frame.grid(column=0, row=0)
        #self.Neu.grid(column=0, row=0)
    # Funktion zum Starten vom 1. Fenster, in "starten.py" benutzt
    def start(self):
        self.Fenster.mainloop()

    # Funktionen, welche durch Buttons ausgelöst werden, werden nachfolgend definiert:

    def zur_vokabelliste(self):
        Vokabelliste.Vokabelliste(self.Fenster)  # bewirkt einen Fensterwechsel zu der Vokabelliste

    def vokabel_anzeigen(self):
        self.Vokabelfeld.delete('1.0', "end")
        self.lösungsfeld.delete('1.0', "end")
        # Durch eine if-Abfrage wird sichergestellt, dass jede Vokabel (pro Durchgang) nur einmal abgefragt wird.
        if len(self.vokabelliste_latein) == 0:
            self.anzahl_durchgang += 1
            self.Vokabelfeld.insert("end", 'Du bist alle Vokabeln nun ' + str(
                self.anzahl_durchgang) + '-mal durchgegangen.\n Drücke "Neue Vokabel", um mit dem nächsten Durchgang zu starten.')
            self.zähler.set("Insgesamt gibt es " + str(db.anzahl_vokabeln_insgesamt) + " verschiedene Vokabeln.")
            self.zähler_pro_durchgang = 0
            self.vokabelliste_latein = db.vokabelliste_latein()  # neue Vokabelliste kreieren
        else:
            vokabel = random.choice(self.vokabelliste_latein)  # wählt ein zufälliges Element aus der Liste aus
            self.Vokabelfeld.insert("end", str(vokabel))
            self.verlauf.append(vokabel)
            self.vokabelliste_latein.pop(
                self.vokabelliste_latein.index(vokabel))  # diese Zeile stellt sicher, dass die if-Abfrage funktioniert.
            self.zähler_pro_durchgang += 1
            self.zähler.set(str(self.zähler_pro_durchgang) + ". Vokabel des Durchlaufs.\nInsgesamt gibt es " + str(
                db.anzahl_vokabeln_insgesamt) + " verschiedene Vokabeln.")

    def lösung_anzeigen(self):

        self.lösungsfeld.delete('1.0', "end")
        wort = self.Vokabelfeld.get("1.0", "end").rstrip('\n').replace('"', '')
        if self.Vokabelfeld.compare("end-1c", "!=", "1.0") and db.übersetzung(
                wort) != None:  # wenn das Vokabelfeld nicht leer ist und das jeweilige wort in der DB ist:...
            lateinische_vokabel = str(self.Vokabelfeld.get("1.0", "end").rstrip("\n"))
            if db.stammformen(
                    lateinische_vokabel) != "":  # wenn Vokabel keine Stzammformen hat, soll diese direkt in der 1. Zeile ausgegeben werden
                self.lösungsfeld.insert("end",
                                        f"{db.stammformen(lateinische_vokabel)} \n {db.übersetzung(lateinische_vokabel)}")
            else:
                self.lösungsfeld.insert("end", f"{db.übersetzung(lateinische_vokabel)}")
        else:
            self.lösungsfeld.insert("end", 'Drücke erst die Taste "Neue Vokabel".', "warning")

    def Reset(self):

        self.Vokabelfeld.delete('1.0', "end")
        self.lösungsfeld.delete('1.0', "end")
        if self.schwierige_vokabeln != []:
            self.Vokabelfeld.insert("end", 'Wiederhole vor dem Reset noch die Vokabeln.')
        else:
            self.Vokabelfeld.insert("end", 'Zurückgesetzt. Drücke "Neue Vokabel", um anzufangen.')
            self.zähler_pro_durchgang = 0
            self.anzahl_durchgang = 0

    # durch die Funktion "Merken" und "wdh" ist es trotz zufäliger Auswahl der Vokabeln dem User möglich, Vokabeln zu wiederholen
    def Merken(self):
        wort = str(self.Vokabelfeld.get("1.0", "end").rstrip('\n').replace('"', ''))
        if self.Vokabelfeld.compare("end-1c", "!=", "1.0") and db.übersetzung(wort) != None:  # s. o.
            vokabel = self.Vokabelfeld.get("1.0", "end")
            self.schwierige_vokabeln.append(vokabel)
            self.zähler_für_merkliste.set(f"{len(self.schwierige_vokabeln)} Vokabeln in der Merkliste.")
            self.Vokabelfeld.delete('1.0', "end")
            self.lösungsfeld.delete('1.0', "end")
            self.Vokabelfeld.insert("end", 'Vokabel "' + str(vokabel.rstrip('\n')) + '" gemerkt.')

        else:
            self.Vokabelfeld.delete("1.0", "end")

            self.Vokabelfeld.insert("end", 'Drücke erst auf "Neue Vokabel", um eine Vokabel anzuzeigen.', 'warning')

    def wdh(self):

        if self.schwierige_vokabeln != []:
            if self.lösungsfeld.compare("end-1c", "!=", "1.0"):
                self.Vokabelfeld.delete('1.0', "end")
                self.lösungsfeld.delete('1.0', "end")
                vokabel = random.choice(self.schwierige_vokabeln)  # s. o.
                self.Vokabelfeld.insert("end", str(vokabel))
                self.verlauf.append(vokabel)
                self.schwierige_vokabeln.pop(self.schwierige_vokabeln.index(vokabel))
                self.zähler_für_merkliste.set(f"{len(self.schwierige_vokabeln)} Vokabeln in der Merkliste.")
            else:
                self.lösungsfeld.delete("1.0", "end")
                self.lösungsfeld.insert("end", 'Lasse dir erst die Lösung der aktuellen Vokabel anzeigen.', "warning")

        else:
            self.Vokabelfeld.delete("1.0", "end")
            self.Vokabelfeld.insert("end", 'Drücke erst auf "Merken", um Vokabeln zu wiederholen.', "warning")

    def back(self):

        if self.Vokabelfeld.compare("end-1c", "!=",
                                    "1.0"):  # falls man "back" ausführt, ohne zuvor die jetzige Vokabel gelernt zu haben, geht diese "verloren"
            self.Vokabelfeld.delete("1.0", "end")
            self.lösungsfeld.delete('1.0', "end")
            self.Vokabelfeld.insert("end", self.verlauf[len(self.verlauf) - 2])
        else:
            self.lösungsfeld.delete("1.0", "end")
            self.lösungsfeld.insert("end", "Lasse dir erst die Lösung zu der momentanen Vokabel anzeigen.", "warning")










