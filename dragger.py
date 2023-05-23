import pygame
from const import *

class Dragger:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.pawn = None
        self.dragging = False
    
    def update_blit(self, surface):
        # TODO: make the pawn texture a little bit bigger when you pick it up
        pass

    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos
    
    def save_inital(self, pos):
        self.inital_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE
    
    def drag_pawn(self, pawn):
        self.pawn = pawn
        self.dragging = True
    
    def undrag_pawn(self):
        self.pawn = None
        self.dragging = False