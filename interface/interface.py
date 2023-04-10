import pygame


class Interface:
    """ Class to show and manage interface"""
    def __init__(self, width, height):
        # Initialize pygame
        pygame.init()
        self.screen_width = width
        self.screen_height = height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pixel Runner")
        self.font_size = 50
        self.font = pygame.font.Font('font/Pixeltype.ttf', self.font_size)
        self.bg_music = None

        # Initialize button variables to access it with Game Class
        self.button_pos = 695, 35
        self.width = 80
        self.height = 80

    def music_init(self):
        self.bg_music = pygame.mixer.Sound('audio/music.wav')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)

    def render_bg(self, sky_surface, ground_surface):
        # Function to show background of the game
        self.screen.blit(sky_surface, (0, 0))
        self.screen.blit(ground_surface, (0, 300))

    def display_score(self, score):
        # Function to display score on the top center of the game
        score_surface = self.font.render(f'Score: {score}', False, '#404040')
        score_rect = score_surface.get_rect(center=(400, 50))
        self.screen.blit(score_surface, score_rect)
        return score

    def show_scoreboard_button(self):
        pygame.draw.rect(self.screen, (0, 122, 122), (self.button_pos[0], self.button_pos[1], self.width, self.height))
        label = self.font.render("TOP", True, (255, 255, 255))
        label_pos = 710, 60
        self.screen.blit(label, label_pos)

    def show_intro_and_end_screen(self, score, player_image):
        # Function about rendering intro or end screen depending on state of game
        self.screen.fill('#5e81a2')
        welcome_text = self.font.render("Pixel Runner", False, 'Black')
        welcome_text_rect = welcome_text.get_rect(center=(400, 50))

        player_stand = player_image
        player_stand_rect = player_stand.get_rect(center=(400, 200))

        instruction_text = self.font.render("Press SPACE to run!", False, 'Black')
        instruction_text_rect = instruction_text.get_rect(center=(400, 350))

        self.screen.blit(player_stand, player_stand_rect)
        self.screen.blit(welcome_text, welcome_text_rect)
        self.show_scoreboard_button()

        score_message = self.font.render(f"Your score: {score}!", False, 'Black')
        score_message_rect = score_message.get_rect(center=(400, 330))
        if score == 0:
            self.screen.blit(instruction_text, instruction_text_rect)
        else:
            self.screen.blit(score_message, score_message_rect)


interface = Interface(800, 400)


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
