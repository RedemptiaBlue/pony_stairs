from gameObject import GameObject
import pygame


class Collectible(GameObject):

    def __init__(self, x, y, width, height, image_path, type):
        super().__init__(x, y, width, height, image_path)

        self.type = type
