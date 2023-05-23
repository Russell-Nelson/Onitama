import pygame
import sys
from const import *
from game_state import Game_state
import os


class Display:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Onitama")
    
    def show_bg(self):
        for row in range(5):
            for col in range(5):
                # add check for temple
                if (row + col) % 2 == 0:
                    # light brown
                    color = (240, 217, 181)
                else:
                    # dark brown
                    color = (181, 136, 99)
                
                # pygame rectange has (start on the x axis, start on the y axis, width, height)
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(self.screen, color, rect)
            
    def show_pawns(self, state):
        board = state.board
        for row in range(5):
            for col in range(5):
                if (board[row][col].pawn != None):
                    pawn = board[row][col].pawn

                    # texture should be a path to a texture
                    texture = os.path.join(
                        f'assets/images/imgs-80px/black_pawn.png')
                    img = pygame.image.load(texture)

                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    self.screen.blit(img, img.get_rect(center=img_center))

    


# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         pygame.quit()
#         sys.exit()
    
# pygame.display.update()
