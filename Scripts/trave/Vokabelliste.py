import tkinter as tk
import tkinter.scrolledtext as st
import DB_Kommunikation as db

# komplettes 2. Fenster wird innerhalb einer Klasse erstellt
class Vokabelliste:
    def __init__(self, fenster): #Der "fenster" Parameter ist nötig, um das Fenster aufzurufen (s. u.)

        #Variablen werden deklariert
        self.vokabel_ID = 0

        self.Fenster2 = tk.Toplevel(fenster) #Hier ist es wichtig, dass dem "Vokabellisten-Fenster als Parameter das 1. Fenster übergeben wird (s. o.)
        self.Fenster2.geometry("1300x1000")
        self.Fenster2.title("Vokabelliste")
        self.Fenster2.configure(bg="#181818")


        self.count = tk.StringVar() #Variable für das Markieren der gesuchten Vokabel

        #Variablen für Labels deklarieren
        self.vokabelzähler2 = tk.StringVar()
        self.vokabelzähler2.set("Insgesamt gibt es " + str(db.anzahl_vokabeln_insgesamt) + " verschiedene Vokabeln.")



        # Widgets werden erstellt
        self.Scrollbar = tk.Scrollbar(self.Fenster2)
        self.Scrollbar.place(x=610, y=150)
        self.Scrollbar.pack(side="right", fill="y")

        self.scroll_l=tk.Canvas(self.Fenster2, bg="green", width=200,height=1000)
        self.scroll_l.place(x=50,y=150)
        self.Vokabelanzeige_Latein = tk.Text(self.scroll_l, font=("Arial", 16), bg="#262626", fg="white", width=45, height=30)
        #self.Vokabelanzeige_Latein.place(x=50,y=150)
        self.Vokabelanzeige_Latein.pack()

        self.Vokabelanzeige_Deutsch = tk.Text(self.Fenster2, font=("Arial", 16), bg="#262626", fg="white", width=45, height=30, yscrollcommand=self.Scrollbar.set)
        self.Vokabelanzeige_Deutsch.place(x=650, y=150)



        self.Scrollbar.config(command=self.scrollen3)

        self.Vokabelanzeige_Deutsch.bind("<MouseWheel>", self.scrollen)
        self.Vokabelanzeige_Latein.bind("<MouseWheel>", self.scrollen)

        #self.scroll_l.bind("<MouseWheel>", self.scrollen)

        self.Fenster2.bind("<MouseWheel>", self.scrollen)
        #self.Vokabelanzeige_Deutsch.bind("<MouseWheel>", self.scrollen2)
        #self.Vokabelanzeige_Latein.bind("<MouseWheel>", self.scrollen2)
        #self.Vokabelanzeige_Deutsch.bind("<MouseWheel>", self.scrollen)
        #self.Vokabelanzeige_Latein.bind("<MouseWheel>", self.scrollen)
        #self.Fenster2.bind_all("<MouseWheel>", self.scrollen_verbieten)

        self.nächste_vokabelzeile = tk.Button(self.Fenster2, text="Nächste Zeile", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.nächste_vokabelzeile_anzeigen)
        self.nächste_vokabelzeile.place(x=450, y=30)

        self.alle_vokabeln_anzeigen = tk.Button(self.Fenster2, text="Alles anzeigen", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.alles_anzeigen)
        self.alle_vokabeln_anzeigen.place(x=700, y=30)

        self.Latein = tk.Label(self.Fenster2, text="Latein", font=("Arial", 16), bg="#262626", fg="white", width=15)
        self.Latein.place(x=100, y=100)

        self.Deutsch = tk.Label(self.Fenster2, text="Deutsch", font=("Arial", 16), bg="#262626", fg="white")
        self.Deutsch.place(x=700, y=100)

        self.vokabel_suchfeld = tk.Entry(self.Fenster2, font=("Arial", 16), bg="#262626", fg="white", width=15)
        self.vokabel_suchfeld.place(x=950, y=100)

        self.Suche = tk.Button(self.Fenster2, text="Vokabel suchen", font=("Arial", 16), bg="#262626", fg="white", width=15, command=self.Suchen)
        self.Suche.place(x=950, y=30)

        self.Zähler = tk.Label(self.Fenster2, textvariable=self.vokabelzähler2, font=("Arial", 16), bg="#262626", fg="white", width=35)
        self.Zähler.place(x=10, y=10)







    # Funktionen, welche durch Buttons ausgelöst werden, werden nachfolgend definiert:
    def scrollen_verbieten(self,event): #"event" wird der Funktion bei jeder Betätigung des Mausrades mit der x und y Koordinate des Cursors übergeben
        return 'break' #dadurch kann amn das Widget nciht mehr ohne Funktion scrollen

    def scrollen(self,event): #s.o.
        print(event.delta)
        self.Vokabelanzeige_Latein.yview_scroll(int(-1*(event.delta/120)), "units") #"event" übergibt neben x und y auch delta, welches durch das Vorzeichen angibt, in welche Richtung gescrollt wird (120 oder -120)
        self.Vokabelanzeige_Deutsch.yview_scroll(int(-1*(event.delta/120)), "units") #für die yview_scroll Funktion muss der Parameter (OS spezifisch)  abgeändert werden
        return "break"

    def scrollen2(self,event):
        self.Vokabelanzeige_Latein.yview_scroll(int((-1 * (event.delta / 120))/10),"units")  # "event" übergibt neben x und y auch delta, welches durch das Vorzeichen angibt, in welche Richtung gescrollt wird (120 oder -120)
        self.Vokabelanzeige_Deutsch.yview_scroll(int((-1 * (event.delta / 120))/2), "units")


    def scrollen3(self,*args):
        self.Vokabelanzeige_Latein.yview(*args)
        self.Vokabelanzeige_Deutsch.yview(*args)

    def nächste_vokabelzeile_anzeigen(self):

        if self.vokabel_ID < db.anzahl_vokabeln_insgesamt:
            self.vokabel_ID += 1
            self.Vokabelanzeige_Latein.insert("end", str(db.vokabel_latein(self.vokabel_ID)) + str(db.stammformen(db.vokabel_latein(self.vokabel_ID))) + "\n")
            self.Vokabelanzeige_Latein.see("end")
            self.Vokabelanzeige_Deutsch.insert("end", str(db.übersetzung(db.vokabel_latein(self.vokabel_ID))) + "\n")
            self.Vokabelanzeige_Deutsch.see("end")
            self.vokabelzähler2.set("Noch " + str(db.anzahl_vokabeln_insgesamt - self.vokabel_ID) + " Vokabeln.")
        else:
            self.vokabelzähler2.set("Das waren alle Vokabeln.")

    def alles_anzeigen(self):

        self.Vokabelanzeige_Deutsch.delete('1.0', "end")
        self.Vokabelanzeige_Latein.delete('1.0', "end")
        for i in range(1, db.anzahl_vokabeln_insgesamt + 1):
            self.Vokabelanzeige_Latein.insert("end", str(db.vokabel_latein(i)) + str(db.stammformen(db.vokabel_latein(i))) + "\n")
            self.Vokabelanzeige_Deutsch.insert("end", str(db.übersetzung(db.vokabel_latein(i))) + "\n")
        self.Vokabelanzeige_Latein.see("end")
        self.Vokabelanzeige_Deutsch.see("end")
        self.vokabelzähler2.set("Das waren alle Vokabeln.")

    def Suchen(self):
        wort = str(self.vokabel_suchfeld.get())
        self.vokabel_suchfeld.delete(0, "end")
        self.Vokabelanzeige_Latein.tag_remove('highlightline', 1.0, 'end')
        if wort != "" and not wort.isnumeric(): #Es muss nach Buchstaben gesucht werden
            self.Vokabelanzeige_Latein.tag_configure('highlightline', background='#737F00')
            start_index = "1.0"
            index_gesuchtes_wort = str(self.Vokabelanzeige_Latein.search(wort, start_index, stopindex="end", count=self.count))
            while index_gesuchtes_wort != "": #Durch eine while-Schleife werden alle Ergebnisse markiert + Fehlermeldungen, wenn die eingegebe Buchstabenkombination nicht existiert, verhindert
                self.Vokabelanzeige_Latein.tag_add('highlightline', index_gesuchtes_wort, f"{index_gesuchtes_wort}+{self.count.get()}c") #Durch die Count-Variable wird immer nur die eingegebene Buchstabenkombination markiert (s. o.)
                self.Vokabelanzeige_Latein.see(index_gesuchtes_wort)
                self.Vokabelanzeige_Deutsch.see(index_gesuchtes_wort)
                index_gesuchtes_wort = str(self.Vokabelanzeige_Latein.search(wort, start_index, stopindex="end", count=self.count))
                start_index = f"{index_gesuchtes_wort}+{self.count.get()}c"  # Der neue Start-Index nach dem gesuchten Wortes


        else:
            pass
