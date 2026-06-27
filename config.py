MINA = -1
PUSTE = 0
ZAKRYTE = -2
FLAGA = -3

POZIOM_TRUDNOSCI = {
    "łatwy":{
        "szerokosc": 9,
        "wysokosc": 9,
        "miny": 10
    },
    "sredni":{
        "szerokosc": 16,
        "wysokosc": 16,
        "miny": 40
    },
    "trudny":{
        "szerokosc": 30,
        "wysokosc": 16,
        "miny": 99
    }
}

KOLORY = {
    'tlo': (150, 150, 150),
    'zakryte': (192, 192, 192),
    'odkryte': (220, 220, 220),
    'krawedz': (128, 128, 128),
    'flaga': (255, 0, 0),
    'mina': (0, 0, 0),
    'cyfry': {
        1: (0, 0, 255),       # Niebieski
        2: (0, 128, 0),       # Zielony
        3: (255, 0, 0),       # Czerwony
        4: (0, 0, 128),       # Granatowy
        5: (128, 0, 0),       # Bordowy
        6: (0, 128, 128),     # Cyjan
        7: (0, 0, 0),         # Czarny
        8: (128, 128, 128)    # Szary
    }
}
ROZMIAR_KAFELKA = 32