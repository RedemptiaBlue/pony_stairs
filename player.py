import pygame
from gameObject import GameObject


class Player(GameObject):

    def __init__(self, x, y, width, height, image_path, jump_image_path, loss_face_path):
        super().__init__(x, y, width, height, image_path)

        self.image_lf = self.image
        self.image_rf = pygame.transform.flip(self.image_lf, True, False)
        images = [pygame.image.load(path) for path in jump_image_path]
        self.jump_left = [pygame.transform.scale(image, (width, height)) for image in images]
        self.jump_right = [pygame.transform.flip(self.jump_left[i], True, False) for i in range(4)]
        loss_face = pygame.image.load(loss_face_path)
        self.loss_face_lf = pygame.transform.scale(loss_face, (width, height))
        self.loss_face_rf = pygame.transform.flip(self.loss_face_lf, True, False)
        self.direction = 1
        self.score = 0
        self.high_score = 0
        self.coins = 0
        self.hearts = 0
        self.just_revived = False
