from tkinter import *
from tkinter import ttk 
import tkintermapview


class StronaGlowna:
    def __init__(self):
        # GUI
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Projekt banku")
        self.root.geometry("1024x760")

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


        self.medu_wyboru_edycji()
        self.root.mainloop()

    def medu_wyboru_edycji(self):
        self.ramka_dla_edycji_obiektow.destroy()
        self.ramka_dla_edycji_obiektow = Frame(self.root) 
        self.ramka_dla_edycji_obiektow.grid(row=0, column=2, padx=10)
        # lista obiektów sekcji edycji
        przycisk_do_pokazania_na_mapie = Button(self.ramka_dla_edycji_obiektow, text="Pokaż na mapie", width=25)
        przycisk_do_dodawania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Dodaj nowy obiekt", width=25)
        przycisk_do_usuwania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Usuń kierowce", width=25)
        przycisk_do_edycji_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Edytuj kierowce", width=25)

        przycisk_do_pokazania_na_mapie.grid(row=0, column=0, pady=7)
        przycisk_do_dodawania_obiektu.grid(row=1, column=0, pady=7)
        przycisk_do_usuwania_obiektu.grid(row=2, column=0, pady=7)
        przycisk_do_edycji_obiektu.grid(row=3, column=0, pady=7)
        
