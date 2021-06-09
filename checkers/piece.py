import pygame
from checkers.constants import GREY, WHITE, SQUARE_SIZE, CROWN


class Pattern:

    #rozmiary naszej bierki
    PADDING = 15
    BORDER = 2

    def __init__(self, row, col, color):
        '''
        inicjalizacja naszej bierki
        przechowuje informacje w jakiej kolumnie rzędzie się znajduje
        jakiego jest koloru
        wspólrzędna x,y na ekranie
        metoda obliczająca x,y
        '''
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        '''
        metoda oblicza x,y - wspólrzedne na podstawie rzędu i kolumny oraz informacji o wielkości jednego pola
        '''
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


    def draw(self, win):
        '''
        rysowanie kokretnej bierki w konkretnych współrzędnych x,y na ekranie, istnieje opcja nałożenia na rysunek
        korony jeżeli bierka jest królem
        '''
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.BORDER)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def __repr__(self):
        '''
        zwraca kolor danej bierki dla której jest to wywołane - kolor przynależność do CZERWONI/BIALI
        '''
        return str(self.color)

    def move(self, row, col):
        '''
        przypisanie nowych kolumn i rzędów, obliczenie x,y korzystają z calc_pos()
        '''
        self.row = row
        self.col = col
        self.calc_pos()


class Piece(Pattern):
    '''
    właściwa klasa która odpowiada za podstawowe bierki - posiada konstruktor z klasy nadrzędnej rozszerzony o nowe pole
    a mianowicie definicja że bierka nie jest królem
    '''
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = False


class King(Piece):
    '''
    dziedziczy po domyślnej bierce - jeden z parametrów konstruktora stanowi że bierka jest królem
    '''
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.king = True
