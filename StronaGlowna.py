# W danym pliku znajduje się całe serce programu. Główny widok obiektów wraz z interaktywną mapą.

from tkinter import * # Import biblioteki odpowiedzialnej za część graficzną
from tkinter import ttk  # Import biblioteki odpowiedzialnej za dodatkowe elementy graficzne
from geopy.geocoders import Nominatim # Import biblioteki do pobrania współrzędnych
import tkintermapview # Import biblioteki mapy

# import klas odpowiedzialnych za placówki banku, pracowników banku oraz o klientów
from PlacowkaBanku import PlacowkaBanku
from PracownikBanku import PracownikBanku
from KlientBanku import KlientBanku

# Do pobrania danych lokalizacji potrzebne jest ustawienie agenta
geolocator = Nominatim(user_agent="Chrome/104.0.5112.79") 


# Główna klasa aplikacji
class StronaGlowna:
    def __init__(self):
        # GUI
        self.root = Tk() # Stworzenie nowego okienka
        self.root.resizable(False, False) # Zablokowanie zmiany rozmiaru okna
        self.root.title("Projekt banku") # Napis na górnej belce
        self.root.geometry("1300x760") # rozmair okna

        # Zmienna dla włączania i wyłączania filtru placówek bankowych
        self.filtr_placowek = IntVar()

        # Ramki dla łatwiejszego ułożenia elementów na stronie
        ramka_dla_wyboru_wyswietlanych_elemntow = Frame(self.root)        
        ramka_dla_wyswietlanych_elementow = Frame(self.root)        
        self.ramka_dla_edycji_obiektow = Frame(self.root)    
        ramka_dla_mapy = Frame(self.root)

        # Ustawienie położenia ramek na stronie
        ramka_dla_wyboru_wyswietlanych_elemntow.grid(row=0, column=0, padx=15)
        ramka_dla_wyswietlanych_elementow.grid(row=0, column=1)
        ramka_dla_mapy.grid(row=1, column=0, columnspan=5, pady=20, padx=0)

        # lista obiektów sekcji filtrow
        label_tytul_sekcji_filtrow = Label(ramka_dla_wyboru_wyswietlanych_elemntow, text="Aktualne zaaplikowane filtry")
        label_wybur_obiektow = Label(ramka_dla_wyboru_wyswietlanych_elemntow, text="Wybierz aktualnie wyświetlane elementy")
        self.wybor_aktualnych_obiektow = ttk.Combobox(ramka_dla_wyboru_wyswietlanych_elemntow, state="readonly",  
                                                      values=["Placówki Bankowe", "Pracownicy", "Klienci"], 
                                                      width=47)
        # Podłączenie akcji po wywołaniu wydarzenia zmiany aktualnie wyświetlanych elementów
        self.wybor_aktualnych_obiektow.bind("<<ComboboxSelected>>", lambda _ : self.odswiez_widok())
        self.wybor_aktualnych_obiektow.current(0) # Ustawienie, że na początku mają się wyświetlić placówki banku
    
        self.checkbutton_ustaw_filtr = Checkbutton(ramka_dla_wyboru_wyswietlanych_elemntow, 
                                              text="Zaznacz aby filtrować placowki", onvalue=True, offvalue=False,
                                              variable=self.filtr_placowek, state=DISABLED, command=self.odswiez_widok)
        self.wybor_filtru_placowek = ttk.Combobox(ramka_dla_wyboru_wyswietlanych_elemntow, state="disabled",  values=[], width=47)
        self.wybor_filtru_placowek.bind("<<ComboboxSelected>>", lambda _ : self.odswiez_widok())

        # ustawienie obiektów na mapie
        label_tytul_sekcji_filtrow.grid(row=0, column=0, columnspan=2)
        label_wybur_obiektow.grid(row=1, column=0, columnspan=2)
        self.wybor_aktualnych_obiektow.grid(row=2, column=0, columnspan=2)
        self.checkbutton_ustaw_filtr.grid(row=3, column=0, columnspan=2)
        self.wybor_filtru_placowek.grid(row=4, column=0, columnspan=2)

        # lista obiektów sekcji filtrow
        label_tytul_sekcji_obiektow = Label(ramka_dla_wyswietlanych_elementow, text="Lista aktualnych obiektów")
        self.wyswietlanie_obiektow = Listbox(ramka_dla_wyswietlanych_elementow, width=70) 

        label_tytul_sekcji_obiektow.grid(row=0, column=0, columnspan=4)
        self.wyswietlanie_obiektow.grid(row=1, column=0, columnspan=4)

        # Wygenerowanie przykładowych danych Placówek banku, pracowników banków i klientów
        self.obiekty_domyslne()

        # Dodanie mapy do widoku
        self.map_widget = tkintermapview.TkinterMapView(ramka_dla_mapy, width=1000, height=430)
        self.map_widget.set_position(52.2, 21.0)
        self.map_widget.set_zoom(8)
        self.map_widget.grid(row=0, column=0)

        # Podpięcie akcji jaka ma się wywołać po kliknięciu prawym przyciskiem na mapie
        self.map_widget.add_right_click_menu_command(label="Dodaj nową placówkę banku",
                                command=self.dodaj_bank_z_mapy,
                                pass_coords=True)

        # Odświeżenie danych w okienku
        self.odswiez_widok()
        self.root.mainloop()


    # Funkcja do wygenerowania prawej części GUI
    def menu_wyboru_edycji(self):
        self.ramka_dla_edycji_obiektow.destroy()  # Usunięcie poprzedniego widoku po prawej stronie
        self.ramka_dla_edycji_obiektow = Frame(self.root) # Dodanie nowej ramki dla nowego menu
        self.ramka_dla_edycji_obiektow.grid(row=0, column=2, padx=160) # Ustawienie paraemtrów ramki

        # lista obiektów sekcji edycji
        przycisk_do_pokazania_na_mapie_wszystkich = Button(self.ramka_dla_edycji_obiektow, text="Pokaż wszystkie obiekty na mapie", 
                                                           width=30, command=self.pokaz_wszystkich)
        przycisk_do_pokazania_na_mapie_wybrany = Button(self.ramka_dla_edycji_obiektow, text="Pokaż zaznaczony obiekt na mapie", 
                                                        width=30, command=self.pokaz_konkretny_obiekt)
        przycisk_do_dodawania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Dodaj nowy obiekt", 
                                               width=30, command=self.dodaj_nowy_obiekt)
        przycisk_do_usuwania_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Usuń obiekt", 
                                              width=30, command=self.usun_obiekt)
        przycisk_do_edycji_obiektu = Button(self.ramka_dla_edycji_obiektow, text="Edytuj obiekt", 
                                            width=30, command=self.edytuj_obiekt)
        # Ustawienie obiektów w oknie
        przycisk_do_pokazania_na_mapie_wszystkich.grid(row=0, column=0, columnspan=3, pady=7)
        przycisk_do_pokazania_na_mapie_wybrany.grid(row=1, column=0, columnspan=3, pady=7)
        przycisk_do_dodawania_obiektu.grid(row=2, column=0, columnspan=3, pady=7)
        przycisk_do_usuwania_obiektu.grid(row=3, column=0, columnspan=3, pady=7)
        przycisk_do_edycji_obiektu.grid(row=4, column=0, columnspan=3, pady=7)
        

    # Funkcja odpowiedzialna za dodawanie nowych obiektów klasy Placówek banku, pracowników i klientów
    def dodaj_nowy_obiekt(self):
        # Sprawdź jakie obiekty są teraz wyświetlane i stwórz obiekt odpowiedniej klasy
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                self.ramka_dla_edycji_obiektow = PlacowkaBanku(self.odswiez_widok).menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case "Pracownicy":
                self.ramka_dla_edycji_obiektow = PracownikBanku(self.odswiez_widok).menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case "Klienci":
                self.ramka_dla_edycji_obiektow = KlientBanku(self.odswiez_widok).menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case default:
                print("Brak takiej opcji")
    

    # Funkcja do obsługi dodania nowej placówki za pomocą prawego przycisku myszy na mapie
    def dodaj_bank_z_mapy(self, koordynaty):
        pb_1 = PlacowkaBanku(self.odswiez_widok) # Stwórz nowy obiekt
        znaleziony_adres = geolocator.reverse(koordynaty, timeout=10) # Zamień koordynaty na lokalizację
        pb_1.lokalizacja_placowki =  znaleziony_adres.address # Uzupełnij lokalizację obiektu
        pb_1.koordynaty = [koordynaty[0], koordynaty[1]] # Uzupełnij koordynaty
        self.ramka_dla_edycji_obiektow = pb_1.menu_edycji(self.ramka_dla_edycji_obiektow, self.root) # Otwórz edycję obiektu
     

    # Funkcja do obsługi edycji istniejących już obiektów
    def edytuj_obiekt(self):
        # Znajdź które obiekty są teraz wyświetlone.
        # Natępnie znajdź obiekt który zawiera takie same dane jak zaznaczony obiekt
        # Na koniec wywołaj funkcję odpowiedzialną za pokazanie menu edycji obiektu
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                    if f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        self.ramka_dla_edycji_obiektow = aktualny_obiekt.menu_edycji(self.ramka_dla_edycji_obiektow, self.root)
            case "Pracownicy":
                for aktualny_obiekt in PracownikBanku.lista_pracownikow_banku:
                    if f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}, " \
                       f"{aktualny_obiekt.lokalizacja_pracownika}, {aktualny_obiekt.nazwa_banku}" == \
                          self.wyswietlanie_obiektow.get(ACTIVE):
                        self.ramka_dla_edycji_obiektow = aktualny_obiekt.menu_edycji(self.ramka_dla_edycji_obiektow, self.root)            
            case "Klienci":
                for aktualny_obiekt in KlientBanku.lista_klientow_banku:
                    if f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}, " \
                       f"{aktualny_obiekt.lokalizacja_klienta}, {aktualny_obiekt.nazwa_banku}" == \
                          self.wyswietlanie_obiektow.get(ACTIVE):
                        self.ramka_dla_edycji_obiektow = aktualny_obiekt.menu_edycji(self.ramka_dla_edycji_obiektow, self.root)            
            case default:
                print("Brak takiej opcji")


    # Funkcja do usuwania obiektów
    def usun_obiekt(self):
        # Znajdź które obiekty są teraz wyświetlone.
        # Natępnie znajdź obiekt który zawiera takie same dane jak zaznaczony obiekt
        # Po znalezieniu usuń go z listy obiektów
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                    if f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        PlacowkaBanku.lista_placowek_banku.remove(aktualny_obiekt)
                        break
            case "Pracownicy":
                for aktualny_obiekt in PracownikBanku.lista_pracownikow_banku:
                    if f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}, " \
                       f"{aktualny_obiekt.lokalizacja_pracownika}, {aktualny_obiekt.nazwa_banku}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        PracownikBanku.lista_pracownikow_banku.remove(aktualny_obiekt)
                        break
            case "Klienci":
                for aktualny_obiekt in KlientBanku.lista_klientow_banku:
                    if f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}, " \
                       f"{aktualny_obiekt.lokalizacja_klienta}, {aktualny_obiekt.nazwa_banku}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        KlientBanku.lista_klientow_banku.remove(aktualny_obiekt)
                        break
            case default:
                print("Brak takiej opcji")
        
        self.odswiez_widok()


    # Funkcja do pokazania obecnie wylistowanych obiektów na mapie
    def pokaz_wszystkich(self):
        self.map_widget.delete_all_marker() # Usuń poprzednie znaczki

        # Znajdź które obiekty są teraz wyświetlone.
        # Sprawdź czy filtr jest wyłączony lub czy placówka jest zgodna z filtrem.
        # Pobierz koordynaty z obiektu i dodaj na mapie
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                    self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                         aktualny_obiekt.koordynaty[1],
                                         marker=True, 
                                         text=aktualny_obiekt.nazwa_placowki_banku)
            case "Pracownicy":
                for aktualny_obiekt in PracownikBanku.lista_pracownikow_banku:
                    if not self.filtr_placowek.get() or aktualny_obiekt.nazwa_banku == self.wybor_filtru_placowek.get():
                        self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                            aktualny_obiekt.koordynaty[1],
                                            marker=True, 
                                            text=f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}")
            case "Klienci":
                for aktualny_obiekt in KlientBanku.lista_klientow_banku:
                    if not self.filtr_placowek.get() or aktualny_obiekt.nazwa_banku == self.wybor_filtru_placowek.get():
                        self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                            aktualny_obiekt.koordynaty[1],
                                            marker=True, 
                                            text=f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}")
            case default:
                print("Brak takiej opcji")

        self.map_widget.set_zoom(14)


    # Zadaniem funkcji jest pokazanie obiecnie zaznaczonego obiektu    
    def pokaz_konkretny_obiekt(self):
        self.map_widget.delete_all_marker() # Usuń poprzednie znaczki

        # Znajdź które obiekty są teraz wyświetlone.
        # Znajdź który obiekt został właśnie zaznaczony dodaj go do mapy i zamknij funkcję.
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                    if f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                            aktualny_obiekt.koordynaty[1],
                                            marker=True, 
                                            text=aktualny_obiekt.nazwa_placowki_banku)
                        break
            case "Pracownicy":
                for aktualny_obiekt in PracownikBanku.lista_pracownikow_banku:
                    if f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}, " \
                       f"{aktualny_obiekt.lokalizacja_pracownika}, {aktualny_obiekt.nazwa_banku}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                            aktualny_obiekt.koordynaty[1],
                                            marker=True, 
                                            text=f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}")
                        break
            case "Klienci":
                for aktualny_obiekt in KlientBanku.lista_klientow_banku:
                    if f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}, " \
                       f"{aktualny_obiekt.lokalizacja_klienta}, {aktualny_obiekt.nazwa_banku}" == \
                                                                    self.wyswietlanie_obiektow.get(ACTIVE):
                        self.map_widget.set_position(aktualny_obiekt.koordynaty[0], 
                                            aktualny_obiekt.koordynaty[1],
                                            marker=True, 
                                            text=f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}")
                        break
            case default:
                print("Brak takiej opcji")

        self.map_widget.set_zoom(20) # Ustaw przybliżenie na obiekt


    # Zadaniem tej funkcji jest uaktualnienie danych jakie są aktualnie wyświetlane w okienku
    def odswiez_widok(self):
        self.wyswietlanie_obiektow.delete(0, END) # usuń wszystkie obiekty z listy obiektów
        self.map_widget.delete_all_marker() # Usuń wszystkie znaczki na mapie
        

        ustawiona_placowka = '' # Zmienna do przechowywania aktualnie wyfiltrowanej placówki bankowej.
        # Jeśli filtr placówek jest załącozny to:
        if self.filtr_placowek.get():
            self.wybor_filtru_placowek.config(state="readonly") # Odblokuj pole wyboru placówki
            ustawiona_placowka = self.wybor_filtru_placowek.get() # Pobierz aktualnie ustawioną placówkę

            # Stworzenie listy ze wszystkich nazw banku
            lista_do_wyboru_bankow = []
            for aktualny_obiekt in PlacowkaBanku.lista_placowek_banku:
                lista_do_wyboru_bankow.append(f"{aktualny_obiekt.nazwa_placowki_banku}")
            self.wybor_filtru_placowek.config(values=lista_do_wyboru_bankow)

            # Jeśli aktualnie jest wybrana placówka to ustaw taki filtr. Jeśli nie to wybierz pierwszy element z listy
            if ustawiona_placowka:
                for idx,  aktualny_bank in enumerate(lista_do_wyboru_bankow):
                    if aktualny_bank == ustawiona_placowka:
                        self.wybor_filtru_placowek.current(idx)
                        break
            elif self.filtr_placowek.get():
                self.wybor_filtru_placowek.current(0)
                ustawiona_placowka = self.wybor_filtru_placowek.get()

        # Jeśli filtr jest wyłączony to wyłącz też pole wyboru placówek i usuń dane z pola
        else:
            self.wybor_filtru_placowek.config(state="disabled", values=[''])
            self.wybor_filtru_placowek.current(0)

        # Znajdź które obiekty są teraz wyświetlone.
        # Sprawdź czy filtr jest wyłączony lub czy placówka jest zgodna z filtrem.
        # Dodaj do listy aktualnie wyświetlanych obiektów
        match self.wybor_aktualnych_obiektow.get():
            case "Placówki Bankowe":
                self.checkbutton_ustaw_filtr.config(state=DISABLED)
                for idx, aktualny_obiekt in enumerate(PlacowkaBanku.lista_placowek_banku):
                    self.wyswietlanie_obiektow.insert(idx, 
                                                      f"{aktualny_obiekt.nazwa_placowki_banku}, {aktualny_obiekt.lokalizacja_placowki}")
            case "Pracownicy":
                self.checkbutton_ustaw_filtr.config(state=ACTIVE)
                for idx, aktualny_obiekt in enumerate(PracownikBanku.lista_pracownikow_banku):
                    if not self.filtr_placowek.get() or aktualny_obiekt.nazwa_banku == ustawiona_placowka:
                        self.wyswietlanie_obiektow.insert(idx, 
                                                        f"{aktualny_obiekt.imie_pracownika} {aktualny_obiekt.nazwisko_pracownika}, "+ 
                                                        f"{aktualny_obiekt.lokalizacja_pracownika}, {aktualny_obiekt.nazwa_banku}")
            case "Klienci":
                self.checkbutton_ustaw_filtr.config(state=ACTIVE)
                for idx, aktualny_obiekt in enumerate(KlientBanku.lista_klientow_banku):
                    if not self.filtr_placowek.get() or aktualny_obiekt.nazwa_banku == ustawiona_placowka:
                        self.wyswietlanie_obiektow.insert(idx, 
                                                        f"{aktualny_obiekt.imie_klienta} {aktualny_obiekt.nazwisko_klienta}, "+ 
                                                        f"{aktualny_obiekt.lokalizacja_klienta}, {aktualny_obiekt.nazwa_banku}")
            case default:
                print("Brak takiej opcji")
        self.menu_wyboru_edycji() # Uruchom funkcję do restartu sekcji 3 w okienku


