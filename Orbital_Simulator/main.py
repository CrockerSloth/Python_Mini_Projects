import pygame
import orbit_simulation as orb
import random

# Initialise pygame
pygame.init()

# Setting variables
screen_size = (1920, 1080)

# Constant colour variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (20, 20, 20)

# Create the screen
screen = pygame.display.set_mode(screen_size)
screen.fill(GRAY)
pygame.display.update()

# Import the tick function
clock = pygame.time.Clock()

# Input variables
wants_quit = False
mouse_down = False
draw_trails = False

# Initialise the orbital simulator
orb.init(screen_size)

# Instructions
print("==================")
print("Orbital Simulation")
print("==================")
print("Click and drag with the mouse to spawn orbitals")
print("==================")
print("ENTER - add a static planet to the center of the screen")
print("DELETE - delete all orbitals")
print("P - toggle show orbital paths")
print("BACKSPACE - delete current orbital paths")
print("==================")

# Main game Loop
orb_location = []
while not wants_quit:

    # Update tick speed
    clock.tick(30)

    # pygame event handling loop
    for event in pygame.event.get():
        # user clicking to close window
        if event.type == pygame.QUIT:
            wantsQuit = True
        # user pressing return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                orb.spawn_orbital([screen_size[0]/2, screen_size[1]/2], [0, 0], 10000, True)

            if event.key == pygame.K_BACKSPACE:
                screen.fill(GRAY)

            if event.key == pygame.K_p:
                draw_trails = not draw_trails

            if event.key == pygame.K_DELETE:
                orb.orbital_list = []

        elif event.type == pygame.MOUSEBUTTONDOWN and not mouse_down:
            mouse_down = True
            orb_location = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP and mouse_down:
            mouse_down = False
            release_location = pygame.mouse.get_pos()
            orb_velocity = [(orb_location[0] - release_location[0])/10,
                            (orb_location[1] - release_location[1])/10]

            orb.spawn_orbital(orb_location, orb_velocity, random.randint(50, 100), False)

    # redraw screen and orbitals
    if not draw_trails:
        screen.fill(GRAY)
    for orbital in orb.return_orbital_list():
        location = orbital.location
        colour_by_mass = (orbital.radius * 5) + 100
        if colour_by_mass >= 255:
            colour_by_mass = 255
        colour = [colour_by_mass, colour_by_mass, colour_by_mass]
        pygame.draw.circle(screen, colour, [int(location[0]), int(location[1])], orbital.radius)
    pygame.display.flip()

    # Update the position of all orbitals
    orb.update_orbitals()

