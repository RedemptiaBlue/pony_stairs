from gameObject import GameObject
import pygame


class Platform(GameObject):

    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, image_path)

        self.item = None
