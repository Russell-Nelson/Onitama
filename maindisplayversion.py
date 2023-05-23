from game_state import Game_state
from move import Move
import re
import onitama
import minimax
import copy
from display import Display
import pygame
import sys
from dragger import Dragger
from const import *

# returns a move object if the input is valid. Otherwise returns None
def format_input(user_input, state):
    # use regex first for a basic syntax check
    pattern = re.compile("\([0-4],[0-4]\)[LR]\([0-4],[0-4]\)")
    if not pattern.fullmatch(user_input):
        return None
    
    piece_row = int(user_input[1])
    piece_col = int(user_input[3])
    row_change = int(user_input[7]) - piece_row
    col_change = int(user_input[9]) - piece_col
    if (user_input[5] == "R"):
        card_index = 1
    else:
        card_index = 0

    # now check if the indicated move is even possible with the selected card
    if (state.current_player.color == "blue"):
        row_change = -row_change
        col_change = -col_change
    movement_index = -1    
    card = state.current_player.hand[card_index]
    for movement in card.movement:
        if (movement[0] == row_change and movement[1] == col_change):
            movement_index = card.movement.index(movement)
            break
    if (movement_index == -1):
        return None

    # if we have gotten this far then it was valid input
    return Move(piece_row, piece_col, card_index, movement_index)

onitama_game = Game_state()

game = onitama.Onitama()

while onitama_game.game_is_over() not in ["red wins", "blue wins"]:
    onitama_game.print_game_state()

    display = Display()
    display.show_bg()
    display.show_pawns(onitama_game)
    for event in pygame.event.get():

        # click
        if (event.type == pygame.MOUSEBUTTONDOWN):
            dragger.update_mouse(event.pos)

            clicked_row = dragger.mouseY // SQSIZE
            clicked_col = dragger.mouseX // SQSIZE

            # check if there is a piece in that spot
            if (onitama_game.board[clicked_row][clicked_col].pawn != None):
                pawn = onitama_game.board[clicked_row][clicked_col].pawn
                dragger.save_initial(event.pos)
                dragger.drag_pawn(pawn)

        # mouse motion
        elif event.type == pygame.MOUSEMOTION:
            if dragger.dragging:
                dragger.update_blit(display.screen)

        # click release
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        
        # quit application        
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.update()

    # AI controls the blue player
    if (onitama_game.current_player.color == "blue"):
        print("Calculating AI opponent's move...")
        # all_moves = [(move, minimax.evaluation2(move.simulate_move(onitama_game))) for move in game.actions(onitama_game)]
        # print(all_moves)
        # best_tuple = max(all_moves, key=lambda x:x[1])
        # user_move = best_tuple[0]

        user_move = minimax.alpha_beta_cutoff_search(onitama_game, game, 4, None, eval_fn=minimax.evaluation3)

    # Human controls the red player    
    else:
        # collect input from the user
        print("Input formatting: (row,col)[L/R](row,col)")
        print("Enter your move: ")
        user_input = input()

        # convert that input into a Move object
        user_move = format_input(user_input, onitama_game)

        # loop until they format properly   
        while (user_move == None or not user_move.is_valid(onitama_game, onitama_game.current_player)):
            onitama_game.print_game_state()
            print("Your input was rejected.")
            print("Input formatting: (row,col)[L/R](row,col)")
            print("Enter your move: ")
            user_input = input()
            user_move = format_input(user_input, onitama_game)

    # perform that move
    user_move.perform_move(onitama_game, onitama_game.current_player)
    

onitama_game.print_game_state()
print(onitama_game.game_is_over())
