import random
import math
import copy


def distance_between_points(p1, p2):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    distance = math.sqrt(x**2 + y**2)
    return abs(distance)


def normalise_distance_list(distance_list, max_distance, invert):
    colour_list = []

    for i in distance_list:
        # Clamp the distance to the maximum distance
        if i > max_distance:
            i = max_distance

        # Normalise the values to 0 - 1 and then multiply them by 255 for the full colour range
        j = i / max_distance
        if invert:
            colour_list.append(255 - j*255)
        else:
            colour_list.append(j*255)

    return colour_list


def generate_worley_noise(grid_x, grid_y, map_size, invert=True, tiling=False):
    # Create the size of the grid tiles on the surface
    grid_size_x = math.floor(map_size[0] / grid_x)
    grid_size_y = math.floor(map_size[1] / grid_y)

    max_distance = math.sqrt((grid_size_x*2)**2 + (grid_size_y*2)**2)

    distance_list = []

    # for every grid tile create a point and assign it to a dictionary
    points_in_grid = {}
    for i in range(0, grid_x):
        for j in range(0, grid_y):
            x_offset = i * grid_size_x
            y_offset = j * grid_size_y
            x = random.randrange(0, grid_size_x) + x_offset
            y = random.randrange(0, grid_size_y) + y_offset
            point_location = [x, y]
            points_in_grid[(i, j)] = point_location

    tile_offsets = [[-1, -1], [ 0, -1], [ 1, -1],
                    [-1,  0], [ 0,  0], [ 1,  0],
                    [-1,  1], [ 0,  1], [ 1,  1]]

    # If tiling is enabled copy the grid 8 times
    if tiling:
        grid_copy = copy.deepcopy(points_in_grid)
        for offset in tile_offsets:
            if offset == [0, 0]:
                continue
            for grid in grid_copy:
                new_grid = (grid[0] + offset[0] * grid_x, grid[1] + offset[1] * grid_y)
                # Don't add grids that are too far away from the actual grid.
                if new_grid[0] < -1 or new_grid[0] > grid_x or new_grid[1] < -1 or new_grid[1] > grid_y:
                    continue
                old_point = grid_copy.get(grid)
                new_point = (old_point[0] + (map_size[0] * offset[0]),
                             old_point[1] + (map_size[1] * offset[1]))
                points_in_grid[new_grid] = new_point

    # For every pixel find out which grid it is in and measure it's distance
    # to the generated point in the grid and all neighbouring tiles.

    for y in range(0, map_size[1]):
        for x in range(0, map_size[0]):
            # Calculate what grid tile this pixel is inside
            x_grid = x // grid_size_x
            y_grid = y // grid_size_y

            distance = max_distance
            # Get the distance to each point in all nearby grid tiles and save the closest
            for grid_tile in tile_offsets:
                current_grid = (x_grid + grid_tile[0], y_grid + grid_tile[1])

                # Skip if we find an invalid grid tile
                # This isn't needed when tiling is enabled
                if points_in_grid.get(current_grid) is None:
                    continue

                # Find the distance from the point in the grid and the current pixel
                point_to_compare = points_in_grid[current_grid]
                new_distance = distance_between_points([x, y], point_to_compare)
                # Save the shortest distance
                if distance > new_distance:
                    distance = new_distance

            distance_list.append(distance)
    colour_list = normalise_distance_list(distance_list, max_distance/2, invert)

    return colour_list

