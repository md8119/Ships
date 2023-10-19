import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
HEX_SIZE = 30
ROWS, COLUMNS = 60, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ZOOM_SPEED = 0.1  # Adjust the zoom speed as needed
MIN_ZOOM = 0.4
MAX_ZOOM = 2.5
MOVE_SPEED = 10  # Adjust the move speed as needed
SIDE_WINDOW_FRACTION = 0.25

# Get the user current screen resolution
user_screen_info = pygame.display.Info()
user_screen_width = user_screen_info.current_w
user_screen_height = user_screen_info.current_h

# Define the dimension and position of the right window
RIGHT_WINDOW_WIDTH = int(user_screen_width * SIDE_WINDOW_FRACTION)
RIGHT_WINDOW_HEIGHT = user_screen_height
RIGHT_WINDOW_X = (user_screen_width - RIGHT_WINDOW_WIDTH)

# Create a separate window surface for the right section
right_window = pygame.Surface((RIGHT_WINDOW_WIDTH, RIGHT_WINDOW_HEIGHT))

# Initialize the screen
screen = pygame.display.set_mode((user_screen_width, user_screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Hexagonal Board")

# Initial zoom level
initial_zoom = user_screen_width / (COLUMNS * (3/2 * HEX_SIZE))
zoom = max(MIN_ZOOM, initial_zoom)

# Initial board position for alignment
board_x = 0
board_y = 0

# Add mouse drag variables
mouse_dragging = False
mouse_x, mouse_y = 0, 0


# Define hexagon drawing function
def draw_hexagon(x, y):
    hexagon_points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        px = x + HEX_SIZE * zoom * math.cos(angle)
        py = y + HEX_SIZE * zoom * math.sin(angle)
        hexagon_points.append((px, py))
    
    border_thickness = max(1, int(3 * zoom))    # Initial border thickness, 1 is min thickness, next nr regulate thickness
    pygame.draw.polygon(screen, (104, 126, 255), hexagon_points)    # Set the hexagon fill colour
    pygame.draw.polygon(screen, (244, 206, 20), hexagon_points, border_thickness)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll Up (Zoom In)
                zoom += ZOOM_SPEED
            elif event.button == 5:  # Scroll Down (Zoom Out)
                zoom -= ZOOM_SPEED
            elif event.button == 1: # Left Mouse Button (Start Dragging)
                mouse_dragging = True
                mouse_x, mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left Mouse Button (Stop Dragging)
                mouse_dragging = False

    # Calculate the center of the board
    center_x = (COLUMNS - 1) * (3/2 * HEX_SIZE * zoom) / 2
    center_y = (ROWS - 1) * (HEX_SIZE * math.sqrt(3) * zoom) / 2

    # Adjust center_x to account for the right window width
    center_x += RIGHT_WINDOW_WIDTH / 2

    

    
    # Adjust board_x and board_y to center the board
    board_x = user_screen_width / 2 - center_x
    board_y = user_screen_height / 2 - center_y

    # Add the zoom limits
    available_screen_width = user_screen_width * (1.0 - SIDE_WINDOW_FRACTION)
    # Calculate the zoom factor based on the center of the board
    centered_zoom = user_screen_width / (COLUMNS * (3/2 * HEX_SIZE))  # Zoom to fit the width
    zoom = max(MIN_ZOOM, min(zoom, MAX_ZOOM))
    min_zoom_to_fit_width = available_screen_width / (COLUMNS * (3/2 * HEX_SIZE))
    min_zoom_to_fit_width *= 0.95   # Add 5% to the minimum zoom level
    MIN_ZOOM = max(MIN_ZOOM, min_zoom_to_fit_width)

    # Update zoom to the minimum of MIN_ZOOM and centered_zoom
    zoom = max(MIN_ZOOM, min(centered_zoom, MAX_ZOOM))

    # Calculate the adjusted horizontal and vertical distances
    horiz = 3/2 * HEX_SIZE * zoom
    vert = HEX_SIZE * math.sqrt(3) * zoom

    # Calculate the board boundaries
    adjusted_hex_size = HEX_SIZE * zoom
    board_left_boundary = -user_screen_width + adjusted_hex_size
    board_right_boundary = (COLUMNS - 1) * horiz + user_screen_width - adjusted_hex_size
    board_top_boundary = -user_screen_height + adjusted_hex_size
    board_bottom_boundary = (ROWS - 1) * vert + user_screen_height - adjusted_hex_size

    # Ensure the board boundaries account for the adjusted hexagon size
    if board_right_boundary < user_screen_width:
        board_left_boundary += user_screen_width - board_right_boundary
        board_right_boundary = user_screen_width

    if board_bottom_boundary < user_screen_height:
        board_top_boundary += user_screen_height - board_bottom_boundary
        board_bottom_boundary = user_screen_height



    # Move the board using arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        board_x -= MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        board_x += MOVE_SPEED
    if keys[pygame.K_UP]:
        board_y += MOVE_SPEED
    if keys[pygame.K_DOWN]:
        board_y -= MOVE_SPEED


    # Update board position based on mouse drag
    if mouse_dragging:
        new_mouse_x, new_mouse_y = pygame.mouse.get_pos()
        delta_x = new_mouse_x - mouse_x
        delta_y = new_mouse_y - mouse_y

        # Calculate the potential board position is within boundaries
        new_board_x = max(board_left_boundary, min(board_right_boundary, board_x + delta_x))
        new_board_y = max(board_top_boundary, min(board_bottom_boundary, board_y + delta_y))

        board_x, board_y = new_board_x, new_board_y
        mouse_x, mouse_y = new_mouse_x, new_mouse_y


        mouse_x, mouse_y = new_mouse_x, new_mouse_y

    # Clear the screen
    screen.fill((53,82,255))

    # Draw the hexagonal grid
    for row in range(ROWS):
        for col in range(COLUMNS):
            x = col * horiz + board_x
            y = row * vert + (col % 2) * (HEX_SIZE * zoom * 0.87) + board_y
            draw_hexagon(x, y)


    # Draw the content for the right section
    right_window.fill((200, 200, 200))

    # Blit the right window onto the main screen
    screen.blit(right_window, (RIGHT_WINDOW_X, 0))


    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
