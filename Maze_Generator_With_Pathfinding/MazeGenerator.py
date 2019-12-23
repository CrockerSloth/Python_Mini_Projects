import pygame
import math
import random

# Initialise pygame
if __name__ == "__main__":
    pygame.init()

# Setting variables
maze_width = 40
maze_height = 40
cell_size = 40
tick_speed = 1
wall_size = 10

# Define the constant colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
GREEN = (0, 100, 0)
PURPLE = (218, 112, 214)
RED = (200, 0, 0)

# Define the cell offsets
cell_offsets = [[-1, 0], [0, -1], [1, 0], [0, 1]]

# Create the screen
if __name__ == "__main__":
    screen_size = [maze_width * cell_size + 1, maze_height * cell_size + 1]
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Maze Generator")
    screen.fill(WHITE)

# Set the game refresh rate
if __name__ == "__main__":
    clock = pygame.time.Clock()


# Draws rectangles across a cell pair
def draw_cell_pair_list(cell_pair_list, colour):

    # Draw a box between the current unfinished cell and the chosen cell
    for cell_pair in cell_pair_list:
        pair_offset = [cell_pair[0][0] - cell_pair[1][0], cell_pair[0][1] - cell_pair[1][1]]
        if pair_offset == [-1, 0]:
            rect = (cell_pair[0][0] * cell_size + math.floor(wall_size / 2),
                    cell_pair[0][1] * cell_size + math.floor(wall_size / 2),
                    cell_size * 2 - wall_size,
                    cell_size - wall_size)
        elif pair_offset == [0, -1]:
            rect = (cell_pair[0][0] * cell_size + math.floor(wall_size / 2),
                    cell_pair[0][1] * cell_size + math.floor(wall_size / 2),
                    cell_size - wall_size,
                    cell_size * 2 - wall_size)
        elif pair_offset == [1, 0]:
            rect = (cell_pair[1][0] * cell_size + math.floor(wall_size / 2),
                    cell_pair[1][1] * cell_size + math.floor(wall_size / 2),
                    cell_size * 2 - wall_size,
                    cell_size - wall_size)
        else:
            rect = (cell_pair[1][0] * cell_size + math.floor(wall_size / 2),
                    cell_pair[1][1] * cell_size + math.floor(wall_size / 2),
                    cell_size - wall_size,
                    cell_size * 2 - wall_size)
        screen.fill(colour, rect)
        pygame.display.update()


# Recursive backtracking implementation
def generate_maze(auto_draw=True):
    # create a starting cell and lists to contain the current stack
    visited_cells = [[0, 0]]
    unfinished_cells = visited_cells[:]
    maze_cells = []

    # Whilst there are remaining cells continue to generate paths
    while len(visited_cells) < maze_height * maze_width:

        # Loop for the current cell at the top of the stack
        cell_offsets_copy = cell_offsets[:]
        while cell_offsets_copy:
            # Choose a random cell offset and create a chosen cell using that offset
            current_offset = cell_offsets_copy.pop(random.randrange(0, len(cell_offsets_copy)))
            chosen_cell = [unfinished_cells[-1][0] + current_offset[0], unfinished_cells[-1][1] + current_offset[1]]

            # Discard chosen cell if it isn't in the grid
            if not 0 <= chosen_cell[0] < maze_width or not 0 <= chosen_cell[1] < maze_height:
                continue

            if chosen_cell not in visited_cells:
                # encode maze as pairs of connected cells
                maze_cells.append([unfinished_cells[-1], chosen_cell])

                if auto_draw:
                    draw_cell_pair_list([[unfinished_cells[-1], chosen_cell]], GRAY)

                # add the chosen cell to the visited_cells list and unfinished list
                visited_cells.append(chosen_cell)
                unfinished_cells.append(chosen_cell)
                # Break from this current loop
                break

        else:
            # Remove this cell from the unfinished cells list
            unfinished_cells.pop()

    return maze_cells


# Remove random walls from the maze to open up possible paths
def erode_maze(maze_cells, attempts):
    maze = maze_cells

    for i in range(0, attempts):
        chosen_cell = [random.randint(1, maze_width - 2), random.randint(1, maze_height - 2)]
        offset = random.choice(cell_offsets)
        paired_cell = [chosen_cell[0] + offset[0], chosen_cell[1] + offset[1]]

        if [chosen_cell, paired_cell] not in maze and [paired_cell, chosen_cell] not in maze:
            maze.append([chosen_cell, paired_cell])

    return maze


# Node class for use in A* path finding
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# A* path finding implementation
def solve_maze(maze_cells, start_position, end_position):

    # Create start and end node
    start_node = Node(None, start_position)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end_position)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Find the node on the open list with the lowest F cost
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Take the node from the open list and add it to the closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # If the node is the end node then return the path by moving through the parent nodes
        if current_node == end_node:
            path = []
            current = current_node
            while current.parent is not None:
                path.append([current.position, current.parent.position])
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in cell_offsets:

            # Get node position by using the cell offset list for valid movements
            node_position = [current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1]]

            # Make sure the node is on the grid
            if not 0 <= node_position[0] < maze_width or not 0 <= node_position[1] < maze_height:
                continue

            # Make sure the two nodes are connected (no walls between them in the maze)
            if ([current_node.position, node_position] not in maze_cells and
                    [node_position, current_node.position] not in maze_cells):
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append the new node to the child list
            children.append(new_node)

        # Loop through children
        for child in children:
            is_valid = True

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    is_valid = False

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node:
                    is_valid = False
                    if child.g < open_node.g:
                        open_node.parent = child.parent
                        open_node.g = child.g
                        open_node.f = child.f

            # Add the child to the open list
            if is_valid:
                open_list.append(child)


# main game loop
if __name__ == "__main__":
    wantsQuit = False
    while not wantsQuit:
        # Set the refresh rate for the pygame graphic component
        clock.tick(tick_speed)

        # pygame event handling loop
        for event in pygame.event.get():
            # user clicking to close window
            if event.type == pygame.QUIT:
                wantsQuit = True
            # user pressing return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    screen.fill(WHITE)
                    generated_maze = generate_maze(False)
                    generated_maze = erode_maze(generated_maze, 200)
                    draw_cell_pair_list(generated_maze, GRAY)
                    solved_path = solve_maze(generated_maze, [0, 0], [maze_width - 1, maze_height - 1])
                    draw_cell_pair_list(solved_path, GREEN)

        # Update the display with the new draw requests
        pygame.display.update()
