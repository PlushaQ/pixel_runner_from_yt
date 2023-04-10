import pygame
from .interface import Interface

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
