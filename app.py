import pygame
from random import choice
from sys import exit

from utils.database import Database
from interface.interface import Interface, Scoreboard
from utils.images import Images
from sprites.sprites import Player, Obstacle

db = Database()

images = Images()
interface = Interface(800, 400)
scoreboard = Scoreboard()


class Game:
    """ Main function to manage main loop, game logic and collisions"""
    def __init__(self, player):
        images.convert_images()
        interface.music_init()
        self.run = True
        self.game_active = False
        self.scoreboard_show = False
        self.score = 0
        self.start_time = 0
        self.clock = pygame.time.Clock()
        # Groups
        self.player = pygame.sprite.GroupSingle(player)
        self.obstacles = pygame.sprite.Group()

        # Timers
        self.obstacle_timer = pygame.USEREVENT + 1
        self.snail_animations_timer = pygame.USEREVENT + 2
        self.fly_animations_timer = pygame.USEREVENT + 3

    def timers_init(self):
        pygame.time.set_timer(self.obstacle_timer, 1400)
        pygame.time.set_timer(self.snail_animations_timer, 500)
        pygame.time.set_timer(self.fly_animations_timer, 200)

    def collisions_sprite(self):
        # Function to check if sprites are colliding
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacles, True):
            self.obstacles.empty()
            db.add_record(self.score)
            return False
        return True

    def calculate_score(self):
        return (pygame.time.get_ticks() - self.start_time) // 1000

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
                        obst = choice(['fly', 'snail', 'snail'])
                        if obst == 'fly':
                            self.obstacles.add(Obstacle('fly', *images.fly_images()))
                        else:
                            self.obstacles.add(Obstacle('snail', *images.snail_images()))
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
                            self.start_time = pygame.time.get_ticks()

            if self.game_active:
                # Main logic
                interface.render_bg(images.sky_image, images.ground_image)
                self.score = interface.display_score(self.calculate_score())

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
                    interface.show_intro_and_end_screen(self.score, images.player_stand_image)

            pygame.display.update()
            self.clock.tick(60)


game = Game(Player(*images.player_images()))

if __name__ == '__main__':
    game.timers_init()
    game.start_game()
