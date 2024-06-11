from tkinter import *

class PlacowkaBanku:
    lista_placowek_banku = []


    def __init__(self, odswiez_widok):
        self.odswiez_widok = odswiez_widok
        self.nazwa_placowki_banku = ''
        self.lokalizacja_placowki = ''
        self.koordynaty = [0, 0]

    def menu_edycji(self, ramka_dla_edycji_obiektow, root):
        ramka_dla_edycji_obiektow.destroy()
        ramka_dla_edycji_obiektow = Frame(root) 
        ramka_dla_edycji_obiektow.grid(row=0, column=3, padx=10)
        
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
        
        gorny_napis.grid(row=0, column=0, columnspan=3)
        opis_do_nazwy.grid(row=1, column=0)
        opis_do_lokalizacji.grid(row=2, column=0)
        self.pole_nazwy_placowki.grid(row=1, column=1, columnspan=2)
        self.pole_lokalizacji_placowki.grid(row=2, column=1, columnspan=2)
        przycisk_porzucenia_edycji.grid(row=3, column=1)
        przycisk_zapisania_obiektu.grid(row=3, column=2)

        if self.nazwa_placowki_banku:
            self.pole_nazwy_placowki.insert(0, self.nazwa_placowki_banku)
        if self.lokalizacja_placowki:
            self.pole_lokalizacji_placowki.insert(0, self.lokalizacja_placowki)

        return ramka_dla_edycji_obiektow
    

    def zapisz_zmiany(self):
        self.nazwa_placowki_banku = self.pole_nazwy_placowki.get()
        self.lokalizacja_placowki = self.pole_lokalizacji_placowki.get()

        if self not in PlacowkaBanku.lista_placowek_banku:
            PlacowkaBanku.lista_placowek_banku.append(self)

        self.odswiez_widok()
        