import pygame
import sys
import math
import string

# Initialize Pygame
pygame.init()
###################

# CONSTANTS
HEX_SIZE = 30
ROWS, COLUMNS = 60, 50  # The size of the board
HEX_COLOR = (104, 126, 255)
FRAME_COLOR = (244, 206, 20)
COORDINATES_OPACITY = 150   # Adjust this value for opacity (0-255)

# VARIABLES
field_coordinates = []
letters = [char for char in string.ascii_uppercase]

# Get the user's current screen resolution
user_screen_info = pygame.display.Info()
user_screen_width = user_screen_info.current_w
user_screen_height = user_screen_info.current_h

# Create the size of the game window with the user's screen re4solution
WINDOW_SIZE = (user_screen_width, user_screen_height)

# Create the game window
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
pygame.display.set_caption("Hexagonal Board")

def get_letter(index):
    try:
        return letters[index]
    except IndexError:
        # Extend the list to include double letters
        while index >= len(letters):
            new_letter = get_letter(index // 26 - 1) + get_letter(index % 26)
            letters.append(new_letter)
        return letters[index]

# Define hexagon drawing function
def draw_hexagon(x, y):
    hexagon_points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        px = x + HEX_SIZE * math.cos(angle)
        py = y + HEX_SIZE * math.sin(angle)
        hexagon_points.append((px, py))

    pygame.draw.polygon(screen, HEX_COLOR, hexagon_points)
    pygame.draw.polygon(screen, FRAME_COLOR, hexagon_points, 2)

    # Display the coordinates on the hexagon
    col_letter = get_letter(col)
    hex_font = pygame.font.Font(None, 24)
    text = hex_font.render(f'{col_letter}{col}', True, (255, 255, 255))
    text.set_alpha(COORDINATES_OPACITY)
    text_rec = text.get_rect(center=(x, y))
    screen.blit(text, text_rec)

#######################################
# MAIN LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((53, 82, 255))

    # Draw the hexagonal grid
    for row in range(ROWS):
        for col in range(COLUMNS):
            x = col * (3/2 * HEX_SIZE)
            y = row * (HEX_SIZE * math.sqrt(3))
            if col % 2 == 1:
                y += (HEX_SIZE * math.sqrt(3)) / 2
            draw_hexagon(x, y)
            field_coordinates.append((x, y))










    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
