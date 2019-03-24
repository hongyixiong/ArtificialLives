import random
import operator
import tkinter
import math

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
        for boid in self.boids_list:
            v1 = self.rule1(boid)
            v2 = self.rule2(boid)
            v3 = self.rule3(boid)

            new_velocity_0 = boid.velocity[0] + v1[0] + v2[0] + v3[0]
            new_velocity_1 = boid.velocity[0] + v1[1] + v2[0] + v3[0]
            boid.velocity = tuple(new_velocity_0, new_velocity_1)

            boid.position = tuple(map(operator.add, boid.position, boid.velocity))
        pass

    def rule1(self, b, boids_list):
        """
        This rule simulates flock cohesion.
        :param b: the position of a selected Boid
        :param boids_list: a list of positions of all Boids
        :return: a tuple of the movement for Boid b
        """
        x = 0
        y = 0
        for boid in boids_list:
            if boid != b:
                x += boid.position[0]
                y += boid.position[1]

        total_boids = len(boids_list)
        average_x = x / (total_boids - 1)
        average_y = y / (total_boids - 1)

        movement_x = (average_x - b.position[0]) / 100
        movement_y = (average_y - b.position[1]) / 100
        movement = (movement_x, movement_y)
        return movement

    def rule2(self, b, boids_list):
        """
        This rule simulates separation.
        :param b: the position of a selected Boid
        :param boids_list: a list of positions of all Boids
        :return: a tuple of movement for Boid b
        """
        x = 0
        y = 0
        for boid in boids_list:
            if boid != b:
                if self.euclidean_distance(boid, b) < 100:
                    x -= (boid.position[0] - b.position[0])
                    y -= (boid.position[1] - b.position[1])

        movement = (x, y)
        return movement

    def rule3(self, boid):
        """
        This rule simulates alignment.
        :return:
        """
        velocity = (0, 0)
        for other_boid in self.boids_list:
            if other_boid != boid:
                velocity = tuple(map(operator.add, velocity, other_boid.velocity))

        boids_num = self.num_boids - 1
        velocity = tuple(map(operator.truediv, velocity, (boids_num, boids_num)))
        new_velocity = tuple(map(operator.sub, velocity, boid.velocity))

        return tuple(map(operator.truediv, new_velocity, (8, 8)))

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

    def euclidean_distance(self, b1, b2):
        '''
        Calculate the euclidean distance between two Boids
        :param b1: the position of the first selected Boid
        :param b2: the position of the second selected Boid
        :return: the euclidean distance between b1 and b2
        '''
        return math.sqrt((b1.position[0] - b2.position[0])**2 + (b1.position[1] - b2.position[1])**2)


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
