import pygame
from fontTools.config import Config
import config

class Interfejs:
    def __init__(self, szerokosc_siatki, wysokosc_siatki):
        pygame.init()

        szerokosc_okna = szerokosc_siatki * config.ROZMIAR_KAFELKA
        wysokosc_okna = wysokosc_siatki * config.ROZMIAR_KAFELKA
        self.okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
        pygame.display.update("Saper")
        self.czcionka = pygame.font.SysFont('arial', int(config.ROZMIAR_KAFELKA * 0.6))

        self.kolory = config.KOLORY

    def rysuj_plansze(self, siatka_gracza):
        self.okno.fill(self.kolory['tło'])
        for y in range(0, siatka_gracza.wysokosc):
            for x in range(0, siatka_gracza.szerokosc):
                wartosc = siatka_gracza.pobierz_stan_pola(x, y)
                rect = pygame.Rect(x * config.ROZMIAR_KAFELKA, y * config.ROZMIAR_KAFELKA, config.ROZMIAR_KAFELKA, config.ROZMIAR_KAFELKA)
                self.rysuj_kafelek(rect, wartosc)

        pygame.display.flip()

    def rysuj_kafelek(self, rect, wartosc):
        if wartosc in [config.ZAKRYTE, config.FLAGA]:
            pygame.draw.rect(self.okno, self.kolory['zakryte'], rect)
            pygame.draw.rect(self.okno, self.kolory['krawedz'], rect, 2)
        else:
            pygame.draw.rect(self.okno, self.kolory['odkryte'], rect)
            pygame.draw.rect(self.okno, self.kolory['krawedz'], rect, 1)

        srodek_x = rect.x + config.ROZMIAR_KAFELKA // 2
        srodek_y = rect.y + config.ROZMIAR_KAFELKA // 2

        if wartosc == config.FLAGA:
            pygame.draw.polygon(self.okno, self.kolory['flag'], [
                (rect.x  + 10, rect.y + 25),
                (rect.x + 10, rect.y + 5),
                (rect.x + 25, rect.y + 15)
            ])
        elif wartosc == config.MINA:
            pygame.draw.circle(self.okno, self.kolory['mina'], (srodek_x, srodek_y), config.ROZMIAR_KAFELKA // 3)
        elif wartosc > 0:
            kolor_tekstu = self.kolory['cyfra'].get(wartosc, (0, 0, 0))
            tekst = self.czcionka.render(str(wartosc), True, kolor_tekstu)
            prostokat_tekstu = tekst.get_rect(center=(srodek_x, srodek_y))
            self.okno.blit(tekst, prostokat_tekstu)