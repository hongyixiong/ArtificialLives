import random
import tkinter


class BoidsSimulation:
    def __init__(self, length, width, num_boids):
        self.num_boids = num_boids
        self.length = length
        self.width = width
        # todo: the following parameters can be changed.
        self.neighbour_radius = 10
        self.max_velocity = 10

    def boids(self):
        self.initialise_boids(self.num_boids)
        self.move_all_boids_to_new_positions()

    def initialise_boids(self, num_boids):
        """
        Initialise boids at random positions and velocity.
        :param num_boids: the number of boids to be created.
        """
        pass

    def move_all_boids_to_new_positions(self):
        """
        Moves all boids to new positions.
        :return:
        """
        pass

    def rule1(self):
        """
        This rule simulates flock cohesion.
        :return:
        """
        pass

    def rule2(self):
        """
        This rule simulates separation.
        :return:
        """
        pass

    def rule3(self):
        """
        This rule simulates alignment.
        :return:
        """
        pass

    def rule4(self):
        """
        This rule simulates wind.
        :return:
        """
        pass

    def rule5(self):
        """
        This rule simulates perching.
        :return:
        """
        pass


class Boid:
    def __init__(self):
        pos_x = random.random()
        pos_y = random.random()
        vel_x = random.random()
        vel_y = random.random()

        self.position = (0, 0)
        self.velocity = (0, 0)


def main():
    num_boids = 20
    length = 100
    width = 100
    boids_simulation = BoidsSimulation(length, width, num_boids)
    boids_simulation.boids()


main()
