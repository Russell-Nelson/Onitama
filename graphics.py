import pygame
import os
from game_state import Game_state
import move
import onitama
import minimax

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SQUARE_POSITIONS = [
    [(234, 134), (301, 134), (368, 134), (435, 134), (502, 134)],
    [(234, 201), (301, 201), (368, 201), (435, 201), (502, 201)],
    [(234, 268), (301, 268), (368, 268), (435, 268), (502, 268)],
    [(234, 335), (301, 335), (368, 335), (435, 335), (502, 335)],
    [(234, 402), (301, 402), (368, 402), (435, 402), (502, 402)]
]

LINE_WIDTH = 3

BOARD_WIDTH = 500 * 2 // 3
BOARD_HEIGHT = 500 * 2 // 3
BOARD_TOP_LEFT = SQUARE_POSITIONS[0][0]
SQSIZE = 64
BOARD_BOTTOM_RIGHT = (SQUARE_POSITIONS[4][4][0] + SQSIZE, SQUARE_POSITIONS[4][4][1] + SQSIZE)
BACKGROUND_PATH = 'images\\board-background.png'

CARD_WIDTH = 150
CARD_HEIGHT = 90
BLUECARD0_POSITION = (239, 23)
BLUECARD1_POSITION = (409, 23)
MIDDLECARD0_POSITION = (63, 255)
MIDDLECARD1_POSITION = (587, 255)
REDCARD0_POSITION = (241, 487)
REDCARD1_POSITION = (409, 487)

def get_movement_index(pawn, card, dest, state):
    piece_row = pawn.coordinates[0]
    piece_col = pawn.coordinates[1]
    row_change = dest[0] - piece_row
    col_change = dest[1] - piece_col

    if (state.current_player.color == "blue"):
        row_change = -row_change
        col_change = -col_change   
    for movement in card.movement:
        if (movement[0] == row_change and movement[1] == col_change):
            return card.movement.index(movement)
    return None

