import pygame
from utils.images import Images

images = Images()


class Interface:
    """ Class to show and manage interface"""
    def __init__(self, width, height):
        # Initialize pygame
        pygame.init()
        self.screen_width = width
        self.screen_height = height
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
