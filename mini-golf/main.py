import pygame
import sys

from settings import Settings
from ball import Ball


class MiniGolf:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.SCREEN_WIDTH,
                                               self.settings.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Mini-Golf")

        self.ball = Ball(self)
        self.game_active = True
        self.jump = False
        self.fall = False

    def run(self):
        """The main loop for the game."""
        while self.game_active:
            self._check_events()
            self._update_screen()

        pygame.quit()
        sys.exit()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_active = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Button: 1 = left mouse button
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_y > self.ball.pos.y:
                        self.fall = True
                    elif mouse_y < self.ball.pos.y:
                        self.jump = True

    def _update_screen(self):
        self.screen.fill(self.settings.BG_COLOR)
        self.ball.draw()

        if self.jump:
            self.ball.pos.y -= self.settings.ball_velocity
            self.settings.ball_velocity += self.settings.ball_acceleration
            if self.ball.pos.y <= self.screen_rect.y:
                self.settings.ball_velocity = 0
                self.jump = False

        if self.fall:
            self.ball.pos.y += self.settings.ball_velocity
            self.settings.ball_velocity += self.settings.ball_acceleration
            if self.ball.pos.bottom >= self.screen_rect.bottom:
                self.settings.ball_velocity = 0
                self.fall = False

        pygame.display.flip()
        pygame.time.delay(10)


if __name__ == '__main__':
    game = MiniGolf()
    game.run()
