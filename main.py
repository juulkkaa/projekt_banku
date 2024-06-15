# main jest główną funkcją programów w wielu językach także w python. 
# Jego zadaniem jest uruchomienie aplikacji. 
# Według dobrych praktyk dana funkcja powinna być jak najkrótsza, a wszystkie funkcje w innych częściach kodu.

from Logowanie import * # Zaimportowanie klasy odpowiedzialnej za stronę logowania.


# Uruchomienie aplikacji
def main():
    Logowanie()


# Dana część kodu jest uruchamiana zaraz po uruchomieniu pliku. 
if __name__ == '__main__':
    main()