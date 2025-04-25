import tkinter as tk
import tkinter.scrolledtext as st
import tools as tools



class Vokabelliste:
    """
    A class representing a vocabulary list for language learning.

    This class creates a GUI window that displays a list of vocabulary words in two languages
    and allows the user to navigate, search, and display the vocabulary.
    """
    
    def __init__(self, zu_lernende_sprache, uebersetzungsrichtung): 
        """
        Initializes the vocabulary list window with the provided languages.

        Args:
            zu_lernende_sprache (str): The language to be learned.
            uebersetzungsrichtung (tuple): A tuple containing the source and target languages (in this order).
        """
        self.vokabel_ID = 0

        self.displayed_all = False

        self.zu_lernende_sprache = zu_lernende_sprache
        self.ausgangssprache = uebersetzungsrichtung[0]
        self.zielsprache = uebersetzungsrichtung[1]
        self.vokabelliste = tools.vokabelliste(self.zu_lernende_sprache, self.ausgangssprache)

        self.Fenster2 = tk.Toplevel()
        self.Hoehe_Fenster = 800
        self.Breite_Fenster = 1300
        self.Breite_Monitor = self.Fenster2.winfo_screenwidth()
        self.Hoehe_Monitor = self.Fenster2.winfo_screenheight()
        self.x = (self.Breite_Monitor / 2) - (self.Breite_Fenster / 2)
        self.y = (self.Hoehe_Monitor / 2) - (self.Hoehe_Fenster / 2)
        self.Fenster2.geometry(f"{self.Breite_Fenster}x{self.Hoehe_Fenster}+{int(self.x)}+{int(self.y)}")

        self.Fenster2.title("Vokabelliste")
        self.Fenster2.configure(bg="#181818")
        self.Fenster2.iconbitmap((tools.find_source_path("vocabulary-list.ico")))


        self.count = tk.StringVar() #Variable fuer das Markieren der gesuchten Vokabel in der Ausgangssprache
        self.count2 = tk.StringVar() #Variable fuer das Markieren der gesuchten Vokabel in der Zielsprache

        #Variablen fuer Labels deklarieren
        self.vokabelzaehler2 = tk.StringVar()
        self.vokabelzaehler2.set(f"Insgesamt gibt es {tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache)} verschiedene Vokabeln.")

        self.text_ausgangssprache = tk.StringVar()
        self.text_ausgangssprache.set(f"{self.ausgangssprache}")

        self.text_zielsprache = tk.StringVar()
        self.text_zielsprache.set(f"{self.zielsprache}")

        # Widgets werden erstellt
        self.Scrollbar = tk.Scrollbar(self.Fenster2)
        self.Scrollbar.pack(side="right", fill="y")

        self.Vokabelanzeige_ausgangssprache = tk.Text(self.Fenster2, font=("Arial", 16), bg="#262626", fg="white", width=45, height=25)
        self.Vokabelanzeige_ausgangssprache.place(x=50,y=150)

        self.Vokabelanzeige_zielsprache = tk.Text(self.Fenster2, font=("Arial", 16), bg="#262626", fg="white", width=45, height=25, yscrollcommand=self.Scrollbar.set)
        self.Vokabelanzeige_zielsprache.place(x=650, y=150)

        self.naechste_vokabelzeile = tk.Button(self.Fenster2, text="Nächste Zeile", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.naechste_vokabelzeile_anzeigen)
        self.naechste_vokabelzeile.place(x=450, y=30)

        self.alle_vokabeln_anzeigen = tk.Button(self.Fenster2, text="Alles anzeigen", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.alles_anzeigen)
        self.alle_vokabeln_anzeigen.place(x=700, y=30)

        self.Label_ausgangssprache = tk.Label(self.Fenster2, textvariable = self.text_ausgangssprache, font=("Arial", 16), bg="#262626", fg="white", width=15)
        self.Label_ausgangssprache.place(x=100, y=100)

        self.Label_zielsprache = tk.Label(self.Fenster2, textvariable= self.text_zielsprache, font=("Arial", 16), bg="#262626", fg="white")
        self.Label_zielsprache.place(x=700, y=100)

        self.vokabel_suchfeld = tk.Entry(self.Fenster2, font=("Arial", 16), bg="#262626", fg="white", width=15)
        self.vokabel_suchfeld.place(x=950, y=100)

        self.Suche = tk.Button(self.Fenster2, text="Vokabel suchen", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.Suchen)
        self.Suche.place(x=950, y=30)

        self.Zaehler = tk.Label(self.Fenster2, textvariable=self.vokabelzaehler2, font=("Arial", 16), bg="#262626", fg="white", width=35)
        self.Zaehler.place(x=10, y=10)



        #Die Vokabeln sollen mithilfe des Mausrads oder einer Scrollbar scrollbar sein
        self.Scrollbar.config(command=self.scrollen_scrollbar)
        self.Vokabelanzeige_zielsprache.bind("<MouseWheel>", self.scrollen_mausrad)
        self.Vokabelanzeige_ausgangssprache.bind("<MouseWheel>", self.scrollen_mausrad)
        self.Fenster2.bind("<MouseWheel>", self.scrollen_mausrad)

    def scrollen_mausrad(self,event): 
        """
        Handles scrolling using the mouse wheel for both vocabulary columns.

        Args:
            event (tk.Event): The event object containing the mouse wheel information.
        """
        self.Vokabelanzeige_ausgangssprache.yview_scroll(int(-1*(event.delta/120)), "units") #"event" uebergibt neben x und y auch delta, welches durch das Vorzeichen angibt, in welche Richtung gescrollt wird (120 oder -120)
        self.Vokabelanzeige_zielsprache.yview_scroll(int(-1*(event.delta/120)), "units") #fuer die yview_scroll Funktion muss der Parameter (OS spezifisch(?))  abgeaendert werden
        return "break" #dadurch lassen sich die Textfelder nicht mehr ohne eine zugewiesene Funktion scrollen (Bei Tkinter kann man Textfelder auch so scrollen, wenn amn mit der Maus darauf zeigt)

    def scrollen_scrollbar(self,*args):
        """
        Handles scrolling using the scrollbar for both vocabulary columns.

        Args:
            *args: Variable arguments passed by the scrollbar widget.
        """
        self.Vokabelanzeige_ausgangssprache.yview(*args) #der .yview Befehl bewirkt, dass gescrollt wird
        self.Vokabelanzeige_zielsprache.yview(*args)

    def naechste_vokabelzeile_anzeigen(self):
        """
        Displays the next vocabulary word in the list.
        If all words have been displayed, it resets the list and prepares for a new cycle.
        """
        if self.displayed_all: #Falls schon alle Vokabeln durch "alles anzeigen" angezeigt sind:
            tools.text_loeschen(self.Vokabelanzeige_ausgangssprache, self.Vokabelanzeige_zielsprache)
            self.vokabel_ID = 0
            self.displayed_all = False

        if self.vokabel_ID < tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache): #solange noch nicht alle Vokabeln angezeigt wurden...
            self.vokabel_ID += 1
            tools.text_bearbeiten(self.Vokabelanzeige_ausgangssprache,f"{tools.vok_ausgangssprache(self.vokabel_ID,self.zu_lernende_sprache,self.ausgangssprache)} {tools.stammformen(tools.vok_ausgangssprache(self.vokabel_ID,self.zu_lernende_sprache,self.ausgangssprache))}\n")
            self.Vokabelanzeige_ausgangssprache.see("end")
            tools.text_bearbeiten(self.Vokabelanzeige_zielsprache,f"{tools.uebersetzung(self.zu_lernende_sprache,self.ausgangssprache,self.zielsprache,tools.vok_ausgangssprache(self.vokabel_ID,self.zu_lernende_sprache,self.ausgangssprache))}\n")
            self.Vokabelanzeige_zielsprache.see("end")
            self.vokabelzaehler2.set(f"Noch {tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache) - self.vokabel_ID} Vokabeln.")
        else:
            self.vokabelzaehler2.set("Das waren alle Vokabeln.")

    def alles_anzeigen(self):
        """
        Displays all vocabulary words in the list.
        The entire vocabulary list is displayed at once, without navigation.
        """
        self.displayed_all = True
        tools.text_loeschen(self.Vokabelanzeige_ausgangssprache,self.Vokabelanzeige_zielsprache)
        for i in range(1, tools.anzahl_vokabeln_insgesamt(self.zu_lernende_sprache) + 1):  #führe nabchfolgende Befehle pro Vokabel aus
            tools.text_bearbeiten(self.Vokabelanzeige_ausgangssprache,f"{tools.vok_ausgangssprache(i,self.zu_lernende_sprache,self.ausgangssprache)} {tools.stammformen(tools.vok_ausgangssprache(i,self.zu_lernende_sprache,self.ausgangssprache))}\n")
            tools.text_bearbeiten(self.Vokabelanzeige_zielsprache,f"{tools.uebersetzung(self.zu_lernende_sprache,self.ausgangssprache,self.zielsprache,tools.vok_ausgangssprache(i,self.zu_lernende_sprache,self.ausgangssprache))}\n")
        self.vokabelzaehler2.set("Alle Vokabeln angezeigt.")

    def Suchen(self):
        """
        Searches for a word in the vocabulary and highlights it in both languages.

        The search is case-sensitive and highlights all occurrences of the word in both the
        source and target language columns.

        If no word is found, no action is performed.
        """
        wort = str(self.vokabel_suchfeld.get())
        self.vokabel_suchfeld.delete(0,"end")
        self.Vokabelanzeige_ausgangssprache.tag_configure('Ausgangssprache', background='#737F00')
        self.Vokabelanzeige_zielsprache.tag_configure('Zielsprache', background='#3FABB0')
        self.Vokabelanzeige_ausgangssprache.tag_remove('Ausgangssprache', 1.0, 'end')
        self.Vokabelanzeige_zielsprache.tag_remove('Zielsprache', 1.0, 'end')

        if wort != "":
            start_index_links = "1.0"
            start_index_rechts = "1.0"
            index_gesuchtes_wort_ausgangssprache = str(self.Vokabelanzeige_ausgangssprache.search(wort, start_index_links, stopindex="end", count=self.count)) #es wird ausgehend vom start_index nach "wort" gesucht
            index_gesuchtes_wort_zielsprache = str(self.Vokabelanzeige_zielsprache.search(wort, start_index_rechts, stopindex="end", count=self.count2)) #"count" gibt u.A. den Index des letzten Treffers wieder

            while index_gesuchtes_wort_ausgangssprache != "": #Durch eine while-Schleife werden alle Ergebnisse markiert + Fehlermeldungen, wenn die eingegebe Buchstabenkombination nicht existiert, verhindert
                self.Vokabelanzeige_ausgangssprache.tag_add('Ausgangssprache', index_gesuchtes_wort_ausgangssprache, f"{index_gesuchtes_wort_ausgangssprache}+{self.count.get()}c") #Durch die Count-Variable wird immer nur die eingegebene Buchstabenkombination markiert (s. o.)

                index_gesuchtes_wort_ausgangssprache = str(self.Vokabelanzeige_ausgangssprache.search(wort, start_index_links, stopindex="end", count=self.count))
                start_index_links = f"{index_gesuchtes_wort_ausgangssprache}+{self.count.get()}c"  # Der neue Start-Index nach dem gesuchten Wortes


            while index_gesuchtes_wort_zielsprache != "":  # Durch eine while-Schleife werden alle Ergebnisse markiert + Fehlermeldungen, wenn die eingegebe Buchstabenkombination nicht existiert, verhindert
                self.Vokabelanzeige_zielsprache.tag_add('Zielsprache', index_gesuchtes_wort_zielsprache,f"{index_gesuchtes_wort_zielsprache}+{self.count2.get()}c")  # Durch die Count-Variable wird immer nur die eingegebene Buchstabenkombination markiert (s. o.)

                index_gesuchtes_wort_zielsprache = str(self.Vokabelanzeige_zielsprache.search(wort, start_index_rechts, stopindex="end",count=self.count2))
                start_index_rechts = f"{index_gesuchtes_wort_zielsprache}+{self.count2.get()}c"  # Der neue Start-Index nach dem gesuchten Wortes

        else:
            pass
