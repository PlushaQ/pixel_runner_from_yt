import pygame
from random import randint, choice
from sys import exit


class Interface:
    """ Class to show and manage interface"""
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Pixel Runner")
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        # Initialize main images
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()
        # Set clock and bg music
        self.clock = pygame.time.Clock()
        self.bg_music = pygame.mixer.Sound('audio/music.wav')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)
        # Set start time
        self.start_time = 0
        # Initialize texts and images for intro and end screen
        self.player_stand = pygame.image.load('graphics/Player/player_stand.png')

    def show_background(self):
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))

    def display_score(self):
        current_time = pygame.time.get_ticks() - self.start_time
        score_surface = self.font.render(f'Score: {current_time // 1000}', False, '#404040')
        score_rect = score_surface.get_rect(center=(400, 50))
        self.screen.blit(score_surface, score_rect)
        return current_time // 1000

    def show_intro_and_end_screen(self):
        self.screen.fill('#5e81a2')
        welcome_text = self.font.render("Pixel Runner", False, 'Black')
        welcome_text_rect = welcome_text.get_rect(center=(400, 50))

        player_stand = pygame.transform.rotozoom(self.player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center=(400, 200))

        instruction_text = self.font.render("Press SPACE to run!", False, 'Black')
        instruction_text_rect = instruction_text.get_rect(center=(400, 350))
        self.screen.blit(player_stand, player_stand_rect)
        self.screen.blit(welcome_text, welcome_text_rect)
        score_message = self.font.render(f"Your score: {score}!", False, 'Black')
        score_message_rect = score_message.get_rect(center=(400, 330))
        if self.start_time == 0:
            self.screen.blit(instruction_text, instruction_text_rect)
        else:
            self.screen.blit(score_message, score_message_rect)


interface = Interface()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.walk = [player_walk_1, player_walk_2]
        self.jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_index = 0

        self.image = self.walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animations(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.walk):
                self.player_index = 0
            self.image = self.walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animations()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        if type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.anim_index = 0
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

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
        if self.rect.x <= -100:
            self.kill()


class Game:
    def __init__(self):
        self.run = True
        self.game_active = False
        # Groups
        self.player = pygame.sprite.GroupSingle(Player())
        self.obstacles = pygame.sprite.Group()

        # Timers
        self.obstacle_timer = pygame.USEREVENT + 1
        self.snail_animations_timer = pygame.USEREVENT + 2
        self.fly_animations_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(self.obstacle_timer, 1400)
        pygame.time.set_timer(self.snail_animations_timer, 500)
        pygame.time.set_timer(self.fly_animations_timer, 200)

    def collisions_sprite(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, True):
            self.obstacles.empty()
            return False
        return True


score = 0


game = Game()

while game.run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(1)
        if game.game_active:
            if event.type == game.obstacle_timer:
                game.obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.game_active = True
                    interface.start_time = pygame.time.get_ticks()

    if game.game_active:
        interface.show_background()
        score = interface.display_score()

        game.player.draw(interface.screen)
        game.player.update()

        game.obstacles.draw(interface.screen)
        game.obstacles.update()

        game.game_active = game.collisions_sprite()

    else:
        interface.show_intro_and_end_screen()

    pygame.display.update()
    interface.clock.tick(60)
