import config

class SiatkaGracza:
    def __init__(self, poziom_trudnosci="łatwy"):
        cfg = config.POZIOM_TRUDNOSCI[poziom_trudnosci]
        self.szerokosc = cfg['szerokosc']
        self.wysokosc = cfg['wysokosc']
        self.liczba_min = cfg['miny']

        self.plansza = [[config.PUSTE for _ in range(0, self.szerokosc)] for _ in range(0, self.wysokosc)]

    def odkryj_pole(self, x, y, wartosc):
        self.plansza[y][x] = wartosc

    def przelacz_flage(self, x, y):
        if self.plansza[y][x] == config.ZAKRYTE:
            self.plansza[y][x] = config.FLAGA
        if self.plansza[y][x] == config.FLAGA:
            self.plansza[y][x] = config.ZAKRYTE

    def pobierz_stan_pola(self, x, y):
        return self.plansza[y][x]