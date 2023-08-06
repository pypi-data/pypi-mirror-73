
import arcade
import time

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Example"


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.score = 0

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """ Draw everything """
        self.score += 1
        start_time = time.time()
        arcade.start_render()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        end_time = time.time()
        print(f"{end_time - start_time:.5f}")


def main():
    """ Main method """
    window = MyGame()
    arcade.run()


if __name__ == "__main__":
    main()
