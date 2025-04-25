import Vokabeltrainer
import tkinter as tk
import tools as tools

class auswahlmenue:
    """
    GUI class to display a language selection menu for a vocabulary trainer.

    This class creates a Tkinter-based graphical user interface (GUI) with options
    to start a vocabulary training session in different languages. The available
    languages are Latin, English, French, and Ancient Greek. The user can select
    a language and start the training session for that language.
    """
    
    def __init__(self):
        """
        Initializes the main window and GUI components.

        This constructor sets up the Tkinter window, adjusts its size and position
        to center it on the screen, and creates labels and buttons for the selection menu.
        """
        self.x = 0
        self.Fenster0 = tk.Tk()
        self.Fenster0.title("Auswahlmenü")
        self.Fenster0.iconbitmap((tools.find_source_path("Translation.ico")))
        self.Hoehe_Fenster = 800
        self.Breite_Fenster = 800
        self.Breite_Monitor = self.Fenster0.winfo_screenwidth()
        self.Hoehe_Monitor = self.Fenster0.winfo_screenheight()
        self.x = (self.Breite_Monitor / 2) - (self.Breite_Fenster / 2)
        self.y = (self.Hoehe_Monitor / 2) - (self.Hoehe_Fenster / 2)
        self.Fenster0.geometry(f"{self.Breite_Fenster}x{self.Hoehe_Fenster}+{int(self.x)}+{int(self.y)}")
        self.Fenster0.configure(bg="#181818")

        self.label = tk.Label(self.Fenster0, font=("Arial", 20), bg="#262626", fg="white",text = "Willkommen beim Vokabeltrainer\nBitte wähle eine Sprache aus.")
        self.label.place(x=200,y=50)
        self.button_latein = tk.Button(self.Fenster0, font=("Arial", 20), bg="#262626", fg="white", text = "Latein-Deutsch", command = self.latein_starten)
        self.button_latein.place(x=50,y=200)
        self.button_englisch = tk.Button(self.Fenster0, font=("Arial", 20), bg="#262626", fg="white", text ="Deutsch-Englisch", command = self.englisch_starten)
        self.button_englisch.place(x=400,y=200)
        self.button_franzoesisch = tk.Button(self.Fenster0, font=("Arial", 20), bg="#262626", fg="white",text="Deutsch-Französisch", command=self.franzoesisch_starten)
        self.button_franzoesisch.place(x=50, y=400)
        self.button_altgriechisch = tk.Button(self.Fenster0, font=("Arial", 20), bg="#262626", fg="white", text="Deutsch-Altgriechisch", command=self.altgriechisch_starten)
        self.button_altgriechisch.place(x=400, y=400)

    def start(self):
        """
        Starts the Tkinter main loop.

        This method launches the GUI and waits for user interaction with the buttons.
        """
        self.Fenster0.mainloop()
        self.x = 1

    def latein_starten(self):
        """
        Starts the Latin vocabulary trainer.

        This method closes the current window and initializes the Latin vocabulary trainer.
        """
        self.Fenster0.destroy()
        Vokabeltrainer.Vokabeltrainer("Latein",["Latein","Deutsch"]).start()

    def englisch_starten(self):
        """
        Starts the English vocabulary trainer.

        This method closes the current window and initializes the English vocabulary trainer.
        """
        self.Fenster0.destroy()
        Vokabeltrainer.Vokabeltrainer("Englisch", ["Deutsch", "Englisch"]).start()

    def franzoesisch_starten(self):
        """
        Starts the French vocabulary trainer.

        This method closes the current window and initializes the French vocabulary trainer.
        """
        self.Fenster0.destroy()
        Vokabeltrainer.Vokabeltrainer("Franzoesisch", ["Deutsch", "Franzoesisch"]).start()

    def altgriechisch_starten(self):
        """
        Starts the Ancient Greek vocabulary trainer.

        This method closes the current window and initializes the Ancient Greek vocabulary trainer.
        """
        self.Fenster0.destroy()
        Vokabeltrainer.Vokabeltrainer("Altgriechisch", ["Deutsch", "Altgriechisch"]).start()

# Start the application
auswahlmenue().start()