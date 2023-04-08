import pygame
from random import randint, choice
from sys import exit

from database import Database

db = Database()


class Images:
    """ Class to manage all images in the game"""
    def __init__(self):
        self.sky_image = pygame.image.load('graphics/Sky.png')
        self.ground_image = pygame.image.load('graphics/ground.png')
        self.player_image = pygame.image.load('graphics/Player/player_stand.png')
        self.player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png')
        self.player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png')
        self.jump_image = pygame.image.load('graphics/Player/jump.png')
        self.fly_1 = pygame.image.load('graphics/Fly/Fly1.png')
        self.fly_2 = pygame.image.load('graphics/Fly/Fly2.png')
        self.snail_1 = pygame.image.load('graphics/snail/snail1.png')
        self.snail_2 = pygame.image.load('graphics/snail/snail2.png')

    def convert_images(self):
        self.player_image = pygame.transform.rotozoom(self.player_image, 0, 2)
        self.ground_image.convert()
        self.sky_image.convert()
        self.player_image.convert()
        self.player_walk_1.convert_alpha()
        self.player_walk_2.convert_alpha()
        self.jump_image.convert_alpha()
        self.fly_1.convert_alpha()
        self.fly_2.convert_alpha()
        self.snail_1.convert_alpha()
        self.snail_2.convert_alpha()


images = Images()


class Interface:
    """ Class to show and manage interface"""
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width , self.screen_height))
        pygame.display.set_caption("Pixel Runner")
        images.convert_images()
        self.font_size = 50
        self.font = pygame.font.Font('font/Pixeltype.ttf', self.font_size)
        # Initialize main images
        self.sky_surface = images.sky_image
        self.ground_surface = images.ground_image
        # Set clock and bg music
        self.clock = pygame.time.Clock()
        self.bg_music = pygame.mixer.Sound('audio/music.wav')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)
        # Set scoring
        self.start_time = 0
        self.score = 0
        # Initialize texts and images for intro and end screen
        self.player_stand = images.player_image

        # Initialize button variables
        self.button_pos = 695, 35
        self.width = 80
        self.height = 80

    def show_background(self):
        # Function to show background of the game
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))

    def display_score(self):
        # Function to display score on the top center of the game
        current_time = pygame.time.get_ticks() - self.start_time
        score_surface = self.font.render(f'Score: {current_time // 1000}', False, '#404040')
        score_rect = score_surface.get_rect(center=(400, 50))
        self.screen.blit(score_surface, score_rect)
        return current_time // 1000

    def show_scoreboard_button(self):
        pygame.draw.rect(self.screen, (0, 122, 122), (self.button_pos[0], self.button_pos[1], self.width, self.height))
        label = self.font.render("TOP", True, (255, 255, 255))
        label_pos = 710, 60
        self.screen.blit(label, label_pos)

    def show_intro_and_end_screen(self):
        # Function about rendering intro or end screen depending on state of game
        self.screen.fill('#5e81a2')
        welcome_text = self.font.render("Pixel Runner", False, 'Black')
        welcome_text_rect = welcome_text.get_rect(center=(400, 50))

        player_stand = images.player_image
        player_stand_rect = player_stand.get_rect(center=(400, 200))

        instruction_text = self.font.render("Press SPACE to run!", False, 'Black')
        instruction_text_rect = instruction_text.get_rect(center=(400, 350))

        self.screen.blit(player_stand, player_stand_rect)
        self.screen.blit(welcome_text, welcome_text_rect)
        self.show_scoreboard_button()

        score_message = self.font.render(f"Your score: {self.score}!", False, 'Black')
        score_message_rect = score_message.get_rect(center=(400, 330))
        if self.start_time == 0:
            self.screen.blit(instruction_text, instruction_text_rect)
        else:
            self.screen.blit(score_message, score_message_rect)


interface = Interface()


