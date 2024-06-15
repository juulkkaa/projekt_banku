from tkinter import * # Import części graficznej.

from StronaGlowna import StronaGlowna # Część główna aplikacji dostępna zaraz po zalogowaniu.

class Logowanie:
    # Konstruktor danej klasy.
    def __init__(self):

        # Spis wszystkich użytkowników danego programu.
        self.dane_do_logowania = {
            "adam": "password",
            "zaneta": "passw0rd"
        }

        # Część graficzna
        self.root = Tk() # Stworzenie nowego okienka
        self.root.resizable(False, False) # Zablokowanie zmiany rozmiaru okna
        self.root.title("Projekt banku") # Napis na górnej belce
        self.root.geometry("300x180") # rozmair okna

        # Opisy przed logowaniem
        opis_aplikacji = Label(self.root, text="Projekt do zarządzania bankiem wraz z jego oddziałami")
        self.opis_blednego_logowania = Label(self.root, text="")
        opis_przed_logowaniem = Label(self.root, text="Wstaw dane logownia:")

        # Pola i opisy do wprowadzenia danych logowania
        napis_login = Label(self.root, text="Login: ")
        self.entry_do_loginu = Entry(self.root)
        napis_haslo = Label(self.root, text="Haslo: ")
        self.entry_do_hasla = Entry(self.root, show="*")

        # Przycisk do zalogowania
        zatwierdzenie_logowownaia = Button(self.root, text="Zaloguj", width=17, command=self.sprawdzenie_danych_logownaia)
        
        # Ustawienie obiektów w oknie
        opis_aplikacji.grid(row=0, column=0, columnspan=2)
        opis_przed_logowaniem.grid(row=1, column=0)
        napis_login.grid(row=2, column=0)
        napis_haslo.grid(row=3, column=0)
        self.entry_do_loginu.grid(row=2, column=1)
        self.entry_do_hasla.grid(row=3, column=1)
        zatwierdzenie_logowownaia.grid(row=4, column=1)
        self.opis_blednego_logowania.grid(row=5, column=0)

        self.root.mainloop() # Pokazanie okienka
    

    # Dana funkcja służy do sprawdzenia danych logowania. Jeśli są poprawne to uruchomi główną część aplikacji.
    def sprawdzenie_danych_logownaia(self):
        # Jeśli podany login nie istnieje to ustaw taką informację.
        if self.entry_do_loginu.get() not in self.dane_do_logowania:
           self.opis_blednego_logowania.config(text="Błedy login lub hasło")
        # Jeśli podany login istnieje, ale hasło się nie jest poprawne to ustaw taką informację.
        elif self.dane_do_logowania[self.entry_do_loginu.get()] != self.entry_do_hasla.get():
            self.opis_blednego_logowania.config(text="Błedy login lub hasło")
        # Jeśli podane poświadczenia są poprawne to uruchom część główną aplikacji.
        else:
            self.root.destroy()
            StronaGlowna()


