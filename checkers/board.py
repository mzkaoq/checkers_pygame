import pygame
from .constants import BLACK, WHITE, ROWS, COLS, RED, SQUARE_SIZE, GREY, GOLD, FONT
import checkers.game
from .piece import Piece, King


class Board:
    def __init__(self, win):
        '''
        inicjalizacja klasy
        ustawienie początkowych parametrow jak pusta tablica która jest naszą planszą, licza królów, liczba pozostalych pionków
        przekazywanie parametru win - nasze okno z main'a
        tworzenie konkretnej tablicy z rozstawieniem początkowym
        '''
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.win = win
        self.create_board2()
        # self.create_board_test_g_f()

    def draw_squares(self, win):
        '''
        rysowanie szachownicy z czerwonych i czarnych pol
        '''
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_button_and_back(self, win):
        '''
        rysowanie przycisku RESTART na dole ekranu
        '''
        pygame.draw.rect(win, GOLD, (0, 8 * SQUARE_SIZE, 8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
        pygame.draw.rect(win, GREY, (0 * SQUARE_SIZE + 5, 8 * SQUARE_SIZE + 5, 2 * SQUARE_SIZE - 10, SQUARE_SIZE - 10))

    def show_text(self, content, x, y):
        '''
        funkcja służąca do rysowania/pisania zadanego tekstu w konkretnych współrzędnych na ekranie
        '''
        text = FONT.render(content, True, (0, 0, 0))
        self.win.blit(text, (y * SQUARE_SIZE + SQUARE_SIZE // 4 + 5, x * SQUARE_SIZE + SQUARE_SIZE // 4 + 5))

    def create_board2(self):
        '''
        ustawienie początkowe planszy poprzez inicjalizacje tablicy do gry standardowej
        '''
        for i in range(ROWS):
            if i < 3:
                self.board.append([Piece(i, x, WHITE) if x % 2 == (i + 1) % 2 else 0 for x in range(COLS)])
            elif i > 4:
                self.board.append([Piece(i, x, RED) if x % 2 == (i + 1) % 2 else 0 for x in range(COLS)])
            else:
                self.board.append([0 for x in range(COLS)])

    def draw(self, win):
        '''
        wywołanie pętli rysującej pola jak i konkretne obiekty (bierki) oraz przycisk z napisem
        '''
        self.draw_squares(win)
        self.draw_button_and_back(win)
        self.show_text("RESTART", 8, 0)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        '''
        funkcja obsługująca ruchy, przekazujemy do niej konkretny obiekt klasy i zamieniamy go z tym co znajduje się
        na wskazanych współrzędnych w metodzie, w naszej grze jest to zawsze zamiana miejscami jakiegoś obiektu klasy z 0
        obsługa promocji na króla
        '''
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            self.board[piece.row][piece.col] = King(piece.row, piece.col, piece.color)
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        '''
        zwraca to co kryje się pod danymi współrzędnymi w naszej tablicy reprezentującej planszę pod danymi współrzędnymi
        '''
        return self.board[row][col]

    def get_valid_moves(self, piece):
        '''
        metoda inicjalizująca przeszukiwanie dozwolonych ruchów dla przekazanej do niej bierki, tylko w górę lub tylko w dól
        w zalezności od koloru, dla króla w obie strony, określamy zasięg przeszukiwania w odległości od danej bierki
        (dla jakich rzędów i kolumn szukać),
        jak i kolor bierki dla której szukamy ruchów

        zwracamy słownik z listą współrzędnych oraz odpowiadającym im zbitym bierkom o ile występują
        '''
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -3), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -3), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        '''
        przeszukiwanie na lewo od bierki
        :param step definiuje czy w górę czy w dół patrząc po rzędach
        :param start,stop definiuje jaki przedział rzędów przeszukujemy
        :skipped pusta lista którą będziemy wypełniać
        :left kolumna na lewo od tej od której to wywołujemy

        zwracamy słownik gdzie pierszym argumentem jest spółrzędne na które mozemy się ruszyć
        a drugim jest lista elementów które możemy zbić ew. jest pusta tzn nic nie bijemy
        przy wielokrotnych biciach idziemy od "konca" tzn ważne ruchy również są dodawne do listy w słowniku
        '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            # jeśli wyjście poza planszę break
            if left < 0:
                break

            # obecna pozycja na planszy dla której sprawdzamy ruchy jeśli jest równy 0 = puste pole
            # spradzamy czy mogliśmy coś zbić
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        '''
        analogicznie jak _traverse_left powyżej
        '''
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves

    def remove(self, pieces):
        '''
        na podstawie otrzymanej listy usuwa kolejne elementy z planszy - pola odpowiadających współrzędnych
        na szachownicy zmienia na 0 czyli usuwa poprzednią instancję klasy która tam była
        odejmuje od licznika -1 czyli zmniejsza ogólną liczbe bierek danego koloru - informacja potrzebna żeby wiedzieć kto
        wygrał gdy dana wartość osiągnie 0

        '''
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        '''
        na podsatwie liczników - atrybutów klasy przechowujących informację o pozostałych bierkach danego koloru wyłaniamy zwycięzcę
        lub typ pusty NONE gdyż metoda ta wywoływana jest w każdym obrocie głównej pętli
        :return:
        '''
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    # tworzenie ustawień początkowych tablicy dla poszczególnych testów zwierających ilość elementów
    # jak i odpowiednio rozmieszczone odpowiednie klasy

    def create_board_test_d(self):
        self.red_left = 1
        self.white_left = 3
        self.board = [[0 for x in range(COLS)] for y in range(ROWS)]
        self.board[2][3] = Piece(2, 3, WHITE)
        self.board[4][5] = Piece(4, 5, WHITE)
        self.board[5][6] = Piece(5, 6, RED)
        self.board[6][1] = Piece(6, 1, WHITE)

    def create_board_test_e(self):
        self.red_left = 1
        self.white_left = 1
        self.board = [[0 for x in range(COLS)] for y in range(ROWS)]
        self.board[1][2] = Piece(1, 2, RED)
        self.board[6][1] = Piece(6, 1, WHITE)

    def create_board_test_f(self):
        self.red_left = 1
        self.white_left = 2
        self.board = [[0 for x in range(COLS)] for y in range(ROWS)]
        self.board[0][1] = Piece(0, 1, WHITE)
        self.board[5][0] = King(5, 0, RED)
        self.board[6][1] = Piece(6, 1, WHITE)

    def create_board_test_g_f(self):
        self.red_left = 1
        self.white_left = 1
        self.board = [[0 for x in range(COLS)] for y in range(ROWS)]
        self.board[4][1] = Piece(4, 1, WHITE)
        self.board[5][0] = Piece(5, 0, RED)
