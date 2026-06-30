import random
import config

class SiatkaGry:
    def __init__(self, poziom_trudnosci="łatwy"):
        cfg = config.POZIOM_TRUDNOSCI[poziom_trudnosci]
        self.szerokosc = cfg['szerokosc']
        self.wysokosc = cfg['wysokosc']
        self.liczba_min = cfg['miny']

        self.plansza = [[config.PUSTE for _ in range(self.szerokosc)] for _ in range(self.wysokosc)]
        self.czy_wygenerowana = False
        for i in self.plansza:
            print(i)

    def generuj_plansze(self, x_uzytkownika, y_uzytkownika):
        print("poczatek generowania planszy")

        wszystkie_pozycje = []
        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                if abs(x - x_uzytkownika) <= 1 and abs(y - y_uzytkownika) <= 1:
                    continue
                wszystkie_pozycje.append((x, y))
        print(wszystkie_pozycje)

        pozycje_min = random.sample(wszystkie_pozycje, self.liczba_min)
        print(pozycje_min)
        for x, y in pozycje_min:
            print(x, y)
            self.plansza[y][x] = config.MINA

        for y in range(self.wysokosc):
            for x in range(self.szerokosc):
                if self.plansza[y][x] == config.MINA:
                    continue
                self.plansza[y][x] = self._liczba_min_w_sadziectwie(x, y)

        self.czy_wygenerowana = True
        print("plansza wygenerowana")

    def _liczba_min_w_sadziectwie(self, x, y):
        licznik = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                xx, yy = x + j, y + i
                if 0 <= xx < self.szerokosc and 0 <= yy < self.wysokosc:
                    if self.plansza[yy][xx] == config.MINA:
                        licznik += 1
        return licznik

    def pobierz_wartosc_pola(self, x, y):
        return self.plansza[y][x]