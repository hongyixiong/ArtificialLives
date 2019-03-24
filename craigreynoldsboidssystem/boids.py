import random
import tkinter


class BoidsSimulation:
    def __init__(self, field_length, field_width, num_boids):
        self.num_boids = num_boids
        self.field_length = field_length
        self.field_width = field_width
        self.boids_list = []

        # todo: the following parameters can be changed.
        self.neighbour_radius = 10
        self.max_velocity = 10

    def boids(self):
        self.initialise_boids(self.num_boids)
        self.move_all_boids_to_new_positions()

    def initialise_boids(self):
        """
        Initialise boids at random positions and velocity.
        """
        for i in range(0, self.num_boids):
            new_boid = Boid()
            new_boid.position = (random.uniform(0, self.field_width), random.uniform(0, self.field_length))
            new_boid.velocity = (random.uniform(-20, 20), random.uniform(-20, 20))
            self.boid_list.append(new_boid)


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

    def rule3(self, boid):
        """
        This rule simulates alignment.
        :return:
        """

        for other_boid in self.boids_list:
            if other_boid != boid:
                boid.velocity[0] += other_boid.velocity[0]



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
        self.position = (0, 0)
        self.velocity = (0, 0)


def main():
    num_boids = 20
    length = 100
    width = 100
    boids_simulation = BoidsSimulation(length, width, num_boids)
    boids_simulation.boids()


main()
