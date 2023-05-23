from game_state import Game_state
from move import Move
import re
import onitama
import minimax
import copy
from graphics import *


# Main game setup and loop
pygame.init()
graphics = Graphics()
state = Game_state()
done = False
display_final = True
clicked_pawn = None
clicked_card = None
clicked_dest = None
search_space = onitama.Onitama()
graphics.show_background()
graphics.show_cards(state)
graphics.show_pawns(state)
pygame.display.update()

while not done:

    # graphics stuff for red player (human)
    if state.current_player.color == "red":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                display_final = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (clicked_pawn, clicked_card, clicked_dest) = graphics.interpret_mouse_click(pos, state, clicked_pawn, clicked_card, clicked_dest)
        if None not in [clicked_pawn, clicked_card, clicked_dest]:
            movement_index = get_movement_index(clicked_pawn, state.current_player.hand[clicked_card], clicked_dest, state)
            if (movement_index != None):
                user_move = move.Move(clicked_pawn.coordinates[0], clicked_pawn.coordinates[1], clicked_card, movement_index)
                if user_move.is_valid(state, state.current_player):
                    capture_flag = user_move.will_capture(state)
                    user_move.perform_move(state, state.current_player)
                    if capture_flag:
                        pygame.mixer.Sound.play(graphics.capture_sound)
                    else:
                        pygame.mixer.Sound.play(graphics.move_sound)
                    clicked_pawn = None
                    clicked_card = None
                    clicked_dest = None

    # otherwise current player is blue, so send off to minimax opponent    
    else:
        pygame.display.set_caption('Onitama (Calculating blue\'s move...)')
        user_move = minimax.alpha_beta_cutoff_search(state, search_space, 4, None, eval_fn=minimax.evaluation3)
        capture_flag = user_move.will_capture(state)
        user_move.perform_move(state, state.current_player)
        if capture_flag:
            pygame.mixer.Sound.play(graphics.capture_sound)
        else:
            pygame.mixer.Sound.play(graphics.move_sound)
        pygame.display.set_caption('Onitama')

    graphics.show_background()
    graphics.show_cards(state)
    graphics.show_selection(clicked_pawn, clicked_card, state)
    graphics.show_pawns(state)
    pygame.display.update()
    done = state.game_is_over() in ["red wins", "blue wins"] or done

if display_final:
    pygame.display.set_caption(state.game_is_over())
while display_final:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display_final = False
