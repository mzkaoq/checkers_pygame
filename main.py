import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, HEIGHT_BELT, FONT, BLACK, GREY
from checkers.game import Game
from checkers.Exceptions import OutsideBoardExceptions

'''
stworzyłem grę checkers - czyli odmiana brytyjska warcabów - bicie zwykłym pionkiem jak i poruszanie się
tylko do przodu, król/damka może bić jak i chodzić do tyłu

Plansza jest 8x8, 12 pionów dla każdego z graczy. 
Pozycja początkowa jest taka sama jak w warcabach międzynarodowych 8x8. 
Piony przesuwają się do przodu po skosie o jedno pole, 
jeżeli nie jest ono zajęte. Jeżeli to pole możliwego ruchu jest zajęte przez pion przeciwnika, 
a bezpośrednio za tym pionem, na tej samej przekątnej, jest puste pole, 
można wtedy zbić ten pion przeciwnika, przez postawienie swojego piona na tym pustym polu. 

Gdy jest więcej niż jedna możliwa droga bicia, możemy ją dowolnie wybrać. 
Pion dochodzący do ostatniego rzędu staje się królem. Promocja piona do króla powoduje zakończenie posunięcia. 
Król ma analogiczną możliwość wykonywania posunięć jak pion, z tym, że może poruszać się i bić także do tyłu. 
Wygrana następuje po zbiciu wszystkich bierek przeciwnika 
'''

# ustawienie liczby FPS, określenie wielkości okna i ustawienie tytułu
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT_BELT))
pygame.display.set_caption("checkers")


def get_row_col_from_mouse(pos):
    '''
    pobieranie pozycji myszy zwracanie pozycji w przeliczeniu na rzędy i kolumny
    '''
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    '''
    główna funkcja programu określa kiedy wyświetla się okno z grą i przekazuje liczbę FPS w grze,w niej znajduje się główną pętla programu
    która odpowiada za rysowanie okna pygame, pobieranie pozycji myszy i przekazywanie jej do kolejnych funkcji
    gdy przycisk zostanie naciśniety

    wywoływanie funkcji update'ujacej, zamykanie okna z grą
    gdy zamkniemy okno z grą pętla zostaje przerwana co umożliwia nam zamknięcie okna

    jest też łapany wyjątek dla kliknięć poza obręb planszy do gry ale wciąż w oknie gry
    '''
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            # jeżeli nastąpi naciśniecię czerwonego X pętla jest stopowana
            if event.type == pygame.QUIT:
                run = False
            # jeśli wystąpi naciśnięcie myszy wywoływana jest metoda select
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print(row, col)
                try:
                    game.select(row, col)
                except OutsideBoardExceptions:
                    game.outside_board_exce = True
                    print("outside board exce")
        pygame.display.update()
        # metoda zarządzająca grą
        game.update()

    # po wyjściu z pętli while następuje wyjście z aplikacji okna pygame
    pygame.quit()


# wywowalnie main'a
main()
