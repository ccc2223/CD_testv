# main.py
import pygame
import sys
from game import Game
from config import WINDOW_WIDTH, WINDOW_HEIGHT

def main():
    """
    Main entry point for the Castle Defense game.
    Initializes Pygame and starts the game loop.
    """
    # Initialize Pygame
    pygame.init()
    
    # Create game window with dimensions from config
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Castle Defense")
    
    # Set window icon if desired
    # icon = pygame.image.load("assets/icon.png")
    # pygame.display.set_icon(icon)
    
    # Create and run game
    game = Game(screen)
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
