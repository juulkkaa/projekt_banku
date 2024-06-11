from tkinter import *
from tkinter import ttk 
import tkintermapview

from PlacowkaBanku import PlacowkaBanku


class StronaGlowna:
    def __init__(self):
        # GUI
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Projekt banku")
        self.root.geometry("1250x760")

        self.filtr_placowek = IntVar()

        ramka_dla_wyboru_wyswietlanych_elemntow = Frame(self.root)        
        ramka_dla_wyswietlanych_elementow = Frame(self.root)        
        self.ramka_dla_edycji_obiektow = Frame(self.root)    
        ramka_dla_mapy = Frame(self.root)

        ramka_dla_wyboru_wyswietlanych_elemntow.grid(row=0, column=0, padx=15)
        ramka_dla_wyswietlanych_elementow.grid(row=0, column=1)
        ramka_dla_mapy.grid(row=1, column=0, columnspan=3)

        # lista obiektów sekcji filtrow
        label_tytul_sekcji_filtrow = Label(ramka_dla_wyboru_wyswietlanych_elemntow, text="Aktualne zaaplikowane filtry")
        label_wybur_obiektow = Label(ramka_dla_wyboru_wyswietlanych_elemntow, text="Wybierz aktualnie wyświetlane elementy")
        self.wybor_aktualnych_obiektow = ttk.Combobox(ramka_dla_wyboru_wyswietlanych_elemntow, state="readonly",  
                                                      values=["Placówki Bankowe", "Pracownicy", "Klienci"], 
                                                      width=47)
        self.wybor_aktualnych_obiektow.current(0)
        checkbutton_ustaw_filtr = Checkbutton(ramka_dla_wyboru_wyswietlanych_elemntow, 
                                              text="Zaznacz aby filtrować placowki", onvalue=True, offvalue=False,
                                              variable=self.filtr_placowek)
        self.wybor_filtru_placowek = ttk.Combobox(ramka_dla_wyboru_wyswietlanych_elemntow, state="readonly",  values=[], width=47)


        label_tytul_sekcji_filtrow.grid(row=0, column=0, columnspan=2)
        label_wybur_obiektow.grid(row=1, column=0, columnspan=2)
        self.wybor_aktualnych_obiektow.grid(row=2, column=0, columnspan=2)
        checkbutton_ustaw_filtr.grid(row=3, column=0, columnspan=2)
        self.wybor_filtru_placowek.grid(row=4, column=0, columnspan=2)

        # lista obiektów sekcji filtrow
        label_tytul_sekcji_obiektow = Label(ramka_dla_wyswietlanych_elementow, text="Aktualne wyświetlane elementy -> Placówki Bankowe")
        self.wyswietlanie_obiektow = Listbox(ramka_dla_wyswietlanych_elementow, width=70) 

        label_tytul_sekcji_obiektow.grid(row=0, column=0, columnspan=4)
        self.wyswietlanie_obiektow.grid(row=1, column=0, columnspan=4)


        self.menu_wyboru_edycji()
        self.root.mainloop()


    def menu_wyboru_edycji(self):
        self.ramka_dla_edycji_obiektow.destroy()
        self.ramka_dla_edycji_obiektow = Frame(self.root) 
        self.ramka_dla_edycji_obiektow.grid(row=0, column=2, padx=160)

        # lista obiektów sekcji edycji
        przycisk_do_pokazania_na_mapie = Button(self.ramka_dla_edycji_obiektow, text="Pokaż na mapie", width=25)
        przycisk_do_dodawania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Dodaj nowy obiekt", 
                                               width=25, command=self.dodaj_nowy_obiekt)
        przycisk_do_usuwania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Usuń obiekt", width=25)
        przycisk_do_edycji_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Edytuj obiekt", 
                                            width=25, command=self.edytuj_obiekt)

        przycisk_do_pokazania_na_mapie.grid(row=0, column=0, pady=7)
        przycisk_do_dodawania_obiektu.grid(row=1, column=0, pady=7)
        przycisk_do_usuwania_obiektu.grid(row=2, column=0, pady=7)
        przycisk_do_edycji_obiektu.grid(row=3, column=0, pady=7)
        


    def dodaj_nowy_obiekt(self):
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                self.ramka_dla_edycji_obiektow = PlacowkaBanku(self.odswiez_widok).menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case "Pracownicy":
                print("2")
            case "Klienci":
                print("3")
            case default:
                print("Brak takiej opcji")
    

    def edytuj_obiekt(self):
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                    if f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        aktualny_obiekt.menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case "Pracownicy":
                print("2")
            case "Klienci":
                print("3")
            case default:
                print("Brak takiej opcji")


    def odswiez_widok(self):
        self.wyswietlanie_obiektow.delete(0, END)
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for idx, aktualny_obiekt in enumerate(PlacowkaBanku.lista_placowek_banku):
                    self.wyswietlanie_obiektow.insert(idx, 
                                                      f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}")
            case "Pracownicy":
                print("2")
            case "Klienci":
                print("3")
            case default:
                print("Brak takiej opcji")
        self.menu_wyboru_edycji()