# Funkcja do dodania wstępnych danych
    def obiekty_domyslne(self):
        pb_1 = PlacowkaBanku(self.odswiez_widok)
        pb_1.nazwa_placowki_banku = "Bank Polski - Dusigrosz"
        pb_1.lokalizacja_placowki = "Targ Sienny 7, 80-806 Gdańsk"
        pb_1.koordynaty = [54.349348, 18.6429306]
        PlacowkaBanku.lista_placowek_banku.append(pb_1)

        pb_2 = PlacowkaBanku(self.odswiez_widok)
        pb_2.nazwa_placowki_banku = "Bank Powszechny - Bocian"
        pb_2.lokalizacja_placowki = "Schuberta 102A, 80-172 Gdańsk"
        pb_2.koordynaty = [54.3523661, 18.5925228]
        PlacowkaBanku.lista_placowek_banku.append(pb_2)

        pb_3 = PlacowkaBanku(self.odswiez_widok)
        pb_3.nazwa_placowki_banku = "Bank Prywatny - lichwiarz"
        pb_3.lokalizacja_placowki = "aleja Grunwaldzka 141, 80-264 Gdańsk"
        pb_3.koordynaty = [54.38208935, 18.600324618432275]
        PlacowkaBanku.lista_placowek_banku.append(pb_3)

        prac_b_1 = PracownikBanku(self.odswiez_widok)
        prac_b_1.imie_pracownika = "Zbigniew"
        prac_b_1.nazwisko_pracownika = "Lasocki"
        prac_b_1.lokalizacja_pracownika = "Stągiewna 8, 80-750 Gdańsk"
        prac_b_1.nazwa_banku = "Bank Polski - Dusigrosz"
        prac_b_1.koordynaty = [54.3473731, 18.6581633]
        PracownikBanku.lista_pracownikow_banku.append(prac_b_1)

        prac_b_2 = PracownikBanku(self.odswiez_widok)
        prac_b_2.imie_pracownika = "Magda"
        prac_b_2.nazwisko_pracownika = "Wysocka"
        prac_b_2.lokalizacja_pracownika = "Czerwony Dwór 27, 80-980 Gdańsk"
        prac_b_2.nazwa_banku = "Bank Powszechny - Bocian"
        prac_b_2.koordynaty = [54.4119888, 18.586955]
        PracownikBanku.lista_pracownikow_banku.append(prac_b_2)

        prac_b_3 = PracownikBanku(self.odswiez_widok)
        prac_b_3.imie_pracownika = "Monika"
        prac_b_3.nazwisko_pracownika = "Zawadzka"
        prac_b_3.lokalizacja_pracownika = "Rajska 2, 80-850 Gdańsk"
        prac_b_3.nazwa_banku = "Bank Prywatny - lichwiarz"
        prac_b_3.koordynaty = [54.3547776, 18.6509751549144]
        PracownikBanku.lista_pracownikow_banku.append(prac_b_3)

        kb_1 = KlientBanku(self.odswiez_widok)
        kb_1.imie_klienta = "Lucjan"
        kb_1.nazwisko_klienta = "Bojaczyk"
        kb_1.lokalizacja_klienta = "Hynka 8, 80-465 Gdańsk"
        kb_1.nazwa_banku = "Bank Polski - Dusigrosz"
        kb_1.koordynaty = [54.38777005, 18.604410076339917]
        KlientBanku.lista_klientow_banku.append(kb_1)

        kb_2 = KlientBanku(self.odswiez_widok)
        kb_2.imie_klienta = "Marcin"
        kb_2.nazwisko_klienta = "Pazura"
        kb_2.lokalizacja_klienta = "Powstania Listopadowego 2F, 80-287 Gdańsk"
        kb_2.nazwa_banku = "Bank Polski - Dusigrosz"
        kb_2.koordynaty = [54.3553782, 18.5777807]
        KlientBanku.lista_klientow_banku.append(kb_2)

        kb_3 = KlientBanku(self.odswiez_widok)
        kb_3.imie_klienta = "Wojciech"
        kb_3.nazwisko_klienta = "Grab"
        kb_3.lokalizacja_klienta = "Aleja Rzeczypospolitej 21B, 80-462 Gdańsk"
        kb_3.nazwa_banku = "Bank Powszechny - Bocian"
        kb_3.koordynaty = [54.3928814, 18.6055271]
        KlientBanku.lista_klientow_banku.append(kb_3)

        kb_4 = KlientBanku(self.odswiez_widok)
        kb_4.imie_klienta = "Ola"
        kb_4.nazwisko_klienta = "Zawalaj"
        kb_4.lokalizacja_klienta = "Dworska 20/24, 80-511 Gdańsk"
        kb_4.nazwa_banku = "Bank Powszechny - Bocian"
        kb_4.koordynaty = [54.4069542, 18.6312159]
        KlientBanku.lista_klientow_banku.append(kb_4)

        kb_5 = KlientBanku(self.odswiez_widok)
        kb_5.imie_klienta = "Jola"
        kb_5.nazwisko_klienta = "Wola"
        kb_5.lokalizacja_klienta = "Klonowa 1, 80-264 Gdańsk"
        kb_5.nazwa_banku = "Bank Prywatny - lichwiarz"
        kb_5.koordynaty = [54.3805141, 18.6039619]
        KlientBanku.lista_klientow_banku.append(kb_5)


