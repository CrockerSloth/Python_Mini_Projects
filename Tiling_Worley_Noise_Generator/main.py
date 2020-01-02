import pygame
import worley_noise_gen as wng

# initialise pygame
pygame.init()

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

# Setting variables
map_size = [500, 500]
iterations = 12
invert_map = True
tile_map = True

# Create a screen
surface = pygame.display.set_mode(map_size)
surface.fill(GRAY)
pygame.display.flip()

# Main game loop
want_quit = False
while not want_quit:

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            want_quit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # When return key is pressed generate a new noise map and copy it to a pixel array
                pixel_brightness_list = wng.generate_worley_noise(iterations, iterations, map_size, invert_map, tile_map)
                px_array = pygame.PixelArray(surface)

                for y in range(0, map_size[1]):
                    for x in range(0, map_size[0]):
                        b = pixel_brightness_list[x + (y * map_size[1])]
                        px_array[x, y] = (b, b, b)

                px_array.close()
                pygame.display.flip()
