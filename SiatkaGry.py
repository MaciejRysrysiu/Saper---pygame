import random
import config

class SiatkaGry:
    def __init__(self, poziom_trudnosci="łatwy"):
        cfg = config.POZIOM_TRUDNOSCI[poziom_trudnosci]
        self.szerokosc = cfg['szerokosc']
        self.wysokosc = cfg['wysokosc']
        self.liczba_min = cfg['miny']

        self.plansza = [[config.PUSTE for _ in range(0, self.szerokosc)] for _ in range(0, self.wysokosc)]
        self.czy_wygenerowana = False

    def generuj_plansze(self, x_uzytkownika, y_uzytkownika):
        wszystkie_pozycje = []
        for y in range(0, self.wysokosc):
            for x in range(0, self.liczba_min):
                if abs(x - x_uzytkownika) <= 1 and abs(y - y_uzytkownika) <= 1:
                    continue
                wszystkie_pozycje.append((x, y))

        pozycje_min = random.sample(wszystkie_pozycje, self.liczba_min)

        for x, y in pozycje_min:
            self.plansza[y][x] = config.MINA

        for y in range(0, self.wysokosc):
            for x in range(0, self.liczba_min):
                if self.plansza[y][x] == config.MINA:
                    continue
                self.plansza[y][x] = self.liczba_min_w_sadziectwie(x, y)

        self.wygenerowana = True

    def liczba_min_w_sadziectwie(self, x, y):
        licznik = 0
        tab = [-1, 0, 1]
        for i in tab:
            for j in tab:
                xx, yy = x + i, y + j
                if 0 <= xx < self.szerokosc and 0 <= yy < self.wysokosc:
                    if self.plansza[yy][xx] == config.MINA:
                        licznik += 1
        return licznik

    def pobierz_wartosc_pola(self, x, y):
        return self.plansza[y][x]