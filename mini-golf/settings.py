class Settings:
    """A class to store mini-golf game settings."""
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BG_COLOR = (90, 170, 56)

        # Ball settings
        self.ball_size = 16
        self.ball_acceleration = 0.1
        self.ball_velocity = 0

