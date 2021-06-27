import pygame
import random

from gameObject import GameObject
from player import Player
from platform import Platform
from collectible import Collectible


class Game:

    def __init__(self):
        self.called_to_exit = False
        self.width = 1200
        self.height = 800
        self.color = (159, 237, 247)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.sky = GameObject(0, -14197, self.width, 14997, 'assets/sky.png')
        self.clouds = GameObject(0, 0, self.width, self.height, 'assets/clouds.png')
        self.jump_key = pygame.K_SPACE
        self.turn_key = pygame.K_LCTRL
        self.platforms = []
        self.HEART = 'heart'
        self.heart_img = pygame.transform.scale(pygame.image.load('assets/life_heart.png'), (120, 120))
        self.COIN = 'coin'
        self.coin_img = pygame.transform.scale(pygame.image.load('assets/coin.png'), (120, 120))

        self.set_platforms()
        self.player = Player(540, 650, 120, 120, 'assets/blue_stand.png',
                             ['assets/blue_jump_1.png', 'assets/blue_jump_2.png',
                              'assets/blue_jump_3.png', 'assets/blue_jump_4.png'],
                             'assets/blue_loss_face.png'
                             )

        self.clock = pygame.time.Clock()

    def set_platforms(self):
        self.platforms = [
            Platform(540, 650, 120, 120, 'assets/platform.png'),
            Platform(440, 550, 120, 120, 'assets/platform.png')
        ]
        while len(self.platforms) < 9:
            rand = random.choice([-100, 100])
            self.platforms.append(
                Platform(
                    (self.platforms[-1].x + rand),
                    (self.platforms[-1].y - 100),
                    120, 120, 'assets/platform.png')
            )

    def set_item(self, platform):
        def has_coin():
            roll = random.randint(0, 5)
            if roll == 5:
                return True
            return False

        def has_life_heart():
            roll = random.randint(0, 1000)
            if roll == 1000 or (self.player.score and (self.player.score + 9) % 1000 == 0):
                return True
            return False
        if has_coin():
            platform.item = Collectible(platform.x, platform.y, 120, 120, 'assets/coin.png', self.COIN)
        elif has_life_heart():
            platform.item = Collectible(platform.x, platform.y, 120, 120, 'assets/life_heart.png', self.HEART)

    def player_jump(self, direction):
        self.sky.y += 1
        i = 0
        while i < 4:
            for platform in self.platforms:
                platform.x += direction * 25
                platform.y += 25
            self.draw_scene()
            self.draw_player_jump(i)
            i += 1
        if not self.player.just_revived:
            if len(self.platforms) == 10:
                self.platforms.pop(0)
            rand = random.choice([-100, 100])
            self.platforms.append(
                Platform(
                    (self.platforms[-1].x + rand),
                    (self.platforms[-1].y - 100),
                    120, 120, 'assets/platform.png')
            )
            self.set_item(self.platforms[-1])
        self.player.just_revived = False

    def is_on_platform(self):
        for platform in self.platforms:
            if platform.y == self.player.y and platform.x == self.player.x:
                return platform
        return False

    def display_hub(self):
        font = pygame.font.SysFont('bauhaus', 80)
        current_score = font.render(str(self.player.score), False, (0, 0, 0))
        high_score_text = font.render(str(self.player.high_score), False, (0, 0, 0))
        total_coins = font.render(str(self.player.coins), False, (0, 0, 0))
        total_lives = font.render(str(self.player.hearts), False, (0, 0, 0))

        pygame.draw.rect(self.window, "white", (0, 0, 120, 120), border_radius=10)
        self.window.blit(current_score, (10, 30, 80, 80))

        pygame.draw.rect(self.window, "white", (0, 120, 120, 120), border_radius=10)
        self.window.blit(high_score_text, (10, 150, 80, 80))

        self.window.blit(self.coin_img, (self.width - 240, 0))
        pygame.draw.rect(self.window, "white", (self.width - 120, 0, 120, 120), border_radius=10)
        self.window.blit(total_coins, (self.width - 110, 30, 80, 80))

        self.window.blit(self.heart_img, (self.width - 240, 120))
        pygame.draw.rect(self.window, "white", (self.width - 120, 120, 120, 120), border_radius=10)
        self.window.blit(total_lives, (self.width - 110, 150, 80, 80))

    def draw_scene(self):
        self.window.blit(self.sky.image, (self.sky.x, self.sky.y))
        self.window.blit(self.clouds.image, (self.clouds.x, self.clouds.y))
        for platform in self.platforms:
            self.window.blit(platform.image, (platform.x, platform.y))
            if platform.item:
                self.window.blit(platform.item.image, (platform.x, platform.y))
        self.display_hub()

    def draw_player_stand(self):
        if self.player.direction == 1:
            self.window.blit(self.player.image_lf, (self.player.x, self.player.y))
        elif self.player.direction == -1:
            self.window.blit(self.player.image_rf, (self.player.x, self.player.y))
        pygame.display.update()

    def draw_player_jump(self, frame):
        if self.player.direction == 1:
            self.window.blit(self.player.jump_left[frame], (self.player.x, self.player.y))
        elif self.player.direction == -1:
            self.window.blit(self.player.jump_right[frame], (self.player.x, self.player.y))
        pygame.display.update()

    def draw_player_game_over(self):
        i = 0
        while self.player.y < self.height + 20:
            self.draw_scene()
            self.draw_you_fell()
            if self.player.direction == 1:
                self.window.blit(self.player.loss_face_lf, (self.player.x, self.player.y))
            elif self.player.direction == -1:
                self.window.blit(self.player.loss_face_rf, (self.player.x, self.player.y))
            pygame.display.update()
            self.player.y += i ^ 2
            i += 2

    def run_game(self):
        while not self.called_to_exit:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.called_to_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == self.jump_key or event.key == self.turn_key:
                        if event.key == self.jump_key:
                            self.player_jump(self.player.direction)
                        elif event.key == self.turn_key:
                            self.player.direction = -self.player.direction
                            self.player_jump(self.player.direction)
                        if not self.is_on_platform():
                            self.game_over_menu()
                        else:
                            self.player.score += 1
                            if self.is_on_platform().item:
                                item = self.is_on_platform().item
                                if item.type == self.COIN:
                                    self.player.coins += 1
                                elif item.type == self.HEART:
                                    self.player.hearts += 1
                                self.is_on_platform().item = None

            self.draw_scene()
            self.draw_player_stand()
            self.clock.tick(60)
        return

    def draw_you_fell(self):
        font = pygame.font.SysFont('bauhaus', 90)
        game_over_text = font.render('You Fell', False, (200, 0, 0))
        self.window.blit(game_over_text, (440, 340))

    def game_over_menu(self):
        self.draw_player_game_over()
        pygame.time.wait(1000)
        font = pygame.font.SysFont('bauhaus', 50)
        try_again = font.render('Press any key to try again', False, (200, 0, 0))
        self.window.blit(try_again, (350, 420))
        if self.player.hearts > 0:
            font = pygame.font.SysFont('bauhaus', 50)
            try_again = font.render('Press return to revive', False, (200, 0, 0))
            self.window.blit(try_again, (350, 460))
        pygame.display.update()
        pygame.event.clear()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.called_to_exit = True
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player.hearts > 0:
                            self.use_heart(self.player.direction)
                            return
                    if self.player.score > self.player.high_score:
                        self.player.high_score = self.player.score
                    self.player.score = 0
                    self.set_platforms()
                    self.sky.y = -14197
                    self.player.direction = 1
                    self.player.y = 650
                    pygame.event.clear()
                    return

    def use_heart(self, direction):
        self.player.hearts -= 1
        self.player.just_revived = True
        self.sky.y -= 1
        i = 0
        while i < 4:
            for platform in self.platforms:
                platform.x -= direction * 25
                platform.y -= 25
            self.draw_scene()
            pygame.display.update()
            i += 1
        self.player.y = 650
        self.draw_player_stand()

