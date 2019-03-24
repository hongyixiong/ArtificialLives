import random
import tkinter


class Boid:
    def __init__(self):
        pos_x = random.random()
        pos_y = random.random()
        vel_x = random.random()
        vel_y = random.random()

        self.position = (0, 0)
        self.velocity = (0, 0)


def boids(n):
    initialise_boids(n)
    move_all_boids_to_new_positions()


def initialise_boids(n):
    """
    Initialise boids at random positions and velocity.
    :param n: the number of boids to be created.
    """
    pass


def move_all_boids_to_new_positions():
    """
    Moves all boids to new positions.
    :return:
    """
    pass


def rule1():
    """
    This rule simulates flock cohesion.
    :return:
    """
    pass


def rule2():
    """
    This rule simulates separation.
    :return:
    """
    pass


def rule3():
    """
    This rule simulates alignment.
    :return:
    """
    pass


def rule4():
    """
    This rule simulates wind.
    :return:
    """
    pass


def rule5():
    """
    This rule simulates perching.
    :return:
    """
    pass


def main():
    num_of_boids = 20
    boids(num_of_boids)


main()
