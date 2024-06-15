from tkinter import * # Import biblioteki odpowiedzialnej za część graficzną
from tkinter import ttk  # Import biblioteki odpowiedzialnej za dodatkowe elementy graficzne
from geopy.geocoders import Nominatim # Import biblioteki do pobrania współrzędnych

from PlacowkaBanku import PlacowkaBanku # Import Placówek banku

# Do pobrania danych lokalizacji potrzebne jest ustawienie agenta
geolocator = Nominatim(user_agent="Chrome/104.0.5112.79") 


# Klasa dla pacowników banku banku
class PracownikBanku:
    # Lista zawierająca wszystkie obiekty danej klasy
    lista_pracownikow_banku = []


    # Konstruktor
    def __init__(self, odswiez_widok):
        self.odswiez_widok = odswiez_widok
        self.imie_pracownika = ''
        self.nazwisko_pracownika = ''
        self.lokalizacja_pracownika = ''
        self.nazwa_banku = ''
        self.koordynaty = [0, 0]


    # Widok dla edycji lub dodania nowego obiektu danej klasy
    def menu_edycji(self, ramka_dla_edycji_obiektow, root):
        ramka_dla_edycji_obiektow.destroy() # Usunięcie poprzedniego widoku po prawej stronie
        ramka_dla_edycji_obiektow = Frame(root) # Dodanie nowej ramki dla nowego menu
        ramka_dla_edycji_obiektow.grid(row=0, column=3, padx=10) # Ustawienie paraemtrów ramki

        # Pobierz nazwy wszystkich banków i zrób z tego listę do wyboru.
        lista_do_wyboru_bankow = []
        for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
            lista_do_wyboru_bankow.append(f"{aktualny_obiekt.nazwa_placowki_banku}")
   
        # lista obiektów sekcji edycji
        gorny_napis = Label(ramka_dla_edycji_obiektow, text="Wprowadz dane nowego pracownika")
        opis_do_imienia = Label(ramka_dla_edycji_obiektow, text="Imię pracownika: ")
        opis_do_nazwiska = Label(ramka_dla_edycji_obiektow, text="Nazwisko pracownika: ")
        opis_do_lokalizacji = Label(ramka_dla_edycji_obiektow, text="Lokalizacja pracownika: ")
        opis_do_banku = Label(ramka_dla_edycji_obiektow, text="Przypisany bank: ")
        self.wybor_banku = ttk.Combobox(ramka_dla_edycji_obiektow, state="readonly",  
                                                      values=lista_do_wyboru_bankow, width=47)
        przycisk_porzucenia_edycji = Button(ramka_dla_edycji_obiektow, text="Powrót do menu", 
                                            width=15, command=self.odswiez_widok)
        przycisk_zapisania_obiektu = Button(ramka_dla_edycji_obiektow, text="Zapisz zmiany", 
                                            width=15, command=self.zapisz_zmiany)

        self.pole_imie = Entry(ramka_dla_edycji_obiektow, width=50)
        self.pole_nazwisko = Entry(ramka_dla_edycji_obiektow, width=50)
        self.pole_lokalizacji_pracownika = Entry(ramka_dla_edycji_obiektow, width=50)
        
        # Ustawienie obiektów w oknie
        gorny_napis.grid(row=0, column=0, columnspan=3)
        opis_do_imienia.grid(row=1, column=0)
        opis_do_nazwiska.grid(row=2, column=0)
        opis_do_lokalizacji.grid(row=3, column=0)
        opis_do_banku.grid(row=4, column=0)
        self.pole_imie.grid(row=1, column=1, columnspan=2)
        self.pole_nazwisko.grid(row=2, column=1, columnspan=2)
        self.pole_lokalizacji_pracownika.grid(row=3, column=1, columnspan=2)
        self.wybor_banku.grid(row=4, column=1, columnspan=2)
        przycisk_porzucenia_edycji.grid(row=5, column=1)
        przycisk_zapisania_obiektu.grid(row=5, column=2)

        # Jeśli jest dostępne imię to ustaw odpowiednie pole
        if self.imie_pracownika:
            self.pole_imie.insert(0, self.imie_pracownika)
        # Jeśli jest dostępne nazwisko to ustaw odpowiednie pole
        if self.nazwisko_pracownika:
            self.pole_nazwisko.insert(0, self.nazwisko_pracownika)
        # Jeśli jest dosępna lokalizacja to ustaw odpowiednie pole
        if self.lokalizacja_pracownika:
            self.pole_lokalizacji_pracownika.insert(0, self.lokalizacja_pracownika)
        # Jeśli jest dosępna placówka banku to zaznacz odpowiedni
        if self.nazwa_banku:
            for idx,  aktualny_bank in enumerate(lista_do_wyboru_bankow):
                if aktualny_bank == self.nazwa_banku:
                    self.wybor_banku.current(idx)
                    break
        
        # Zwróć nowy widok
        return ramka_dla_edycji_obiektow
    

    # Widok dla edycji lub dodania nowego obiektu danej klasy
    def zapisz_zmiany(self):
        # Skopiuj dane z pól
        self.imie_pracownika = self.pole_imie.get()
        self.nazwisko_pracownika = self.pole_nazwisko.get()
        self.lokalizacja_pracownika = self.pole_lokalizacji_pracownika.get()
        self.nazwa_banku = self.wybor_banku.get()

        # Pobierz koordynaty danego miejsca i zapisz nowe współrzędne
        nowe_koordynaty = geolocator.geocode(self.lokalizacja_pracownika, timeout=10)
        self.koordynaty = []
        self.koordynaty.append(nowe_koordynaty.latitude)
        self.koordynaty.append(nowe_koordynaty.longitude)

        # Jeśli danej placówki nie ma na liście obiektów to go dorzuć
        if self not in PracownikBanku.lista_pracownikow_banku:
            PracownikBanku.lista_pracownikow_banku.append(self)

        # Odśwież widok na stronie głównej
        self.odswiez_widok()
        