import pygame
import sys
import config
import SiatkaGry
import SiatkaGracza
import Interfejs
import Menu

class Gra:
    def __init__(self, poziom_trudnosci):
        self.poziom = poziom_trudnosci
        self.siatka_gry = SiatkaGry.SiatkaGry(self.poziom)
        self.siatka_gracza = SiatkaGracza.SiatkaGracza(self.poziom)
        self.interfejs = Interfejs.Interfejs(self.siatka_gracza.szerokosc, self.siatka_gry.wysokosc)

        self.dziala = True
        self.koniec_gry = False
        self.wygrana = False

    def uruchom(self):
        pygame.display.flip()
        pygame.time.delay(200)
        pygame.event.clear()
        while self.dziala:
            self._obsluga_zdarzen()
            self.interfejs.rysuj_plansze(self.siatka_gracza)

            if self.koniec_gry:
                self._ekran_koncowy("Przegrana")
            elif self.wygrana:
                self._ekran_koncowy("Zwyciestwo")

    def _obsluga_zdarzen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dziala = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.koniec_gry and not self.wygrana:
                print(f"myszka kliknietana: {event.pos[0]}, {event.pos[1]}")
                x, y = event.pos
                grid_x = x // config.ROZMIAR_KAFELKA
                grid_y = y // config.ROZMIAR_KAFELKA

                if grid_x >= self.siatka_gry.szerokosc or grid_y >= self.siatka_gry.wysokosc:
                    continue
                if event.button == 1:
                    self._obsluga_lewego_przycisku(grid_x, grid_y)
                elif event.button == 3:
                    self._obsluga_prawego_przycisku(grid_x, grid_y)

    def _obsluga_lewego_przycisku(self, x, y):
        stan_pola = self.siatka_gracza.pobierz_stan_pola(x, y)
        print(f"test, {stan_pola}")
        if stan_pola != config.ZAKRYTE:
            print("debug1")
            return
        if not self.siatka_gry.czy_wygenerowana:
            print("debug2")
            self.siatka_gry.generuj_plansze(x, y)
        wartosc = self.siatka_gry.pobierz_wartosc_pola(x, y)
        print(f"kliknieto x:{x}, y:{y}")
        print(f"Pobrano wartosc: {wartosc}")
        print(f"Systemowa wartosc miny: {config.MINA}")
        if wartosc == config.MINA:
            self.siatka_gracza.odkryj_pole(x, y, config.MINA)
            self.koniec_gry = True
            return
        if wartosc == config.PUSTE:
            self._odkryj_wiele_pol(x, y)
        else:
            self.siatka_gracza.odkryj_pole(x, y, wartosc)

        self._sprawdz_wygrana()

    def _obsluga_prawego_przycisku(self, x, y):
        self.siatka_gracza.przelacz_flage(x, y)

    def _odkryj_wiele_pol(self, start_x, start_y):
        kolejka = [(start_x, start_y)]
        odwiedzone = set()
        while kolejka:
            x, y = kolejka.pop(0)
            if (x, y) in odwiedzone:
                continue
            odwiedzone.add((x, y))
            wartosc = self.siatka_gry.pobierz_wartosc_pola(x, y)
            self.siatka_gracza.odkryj_pole(x, y, wartosc)
            if wartosc == config.PUSTE:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.siatka_gry.szerokosc and 0 <= ny < self.siatka_gry.wysokosc:
                            if self.siatka_gracza.pobierz_stan_pola(nx, ny) == config.ZAKRYTE:
                                kolejka.append((nx, ny))

    def _sprawdz_wygrana(self):
        nieodkryte = 0
        for y in range(self.siatka_gry.wysokosc):
            for x in range(self.siatka_gry.wysokosc):
                stan = self.siatka_gracza.pobierz_stan_pola(x, y)
                if stan in [config.ZAKRYTE, config.FLAGA]:
                    nieodkryte += 1
        if nieodkryte == self.siatka_gry.liczba_min:
            self.wygrana = True

    def _ekran_koncowy(self, tekst):
        print(tekst)
        pygame.display.flip()
        pygame.time.delay(500)
        pygame.event.clear()
        czekaj = True
        while czekaj:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                    czekaj = False
                    self.dziala = False
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    menu = Menu.Menu()
    wybrany_poziom = menu.uruchom()
    if wybrany_poziom:
        gra = Gra(wybrany_poziom)
        gra.uruchom()