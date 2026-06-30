import pygame
import sys
import config
class Menu:
    def __init__(self):
        pygame.init()
        self.okno = pygame.display.set_mode((400, 500))
        pygame.display.set_caption('Saper - Menu Startowe')
        self.czcionka = pygame.font.SysFont('Arial', 24)
        self.czcionka_mala = pygame.font.SysFont('Arial', 18)

        self.kolory = {
            'tlo': (200, 200, 200),
            'przycisk': (150, 150, 150),
            'przycisk_hover': (180, 180, 180),
            'tekst': (0, 0, 0),
            'input_aktywny': (255, 255, 255),
            'input_nieaktywny': (220, 220, 220),
            'blad': (255, 0, 0)
        }
        self.stan = "glowny"
        self.komunikat_bledu = ""
        szerokosc_przycisku, wysokosc_przycisku = 250, 50
        x_srodek = (400 - szerokosc_przycisku) // 2
        self.przycisk_glowne = [
            {"tekst": "Łatwy", "poziom": "latwy", "rect": pygame.Rect(x_srodek, 100, szerokosc_przycisku, wysokosc_przycisku)},
            {"tekst": "Średni", "poziom": "sredni", "rect": pygame.Rect(x_srodek, 170, szerokosc_przycisku, wysokosc_przycisku)},
            {"tekst": "Trudny", "poziom": "trudny", "rect": pygame.Rect(x_srodek, 240, szerokosc_przycisku, wysokosc_przycisku)},
            {"tekst": "Własny (Custom)", "poziom": "custom", "rect": pygame.Rect(x_srodek, 310, szerokosc_przycisku, wysokosc_przycisku)},
        ]
        self.pola_input = {
            "szerokosc": {"etykieta": "Szerokość:", "rect": pygame.Rect(200, 150, 100, 35), "tekst": "", "aktywny": False},
            "wysokosc": {"etykieta": "Wysokość: ", "rect": pygame.Rect(200, 210, 100, 35), "tekst": "", "aktywny": False},
            "miny": {"etykieta": "Ilość min:", "rect": pygame.Rect(200, 270, 100, 35), "tekst": "", "aktywny": False}
        }
        self.przycisk_graj = pygame.Rect(125, 350, 150, 50)
        self.przycisk_wstecz = pygame.Rect(10, 10, 80, 30)

    def uruchom(self):
        dziala = True
        wybrany_poziom = None
        while dziala:
            pozycja_myszy = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.stan == "glowny":
                        wybrany_poziom = self._obsluga_kliku_glowny(pozycja_myszy)
                        if wybrany_poziom == "custom":
                            self.stan = "custom"
                            wybrany_poziom = None
                        elif wybrany_poziom:
                            return wybrany_poziom
                    elif self.stan == "custom":
                        wybrany_poziom = self._obsluga_kliku_custom(pozycja_myszy)
                        if wybrany_poziom:
                            return wybrany_poziom
                if event.type == pygame.KEYDOWN and self.stan == "custom":
                    self._obsluga_klawiatury(event)
            self.okno.fill(self.kolory['tlo'])
            if self.stan == "glowny":
                self._rysuj_menu_glowny(pozycja_myszy)
            elif self.stan == "custom":
                self._rysuj_menu_custom(pozycja_myszy)
            pygame.display.flip()

    def _obsluga_kliku_glowny(self, pozycja_myszy):
        for p in self.przycisk_glowne:
            if p['rect'].collidepoint(pozycja_myszy):
                return p['poziom']
        return None

    def _obsluga_kliku_custom(self, pozycja_myszy):
        if self.przycisk_wstecz.collidepoint(pozycja_myszy):
            self.stan = "glowny"
            self.komunikat_bledu = ""
            return None
        for klucz, pole in self.pola_input.items():
            pole['aktywny'] = pole['rect'].collidepoint(pozycja_myszy)
        if self.przycisk_graj.collidepoint(pozycja_myszy):
            return self._waliduj_i_zapisz_custom()
        return None

    def _obsluga_klawiatury(self, event):
        for klucz, pole in self.pola_input.items():
            if pole['aktywny']:
                if event.key == pygame.K_BACKSPACE:
                    pole['tekst'] = pole['tekst'][:-1]
                elif event.unicode.isnumeric() and len(pole['tekst']) < 3:
                    pole['tekst'] += event.unicode

    def _waliduj_i_zapisz_custom(self):
        try:
            szerokosc = int(self.pola_input['szerokosc']['tekst'])
            wysokosc = int(self.pola_input['wysokosc']['tekst'])
            miny = int(self.pola_input['miny']['tekst'])

            if szerokosc < 5 or wysokosc < 5:
                self.komunikat_bledu = "Minimalna plansza to 5x5"
                return None
            if szerokosc > 40 or wysokosc > 40:
                self.komunikat_bledu = "Maksymalna plansza to 40x40"
                return None
            if miny < 1:
                self.komunikat_bledu = "Minimalna ilość min to 1"
            if miny >= (szerokosc + wysokosc) - 9:
                self.komunikat_bledu = "Za dużo min dla tej planszy"
                return None
            config.POZIOM_TRUDNOSCI['wlasny'] = {
                "szerokosc": szerokosc,
                "wysokosc": wysokosc,
                "miny": miny
            }
            return "wlasny"
        except ValueError:
            self.komunikat_bledu = "Wypełnij wszytskie pola"
            return None

    def _rysuj_menu_glowny(self, pozycja_myszy):
        tytul = self.czcionka.render("Wybierz poziom trudność", True, self.kolory['tekst'])
        self.okno.blit(tytul, (400 // 2 - tytul.get_width() // 2, 30))
        for p in self.przycisk_glowne:
            kolor = self.kolory['przycisk_hover'] if p['rect'].collidepoint(pozycja_myszy) else self.kolory['przycisk']
            pygame.draw.rect(self.okno, kolor, p['rect'])
            pygame.draw.rect(self.okno, (0, 0, 0), p['rect'], 2)
            tekst = self.czcionka_mala.render(p['tekst'], True, self.kolory['tekst'])
            tekst_rect = tekst.get_rect(center=p['rect'].center)
            self.okno.blit(tekst, tekst_rect)

    def _rysuj_menu_custom(self, pozycja_myszy):
        pygame.draw.rect(self.okno, self.kolory['przycisk'], self.przycisk_wstecz)
        pygame.draw.rect(self.okno, (0, 0, 0), self.przycisk_wstecz, 1)
        wstecz_tekst = self.czcionka_mala.render("Wstecz", True, self.kolory['tekst'])
        self.okno.blit(wstecz_tekst, self.przycisk_wstecz.move(10, 3))
        tytul = self.czcionka.render("Tryb Własny", True, self.kolory['tekst'])
        self.okno.blit(tytul, (400 // 2 - tytul.get_width() // 2, 70))
        for klucz, pole in self.pola_input.items():
            etykieta = self.czcionka_mala.render(pole["etykieta"], True, self.kolory['tekst'])
            self.okno.blit(etykieta, (80, pole["rect"].y + 5))
            kolor_pola = self.kolory['input_aktywny'] if pole["aktywny"] else self.kolory['input_nieaktywny']
            pygame.draw.rect(self.okno, kolor_pola, pole["rect"])
            pygame.draw.rect(self.okno, (0, 0, 0), pole["rect"], 2)
            wartosc = self.czcionka.render(pole["tekst"], True, self.kolory['tekst'])
            self.okno.blit(wartosc, (pole["rect"].x + 5, pole["rect"].y + 3))

        kolor_graj = self.kolory['przycisk_hover'] if self.przycisk_graj.collidepoint(pozycja_myszy) else self.kolory['przycisk']
        pygame.draw.rect(self.okno, kolor_graj, self.przycisk_graj)
        pygame.draw.rect(self.okno, (0, 0, 0), self.przycisk_graj, 2)
        tekst_graj = self.czcionka.render("GRAJ", True, self.kolory['tekst'])
        self.okno.blit(tekst_graj, tekst_graj.get_rect(center=self.przycisk_graj.center))

        if self.komunikat_bledu:
            blad = self.czcionka_mala.render(self.komunikat_bledu, True, self.kolory['blad'])
            self.okno.blit(blad, (400 // 2 - blad.get_width() // 2, 420))


