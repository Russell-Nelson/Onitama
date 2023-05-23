class Pawn:
    # Member variables
    # bool is_master: true for a master pawn ("king") only
    # string color: either "red" or "blue"
    # (int, int) coordinates: the (row, col) position of this pawn
    # string texture: a path to the image file for this piece
    # rect texture_rect: updated by img.get_rect() from pygame


    def __init__(self, is_master, color, coordinates, texture=None, texture_rect=None):
        self.is_master = is_master

        self.color = color

        self.coordinates = coordinates

        self.texture = texture
        self.set_texture()

        self.texture_rect = texture_rect
    
    def set_texture(self):
        if self.is_master:
            self.texture = f'images\pawns\{self.color}_master_pawn.png'
        else:
            self.texture = f'images\pawns\{self.color}_pawn.png'
