import pygame


class Images:
    """ Class to manage all images in the game"""
    def __init__(self):
        self.sky_image = pygame.image.load('graphics/Sky.png')
        self.ground_image = pygame.image.load('graphics/ground.png')
        self.player_stand_image = pygame.image.load('graphics/Player/player_stand.png')
        self.player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png')
        self.player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png')
        self.jump_image = pygame.image.load('graphics/Player/jump.png')
        self.fly_1 = pygame.image.load('graphics/Fly/Fly1.png')
        self.fly_2 = pygame.image.load('graphics/Fly/Fly2.png')
        self.snail_1 = pygame.image.load('graphics/snail/snail1.png')
        self.snail_2 = pygame.image.load('graphics/snail/snail2.png')

    def convert_images(self):
        self.player_stand_image = pygame.transform.rotozoom(self.player_stand_image, 0, 2)
        self.ground_image.convert()
        self.sky_image.convert()
        self.player_stand_image.convert()
        self.player_walk_1.convert_alpha()
        self.player_walk_2.convert_alpha()
        self.jump_image.convert_alpha()
        self.fly_1.convert_alpha()
        self.fly_2.convert_alpha()
        self.snail_1.convert_alpha()
        self.snail_2.convert_alpha()

    def player_images(self):
        return [self.player_walk_1, self.player_walk_2, self.jump_image]

    def fly_images(self):
        return [self.fly_1, self.fly_2]

    def snail_images(self):
        return [self.snail_1, self.snail_2]
