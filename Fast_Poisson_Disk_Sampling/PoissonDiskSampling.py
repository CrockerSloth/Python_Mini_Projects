import math
import random


def generate_points(area_size=[0, 0], cell_size=5, k=20):
    # Set up variables
    r = math.sqrt(cell_size**2 * 2)
    grid = []
    active_list = []
    point_list = []

    # Calculate number of rows and columns in grid
    rows = math.floor(area_size[0]/cell_size)
    cols = math.floor(area_size[1]/cell_size)

    # Create a list of all cells and initialise them to -1
    for cell in range(0, (rows * cols)):
        grid.append(-1)

    # Create a starting sample and add it to the grid and active list
    sample = [random.randint(0, area_size[0]), random.randint(0, area_size[1])]

    starting_row = math.floor(sample[0]/cell_size)
    starting_col = math.floor(sample[1]/cell_size)
    grid_index = starting_row + starting_col * cols

    grid[grid_index] = sample
    active_list.append(sample)
    point_list.append(sample)

    # Loop whilst there are still active points remaining
    while active_list:
        # Select a random active point from the list to use
        chosen_sample = random.choice(active_list)
        active_list.remove(chosen_sample)
        # Attempt to generate new points with k tries
        for attempts in range(0, k):
            angle = 2 * math.pi * random.random()
            distance = random.uniform(r, r*2)
            x = math.floor(distance * math.cos(angle) + chosen_sample[0])
            y = math.floor(distance * math.sin(angle) + chosen_sample[1])
            if not 0 < x < area_size[0] or not 0 < y < area_size[1]:
                continue

            # Calculate where the point is in the grid
            candidate_row = math.floor(x / cell_size)
            candidate_col = math.floor(y / cell_size)
            candidate_grid_index = candidate_row + candidate_col * cols
            if not 0 < candidate_grid_index < len(grid):
                continue

            # For each point, check the surrounding grid spaces to see if any other points are too close
            conflict = False
            for y_offset in range(-2, 3):
                if conflict:
                    break
                for x_offset in range(-2, 3):

                    # Create the index for the grid space we are checking
                    grid_check_index = candidate_row + x_offset + (candidate_col + y_offset) * cols
                    if not 0 < grid_check_index < len(grid):
                        continue

                    if grid[grid_check_index] != -1:
                        # Perform a distance check
                        x_distance = (x - grid[grid_check_index][0]) ** 2
                        y_distance = (y - grid[grid_check_index][1]) ** 2
                        distance_between_points = math.sqrt(abs(x_distance + y_distance))
                        if distance_between_points < r:
                            conflict = True
                            break

            # If there was no conflict whilst checking distance between points
            # add the point to the the grid, active list and the point list.
            if not conflict:
                grid[candidate_grid_index] = [x, y]
                active_list.append([x, y])
                point_list.append([x, y])

    return point_list
