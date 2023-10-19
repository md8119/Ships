import pygame
import sys

# Initialize Pygame
pygame.init()

# Get the user's current screen resolution
user_screen_info = pygame.display.Info()
user_screen_width = user_screen_info.current_w
user_screen_height = user_screen_info.current_h

# Create the size of the game window with the user's screen re4solution
WINDOW_SIZE = (user_screen_width, user_screen_height)

# OTHER CONSTANTS #
BG_COLOR = ((53, 82, 255))  # Background color

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Hexagonal Board")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BG_COLOR)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
