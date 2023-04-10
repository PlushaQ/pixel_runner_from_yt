import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    """ Class to manage Player related functions """
    def __init__(self, player_walk_1, player_walk_2, jump_image):
        super().__init__()
        player_walk_1 = player_walk_1
        player_walk_2 = player_walk_2
        self.walk = [player_walk_1, player_walk_2]
        self.jump_image = jump_image
        self.player_index = 0

        self.image = self.walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def jump(self):
        # Player jump function
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        # Simple logic imitating gravity
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animations(self):
        # Function changing images to animate
        if self.rect.bottom < 300:
            self.image = self.jump_image
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.walk):
                self.player_index = 0
            self.image = self.walk[int(self.player_index)]

    def update(self):
        self.jump()
        self.apply_gravity()
        self.animations()


class Obstacle(pygame.sprite.Sprite):
    """ Class managing Obstacles and its dependencies"""
    def __init__(self, type, img_1, img_2):
        super().__init__()
        self.y_pos = 0
        self.frames = [img_1, img_2]
        if type == 'fly':
            self.y_pos = 210
        if type == 'snail':
            self.y_pos = 300

        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self.y_pos))

    def animations(self):
        self.anim_index += 0.1
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def update(self):
        self.animations()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        # Function to destroy sprite when it's not in the screen anymore
        if self.rect.x <= -100:
            self.kill()
