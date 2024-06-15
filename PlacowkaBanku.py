from tkinter import * # Import biblioteki odpowiedzialnej za część graficzną
from geopy.geocoders import Nominatim # Import biblioteki do pobrania współrzędnych

# Do pobrania danych lokalizacji potrzebne jest ustawienie agenta
geolocator = Nominatim(user_agent="Chrome/104.0.5112.79") 


# Klasa dla PLacówek banku
class PlacowkaBanku:
    # Lista zawierająca wszystkie obiekty danej klasy
    lista_placowek_banku = []


    # Konstruktor
    def __init__(self, odswiez_widok):
        # Wstępne ustawienie danych
        self.odswiez_widok = odswiez_widok
        self.nazwa_placowki_banku = ''
        self.lokalizacja_placowki = ''
        self.koordynaty = [0, 0]


    # Widok dla edycji lub dodania nowego obiektu danej klasy
    def menu_edycji(self, ramka_dla_edycji_obiektow, root):
        ramka_dla_edycji_obiektow.destroy() # Usunięcie poprzedniego widoku po prawej stronie
        ramka_dla_edycji_obiektow = Frame(root) # Dodanie nowej ramki dla nowego menu
        ramka_dla_edycji_obiektow.grid(row=0, column=3, padx=10) # Ustawienie paraemtrów ramki
        
        # lista obiektów sekcji edycji
        gorny_napis = Label(ramka_dla_edycji_obiektow, text="Wprowadz dane nowej placowki")
        opis_do_nazwy = Label(ramka_dla_edycji_obiektow, text="Nazwa placówki: ")
        opis_do_lokalizacji = Label(ramka_dla_edycji_obiektow, text="Lokalizacja placówki: ")
        przycisk_porzucenia_edycji = Button(ramka_dla_edycji_obiektow, text="Powrót do menu", 
                                            width=15, command=self.odswiez_widok)
        przycisk_zapisania_obiektu = Button(ramka_dla_edycji_obiektow, text="Zapisz zmiany", 
                                            width=15, command=self.zapisz_zmiany)

        self.pole_nazwy_placowki = Entry(ramka_dla_edycji_obiektow, width=50)
        self.pole_lokalizacji_placowki = Entry(ramka_dla_edycji_obiektow, width=50)
        
        # Ustawienie obiektów w ramce
        gorny_napis.grid(row=0, column=0, columnspan=3)
        opis_do_nazwy.grid(row=1, column=0)
        opis_do_lokalizacji.grid(row=2, column=0)
        self.pole_nazwy_placowki.grid(row=1, column=1, columnspan=2)
        self.pole_lokalizacji_placowki.grid(row=2, column=1, columnspan=2)
        przycisk_porzucenia_edycji.grid(row=3, column=1)
        przycisk_zapisania_obiektu.grid(row=3, column=2)

        # Jeśli w danym obiekcie jest już wpisana nazwa banku to uzupełnij pole
        if self.nazwa_placowki_banku:
            self.pole_nazwy_placowki.insert(0, self.nazwa_placowki_banku)
        # Jeśli w danym obiekcie jest już wpisana lokalizacja to uzupełnij pole
        if self.lokalizacja_placowki:
            self.pole_lokalizacji_placowki.insert(0, self.lokalizacja_placowki)

        # Zwróć do głównego ekranu aktualną ramkę
        return ramka_dla_edycji_obiektow
    

    # Funkcja do zapisu danych po ich wprowazeniu
    def zapisz_zmiany(self):
        # Skopiuj dane z pól
        self.nazwa_placowki_banku = self.pole_nazwy_placowki.get()
        self.lokalizacja_placowki = self.pole_lokalizacji_placowki.get()

        # Pobierz koordynaty danego miejsca i zapisz nowe współrzędne
        nowe_koordynaty = geolocator.geocode(self.lokalizacja_placowki, timeout=10)
        self.koordynaty = []
        self.koordynaty.append(nowe_koordynaty.latitude)
        self.koordynaty.append(nowe_koordynaty.longitude)

        # Jeśli danej placówki nie ma na liście obiektów to go dorzuć
        if self not in PlacowkaBanku.lista_placowek_banku:
            PlacowkaBanku.lista_placowek_banku.append(self)

        # Odśwież widok na stronie głównej
        self.odswiez_widok()
        