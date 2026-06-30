import config

class SiatkaGracza:
    def __init__(self, poziom_trudnosci="latwy"):
        cfg = config.POZIOM_TRUDNOSCI[poziom_trudnosci]
        self.szerokosc = cfg['szerokosc']
        self.wysokosc = cfg['wysokosc']
        self.liczba_min = cfg['miny']

        self.plansza = [[config.ZAKRYTE for _ in range(self.szerokosc)] for _ in range(self.wysokosc)]

    def odkryj_pole(self, x, y, wartosc):
        self.plansza[y][x] = wartosc

    def przelacz_flage(self, x, y):
        print(x, y)
        if self.plansza[y][x] == config.ZAKRYTE:
            self.plansza[y][x] = config.FLAGA
            print("udało sie ustawic flage")
        elif self.plansza[y][x] == config.FLAGA:
            self.plansza[y][x] = config.ZAKRYTE
        for i in self.plansza:
            print(i)

    def pobierz_stan_pola(self, x, y):
        return self.plansza[y][x]