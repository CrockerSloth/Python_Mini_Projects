

import random
import math

# settings
gravity = 6
proximity_dampening = 100

area_size = []
orbital_list = []


def init(area_size_input):
    global area_size
    area_size = area_size_input


class Orbital:
    def __init__(self, location, velocity, mass, static):
        self.id = random.random()
        self.location = location
        self.velocity = velocity
        self.static = static
        self.mass = mass
        self.radius = 0
        self.calculate_radius()

    def __eq__(self, other):
        return self.id == other.id and self.location == other.location

    def calculate_radius(self):
        self.radius = math.floor(math.sqrt(self.mass) / math.pi) + 1


def spawn_orbital(location, velocity, mass, static):
    orbital = Orbital(location, velocity, mass, static)

    orbital_list.append(orbital)


def return_orbital_list():
    return orbital_list


def update_orbitals():

    # For every orbital update their velocity and then calculate their next location
    for orbital in orbital_list:
        for other_orb in orbital_list:

            # If it's the same orbital then we skip
            if other_orb == orbital:
                continue

            # ### calculate the distance between the orbitals ###
            # Create values for screen wrap in both directions
            negative_wrap_x = ((other_orb.location[0] - area_size[0]) - orbital.location[0])
            positive_wrap_x = ((other_orb.location[0] + area_size[0]) - orbital.location[0])
            x = (other_orb.location[0] - orbital.location[0])

            negative_wrap_y = ((other_orb.location[1] - area_size[1]) - orbital.location[1])
            positive_wrap_y = ((other_orb.location[1] + area_size[1]) - orbital.location[1])
            y = (other_orb.location[1] - orbital.location[1])

            # Select the lowest of the distances
            if abs(negative_wrap_x) < abs(x) and abs(negative_wrap_x) < abs(positive_wrap_x):
                x = negative_wrap_x
            elif abs(positive_wrap_x) < abs(x):
                x = positive_wrap_x

            if abs(negative_wrap_y) < abs(y) and abs(negative_wrap_y) < abs(positive_wrap_y):
                y = negative_wrap_y
            elif abs(positive_wrap_y) < abs(y):
                y = positive_wrap_y

            # Calculate the distance using the shortest path accounting for screen wrap
            distance = math.sqrt(abs(x)**2 + abs(y)**2)

            # Combine any orbitals that get too close
            if distance < orbital.radius + other_orb.radius:
                if orbital.mass >= other_orb.mass:
                    orbital.mass += other_orb.mass
                    # Create a new velocity using a split of the velocity from each mass
                    smaller_ratio = other_orb.mass / (other_orb.mass + orbital.mass)
                    larger_ratio = 1 - smaller_ratio
                    orbital.velocity[0] = orbital.velocity[0]*larger_ratio + other_orb.velocity[0]*smaller_ratio
                    orbital.velocity[0] = orbital.velocity[1]*larger_ratio + other_orb.velocity[1]*smaller_ratio
                    orbital.calculate_radius()
                    orbital_list.remove(other_orb)
                    continue
                else:
                    other_orb.mass += orbital.mass
                    # Create a new velocity using a split of the velocity from each mass
                    smaller_ratio = orbital.mass / (other_orb.mass + orbital.mass)
                    larger_ratio = 1 - smaller_ratio
                    orbital.velocity[0] = other_orb.velocity[0]*larger_ratio + orbital.velocity[0]*smaller_ratio
                    orbital.velocity[0] = other_orb.velocity[1]*larger_ratio + orbital.velocity[1]*smaller_ratio
                    orbital.calculate_radius()
                    orbital_list.remove(orbital)
                    continue

            if orbital.static:
                continue

            # Calculate the strength of the pull towards the other orbital
            if distance > 0:  # redundant safety measure. orbitals should combine before this becomes a problem
                f_gravity = (gravity * (orbital.mass * other_orb.mass))/(distance**2 + proximity_dampening)

            # normalise direction to the other orbital
            normalise_direction = [(x / distance), (y / distance)]

            # Split the gravity force based on the objects mass
            magnitude = f_gravity / orbital.mass

            # Apply the remaining force to the current velocity
            orbital.velocity[0] += normalise_direction[0] * magnitude
            orbital.velocity[1] += normalise_direction[1] * magnitude

        # Update the orbitals current location by applying its velocity
        if not orbital.static:
            orbital.location = [(orbital.location[0] + orbital.velocity[0]) % area_size[0],
                                (orbital.location[1] + orbital.velocity[1]) % area_size[1]]
