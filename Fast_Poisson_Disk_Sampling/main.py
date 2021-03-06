import pygame
import PoissonDiskSampling as pds

# Initialise pygame
pygame.init()

# setting variables
screenSize = [500, 500]
display_radius = 2
point_spacing = 5
number_of_samples = 5
tickSpeed = 300
colour_entropy = 0.0003

# Global variables
grid = []
points_micro_colour = 0
points_macro_colour = 0

# Define the constant colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (25, 25, 25)

# create the display
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Poisson Disk Sampling")

# Set the game refresh rate
clock = pygame.time.Clock()


def reset_game():
    # clear screen
    screen.fill(GRAY)
    # generate points
    global grid
    grid = pds.generate_points(screenSize, point_spacing, number_of_samples)
    # reset variables to help handle point colour
    global points_micro_colour
    points_micro_colour = 55
    global points_macro_colour
    points_macro_colour = 1.0


# Main program loop
reset_game()
wantsQuit = False

while not wantsQuit:
    # Set the refresh rate for the pygame graphic component
    clock.tick(tickSpeed)

    # pygame event handling loop
    for event in pygame.event.get():
        # user clicking to close window
        if event.type == pygame.QUIT:
            wantsQuit = True
        # user pressing return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()

    # Loop to draw points generated by pds module
    for i in range(0, 25):
        if grid:
            points_colour = points_micro_colour * points_macro_colour
            pygame.draw.circle(screen, [points_colour , points_colour, points_colour], grid.pop(0), display_radius)
        if points_micro_colour == 255:
            points_micro_colour = 55
        else:
            points_micro_colour += 1
        if points_macro_colour >= 0.1:
            points_macro_colour -= colour_entropy

    # Update the display with the new draw requests
    pygame.display.update()
