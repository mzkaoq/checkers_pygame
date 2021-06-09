import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, HEIGHT_BELT,FONT
from checkers.game import Game

FPS = 60
WIN = pygame.display.set_mode((WIDTH,HEIGHT_BELT))
pygame.display.set_caption("checkers")

def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row,col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            if game.winner()==WHITE:
                print("white has won")
                break
            else:
                print("red has won")
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print(row,col)
                game.select(row,col)

        game.update()

    pygame.quit()
main()