class Scoreboard:
    def __init__(self):
        self.scoreboard_pos = (400, 200)
        self.scoreboard_width = 300
        self.scoreboard_height = 300
        self.scoreboard_color = (0, 122, 122)
        self.scoreboard_border_color = (0, 0, 0)
        self.scoreboard_border_width = 2
        self.scoreboard_label = "SCOREBOARD"
        self.scoreboard_label_color = (0, 0, 0)
        self.scoreboard_label_pos = (
            self.scoreboard_pos[0] - self.scoreboard_width // 2, self.scoreboard_pos[1] - self.scoreboard_height // 2
        )

    def show_scoreboard(self, scores):
        # Draw the scoreboard background and border
        pygame.draw.rect(interface.screen, self.scoreboard_color, (
            self.scoreboard_pos[0] - self.scoreboard_width // 2,
            self.scoreboard_pos[1] - self.scoreboard_height // 2,
            self.scoreboard_width, self.scoreboard_height
        ))
        pygame.draw.rect(interface.screen, self.scoreboard_border_color, (
            self.scoreboard_pos[0] - self.scoreboard_width // 2,
            self.scoreboard_pos[1] - self.scoreboard_height // 2,
            self.scoreboard_width, self.scoreboard_height
        ), self.scoreboard_border_width)

        # Draw the scoreboard label
        label = interface.font.render(self.scoreboard_label, True, self.scoreboard_label_color)
        label_pos = (300, 65)
        interface.screen.blit(label, label_pos)

        # Draw the scores
        for i in range(len(scores)):
            score_label = interface.font.render(f'{i + 1}. {scores[i][0]} points ', True, self.scoreboard_label_color)

            score_pos = (self.scoreboard_pos[0] - self.scoreboard_width // 2 + interface.font_size,
                         self.scoreboard_pos[1] - self.scoreboard_height // 2 + interface.font_size + (
                                     i * interface.font_size))
            interface.screen.blit(score_label, score_pos)


scoreboard = Scoreboard()


class Player(pygame.sprite.Sprite):
    """ Class to manage Player related functions """
    def __init__(self):
        super().__init__()
        player_walk_1 = images.player_walk_1
        player_walk_2 = images.player_walk_2
        self.walk = [player_walk_1, player_walk_2]
        self.jump_image = images.jump_image
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
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = images.fly_1
            fly_2 = images.fly_2
            self.frames = [fly_1, fly_2]
            y_pos = 210
        if type == 'snail':
            snail_1 = images.snail_1
            snail_2 = images.snail_2
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
        # Function to destroy sprite when it's not in the screen anymore
        if self.rect.x <= -100:
            self.kill()


class Game:
    """ Main function to manage main loop, game logic and collisions"""
    def __init__(self):
        self.run = True
        self.game_active = False
        self.scoreboard_show = False

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
        # Function to check if sprites are colliding
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, True):
            self.obstacles.empty()
            db.add_record(interface.score)
            return False
        return True

    def start_game(self):
        # Main loop
        while self.run:
            # Event checking loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(1)
                if game.game_active:
                    if event.type == game.obstacle_timer:
                        self.obstacles.add(Obstacle(choice(['fly', 'snail', 'snail'])))
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if game.scoreboard_show:
                            self.scoreboard_show = False
                        if interface.button_pos[0] <= mouse_pos[0] <= interface.button_pos[0] + interface.width and \
                                interface.button_pos[1] <= mouse_pos[1] <= interface.button_pos[1] + interface.width:
                            # Show scoreboard when button is clicked
                            self.scoreboard_show = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_active = True
                            interface.start_time = pygame.time.get_ticks()

            if self.game_active:
                # Main logic
                interface.show_background()
                interface.score = interface.display_score()

                self.player.draw(interface.screen)
                self.player.update()

                self.obstacles.draw(interface.screen)
                self.obstacles.update()

                self.game_active = self.collisions_sprite()

            else:
                # Screen showing on start or end game
                if self.scoreboard_show:
                    scoreboard.show_scoreboard(db.get_top_five())
                else:
                    interface.show_intro_and_end_screen()

            pygame.display.update()
            interface.clock.tick(60)


game = Game()

if __name__ == '__main__':
    game.start_game()