class Graphics:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
        pygame.display.set_caption('Onitama')
        self.bg_img = pygame.image.load(BACKGROUND_PATH)
        self.bg_img = pygame.transform.scale(self.bg_img,(SCREEN_WIDTH,SCREEN_HEIGHT))
        self.move_sound = pygame.mixer.Sound('sounds\move.wav')
        self.capture_sound = pygame.mixer.Sound('sounds\capture.wav')
    
    def show_background(self):
        self.screen.blit(self.bg_img, (0,0))
    
    def show_pawns(self, state):
        screen = self.screen
        board = state.board

        for row in range(5):
            for col in range(5):
                if (board[row][col].pawn != None):
                    pawn = board[row][col].pawn
                    img = pygame.image.load(pawn.texture)
                    screen.blit(img, SQUARE_POSITIONS[row][col])
    
    def show_cards(self, state):
        blue_cards = state.blue_player.hand
        red_cards = state.red_player.hand
        card_rotation = state.card_rotation

        blue_card0_shadow = pygame.image.load('images\cards\card-shadow.png')
        self.screen.blit(blue_card0_shadow, BLUECARD0_POSITION)
        blue_card1_shadow = pygame.image.load('images\cards\card-shadow.png')
        self.screen.blit(blue_card1_shadow, BLUECARD1_POSITION)
        
        blue_card0 = pygame.image.load(blue_cards[0].texture)
        blue_card0 = pygame.transform.rotate(blue_card0, 180)
        self.screen.blit(blue_card0, BLUECARD0_POSITION)

        blue_card1 = pygame.image.load(blue_cards[1].texture)
        blue_card1 = pygame.transform.rotate(blue_card1, 180)
        self.screen.blit(blue_card1, BLUECARD1_POSITION)

        red_card0_shadow = pygame.image.load('images\cards\card-shadow.png')
        self.screen.blit(red_card0_shadow, REDCARD0_POSITION)
        red_card1_shadow = pygame.image.load('images\cards\card-shadow.png')
        self.screen.blit(red_card1_shadow, REDCARD1_POSITION)

        red_card0 = pygame.image.load(red_cards[0].texture)
        self.screen.blit(red_card0, REDCARD0_POSITION)

        red_card1 = pygame.image.load(red_cards[1].texture)
        self.screen.blit(red_card1, REDCARD1_POSITION)

        if (card_rotation[0] != None):
            middle_card_shadow = pygame.image.load('images\cards\card-shadow.png')
            self.screen.blit(middle_card_shadow, MIDDLECARD0_POSITION)
            middle_card0 = pygame.image.load(card_rotation[0].texture)
            middle_card0 = pygame.transform.rotate(middle_card0, 180)
            self.screen.blit(middle_card0, MIDDLECARD0_POSITION)
        else:
            middle_card_shadow = pygame.image.load('images\cards\card-shadow.png')
            self.screen.blit(middle_card_shadow, MIDDLECARD1_POSITION)
            middle_card1 = pygame.image.load(card_rotation[1].texture)
            self.screen.blit(middle_card1, MIDDLECARD1_POSITION)


    def interpret_mouse_click(self, pos, state, clicked_pawn, clicked_card, clicked_dest):
        x_pos = pos[0]
        y_pos = pos[1]
        player = state.current_player
        color = player.color
        
        # first check if the click was on the board
        if ((BOARD_TOP_LEFT[0] <= x_pos <= BOARD_BOTTOM_RIGHT[0]) and (BOARD_TOP_LEFT[1] <= y_pos <= BOARD_BOTTOM_RIGHT[1])):

            # calculate row and col with adjustments for line spacing between squares
            row = (y_pos - BOARD_TOP_LEFT[1]) // (SQSIZE + LINE_WIDTH)
            col = (x_pos - BOARD_TOP_LEFT[0]) // (SQSIZE + LINE_WIDTH)
            
            # check if there is a piece there that belongs to the current player
            if (state.board[row][col].pawn != None and state.board[row][col].pawn.color == color):
                clicked_pawn = state.board[row][col].pawn
                return (clicked_pawn, clicked_card, clicked_dest)
            # otherwise if we have already clicked a pawn and card, then this might be a dest if it is empty or has an opponent's pawn
            elif (clicked_pawn != None and clicked_card != None and (state.board[row][col].pawn == None or state.board[row][col].pawn.color != color)):
                clicked_dest = (row, col)
                return (clicked_pawn, clicked_card, clicked_dest)
            # else it was a click on the board that does not update anything
            else:
                return (clicked_pawn, clicked_card, clicked_dest)
        
        # if the click was not on the board then we just need to check cards        
        else:
            # set up our reference points based on color
            if (color == "blue"):
                card0_pos = BLUECARD0_POSITION
                card1_pos = BLUECARD1_POSITION
            else:
                card0_pos = REDCARD0_POSITION
                card1_pos = REDCARD1_POSITION
            
            # now compare the click to the player's card dimensions and location
            if ((card0_pos[0] <= x_pos <= card0_pos[0] + CARD_WIDTH) and (card0_pos[1] <= y_pos <= card0_pos[1] + CARD_HEIGHT)):
                clicked_card = 0
                return (clicked_pawn, clicked_card, clicked_dest)

            elif ((card1_pos[0] <= x_pos <= card1_pos[0] + CARD_WIDTH) and (card1_pos[1] <= y_pos <= card1_pos[1] + CARD_HEIGHT)):
                clicked_card = 1
                return (clicked_pawn, clicked_card, clicked_dest)

            # if nothing else then just return any previous clicked objects
            return (clicked_pawn, clicked_card, clicked_dest)
    
    def show_selection(self, clicked_pawn, clicked_card, state):
        player = state.current_player
        if (clicked_pawn != None):
            pawn_row = clicked_pawn.coordinates[0]
            pawn_col = clicked_pawn.coordinates[1]
            pawn_highlight = pygame.image.load('images\selections\\red-pawn-selected.png')
            self.screen.blit(pawn_highlight, SQUARE_POSITIONS[pawn_row][pawn_col])
        
        if (clicked_card != None):
            if (clicked_card == 0):
                card_highlight = pygame.image.load('images\selections\\red-card-selected.png')
                self.screen.blit(card_highlight, REDCARD0_POSITION)
            else:
                card_highlight = pygame.image.load('images\selections\\red-card-selected.png')
                self.screen.blit(card_highlight, REDCARD1_POSITION)
        
        if (clicked_card != None and clicked_pawn != None):
            pawn_row = clicked_pawn.coordinates[0]
            pawn_col = clicked_pawn.coordinates[1]

            for movement_index in range(len(player.hand[clicked_card].movement)):
                possible_move = move.Move(pawn_row, pawn_col, clicked_card, movement_index)
                if possible_move.is_valid(state, player):
                    target_row = pawn_row + player.hand[clicked_card].movement[movement_index][0]
                    target_col = pawn_col + player.hand[clicked_card].movement[movement_index][1]
                    target_highlight = pygame.image.load('images\selections\\red-target-square.png')
                    self.screen.blit(target_highlight, SQUARE_POSITIONS[target_row][target_col])

