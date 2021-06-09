import pygame
from .Exceptions import BadMoveExceptions, OutsideBoardExceptions
from .constants import RED, WHITE, SQUARE_SIZE, BLUE, FONT2,FONT,GREY,BLACK
from checkers.board import Board


class Game:
    def __init__(self, win):
        '''
        de facto wywolanie _init() przypisanie zmiennej win która jest naszym oknem
        '''
        self.win = win
        self._init()

    def update(self):
        '''
        funkcja update uruchamiana w każdym obiegu głównej funkcji main,
        rysuje ustawienie szachownicy jak i samą szachownicę
        dozwolone ruchy o ile istnieją
        po części obłsuguje wyjątki poprzez printowanie tekstów "wywoływanych" przez wyjątki  za pomocą zmiany stanów zmiennych
        kontrolowanie czy któryś z graczy nie wygrał meczu poprzez sprawdzanie zmienne winner, jesli tak obsługuje
        printa z informacja kto wygrał
        '''
        self.board.draw(self.win)
        self.printing_moves()
        self.draw_valid_moves(self.valid_moves)
        if self.bad_move_exce:
            self.bad_move_exe()
            pygame.time.delay(1000)
        self.bad_move_exce = False
        if self.outside_board_exce:
            self.outside_board_exe()
            pygame.time.delay(1000)
        self.outside_board_exce = False
        if self.winner() != None:
            if self.winner() == WHITE:
                pygame.draw.rect(self.win, GREY,
                                 (1 * SQUARE_SIZE + SQUARE_SIZE // 2, 4 * SQUARE_SIZE, 5 * SQUARE_SIZE, SQUARE_SIZE + 5))
                self.show_text("WHITE HAS WON", 4, 1.5,WHITE)
            else:
                pygame.draw.rect(self.win, GREY,
                                 (1 * SQUARE_SIZE + SQUARE_SIZE//2, 4* SQUARE_SIZE, 5 * SQUARE_SIZE , SQUARE_SIZE +5))
                self.show_text("RED HAS WON", 4, 2,WHITE)
        pygame.display.update()

    def show_text(self, content, x, y,rgb):
        '''
        printowanie tekstu o zadanym kolorze rgb na ekranie w konkretnym miejscu
        '''
        text = FONT2.render(content, True, rgb)
        self.win.blit(text, (y * SQUARE_SIZE + SQUARE_SIZE // 4 + 5, x * SQUARE_SIZE + SQUARE_SIZE // 4 + 5))

    def _init(self):
        '''
        de facto funkcja inicjalizująca wywoływana w __init__(), było to potrzebne aby łatwo robić resety
        mamy takie parametry jak selected - zaznaczony item (typu zwykła bierka/król)
        stworzenie obiektu Board (nasza plansza)
        aktualna tura
        dostępne ruchy do funkcji valid_moves
        pola dla wyjątków do obsługi nieco zawiłej procedury printowania wyjątków na ekranie gry pygame
        '''
        self.selected = None
        self.board = Board(self.win)
        self.turn = RED
        self.valid_moves = {}
        self.bad_move_exce = False
        self.outside_board_exce = False

    def reset(self):
        '''
        resetowanie gry poprzez ponowne wywołanie funkcji _init()
        :return:
        '''
        self._init()

    def select(self, row, col):
        '''
        wybranie konkretnego itemu z naszej tablicy (szachownica ma dostępne pola 0 - puste, Piece - obiekt podsatwowej bierki, King - bierka król)
        wybieranie przebiega na podsatwie zmiennych row,col które symbolizują pola 8x8 planszy
        obsługa dwóch wyjątków - łapanie wyjątku odnośnie "bad move" kliknięcie podczas tury ruchu pole które nie jest dozwolonym ruchem
        oraz podnoszenie wyjątku o kliknięciu w dolny pasek który nie jest responsywny a jest jedynie tłem
        w dodatku metoda obsługuje restart gry gdy przekazane współrzędne odpowiadają naszemu przyciskowi

        '''
        if row != 8:
            if self.selected:
                try:
                    result = self._move(row, col)
                    if not result:
                        self.selected = None
                        self.select(row, col)
                except BadMoveExceptions:
                    self.bad_move_exce = True
                    print("bad move")
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
            elif piece != 0 and piece.color != self.turn:
                print("zly kolor")
            return False
        elif col == 0 or col == 1:
            self.restart_game()
        else:
            raise OutsideBoardExceptions()

    def bad_move_exe(self):
        '''
        obsługa printu dla niedozwolonego ruchu
        '''
        pygame.draw.rect(self.win, GREY,
                         (1 * SQUARE_SIZE + SQUARE_SIZE // 2, 4 * SQUARE_SIZE, 5 * SQUARE_SIZE,
                          SQUARE_SIZE + 5))
        self.show_text("BAD MOVE", 4, 1.5, BLACK)

    def outside_board_exe(self):
        '''
        obsługa printu dla kliknięcie poza obszar planszy który jednak dalej jest w oknie gry
        '''
        pygame.draw.rect(self.win, GREY,
                         (1 * SQUARE_SIZE + SQUARE_SIZE // 2, 4 * SQUARE_SIZE, 5 * SQUARE_SIZE,
                          SQUARE_SIZE + 5))
        self.show_text("Outside board", 4, 1.5, BLACK)

    def restart_game(self):
        '''
        metoda restartująca poprzez ponowne wywołanie inita który inicjalizuje wartości
        '''
        print("restart")
        self._init()

    def _move(self, row, col):
        '''
        metoda sprawdzająca czy
        '''
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            if piece == 0:
                raise BadMoveExceptions()
        return True

    def change_turn(self):
        '''
        metoda która zmienia turę bazując na obecnej turze
        :return:
        '''
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        elif self.turn == WHITE:
            self.turn = RED

    def draw_valid_moves(self, moves):
        '''
        na podstawie elementów w valid_moves = możliwe ruchy rysujemy niebieskie kropki w tych punktach
        '''
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 12)

    def winner(self):
        '''
        metoda zwracająca zwycięzce na podstawie zmiennych zawartych w klasie
        '''
        return self.board.winner()

    def printing_moves(self):
        '''
        obsługa printowania tury gracza na dole ekranu z grą
        '''
        if self.turn == RED:
            self.show_text("RED's MOVE", 7.8, 2, BLACK)
        else:
            self.show_text("WHITE's MOVE", 7.8, 2, BLACK)
