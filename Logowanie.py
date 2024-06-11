from tkinter import *

from StronaGlowna import StronaGlowna

class Logowanie:
    def __init__(self):

        self.dane_do_logowania = {
            "adam": "password",
            "zaneta": "passw0rd",
            "": ""
        }

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Projekt banku")
        self.root.geometry("300x180")

        opis_aplikacji = Label(self.root, text="Projekt do zarządzania bankiem wraz z jego oddziałami")
        self.opis_blednego_logowania = Label(self.root, text="")

        opis_przed_logowaniem = Label(self.root, text="Wstaw dane logownia:")

        napis_login = Label(self.root, text="Login: ")
        self.entry_do_loginu = Entry(self.root)
        napis_haslo = Label(self.root, text="Haslo: ")
        self.entry_do_hasla = Entry(self.root, show="*")

        zatwierdzenie_logowownaia = Button(self.root, text="Zaloguj", width=17, command=self.sprawdzenie_danych_logownaia)
        
        opis_aplikacji.grid(row=0, column=0, columnspan=2)
        opis_przed_logowaniem.grid(row=1, column=0)
        napis_login.grid(row=2, column=0)
        napis_haslo.grid(row=3, column=0)
        self.entry_do_loginu.grid(row=2, column=1)
        self.entry_do_hasla.grid(row=3, column=1)
        zatwierdzenie_logowownaia.grid(row=4, column=1)
        self.opis_blednego_logowania.grid(row=5, column=0)

        self.root.mainloop()
    

    def sprawdzenie_danych_logownaia(self):
        if self.entry_do_loginu.get() not in self.dane_do_logowania:
           self.opis_blednego_logowania.config(text="Błedy login lub hasło")
        elif self.dane_do_logowania[self.entry_do_loginu.get()] != self.entry_do_hasla.get():
            self.opis_blednego_logowania.config(text="Błedy login lub hasło")
        else:
            self.root.destroy()
            StronaGlowna()


