import random
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def add(*vectors):
        x = 0
        y = 0
        z = 0
        for v in vectors:
            x += v.x
            y += v.y
            z += v.z
        return Vector(x, y, z)

    @staticmethod
    def multiply_constant(c, vector):
        return Vector(c * vector.x, c * vector.y, c * vector.z)

    @staticmethod
    def euclidean_distance(vector_1, vector_2):
        return math.sqrt(
            (vector_1.x - vector_2.x) ** 2 + (vector_1.y - vector_2.y) ** 2 + (vector_1.z - vector_2.z) ** 2)

    @staticmethod
    def norm_2(vector):
        """
        This returns the 2nd norm of the given vector, also known as the length of the vector.
        :param vector: a 3D vector
        :return: the 2nd norm of the vector.
        """
        return math.sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)

    @staticmethod
    def unit(vector):
        """
        Unit vector of v = v / ||v||, that is, the vector divided by its length.
        ||v|| denotes the second norm of v.
        :param vector: a vector
        :return: a unit vector in the direction of v.
        """
        return Vector.multiply_constant(1 / Vector.norm_2(vector), vector)

    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.z)


class Boid:
    def __init__(self):
        self.position = Vector(0, 0, 0)
        self.velocity = Vector(0, 0, 0)

    def __str__(self):
        return "({}{})".format(self.position, self.velocity)


class BoidsSimulation:
    def __init__(self, field_length, field_width, field_height, num_boids):
        self.field_length = field_length
        self.field_width = field_width
        self.field_height = field_height
        self.num_boids = num_boids
        self.boids_list = []

        # todo: the following parameters can be changed.
        self.neighbour_radius = 100
        self.max_velocity = 1
        self.max_acceleration = 0.1
        self.safe_distance = 20

        self.start_time = time.time()
        self.wind_start_time = self.start_time + 10
        self.wind_end_time = self.start_time + 20

        # the following are constant multipliers for rules
        self.c_1 = 10 / 1000  # cohesion
        self.c_2 = 10 / 1000  # separation
        self.c_3 = 50 / 1000  # alignment
        self.c_4 = 500 / 1000  # wind
        self.c_5 = 1  # perching

        # the following are for drawing on a graph
        self.fig = None
        self.ax = None
        self.surface = None

    def boids_simulation(self):
        self.initialise_boids()
        self.print_boids_list()
        self.build_graph()
        # tkinter.mainloop()
        # todo: max_iteration to be removed, because we want it to continue until user closes the window.
        max_iteration = 100
        iteration = 1
        # while iteration < max_iteration:
        while True:
            if not plt.fignum_exists(1):
                # if user closes the figure, then break out of loop to terminate program.
                break
            print("The current frame number is:", iteration)
            self.draw_boids()
            self.move_all_boids_to_new_positions()
            iteration += 1

    def initialise_boids(self):
        """
        Initialise boids at random positions and velocities.
        """
        for i in range(self.num_boids):
            boid = Boid()
            # pos_x = random.uniform(0, self.field_length)
            # pos_y = random.uniform(0, self.field_width)
            # pos_z = random.uniform(0, self.field_height)
            standart_deviation = 20
            pos_x = random.gauss(self.field_length / 2, standart_deviation)
            pos_y = random.gauss(self.field_width / 2, standart_deviation)
            pos_z = random.gauss(self.field_height / 2, standart_deviation)
            vel_x = random.uniform(-self.max_velocity, self.max_velocity)
            vel_y = random.uniform(-self.max_velocity, self.max_velocity)
            vel_z = random.uniform(-self.max_velocity, self.max_velocity)
            # vel_x = random.uniform(-self.max_velocity, 0)
            # vel_y = random.uniform(-self.max_velocity, 0)
            # vel_z = random.uniform(-self.max_velocity, 0)

            boid.position = Vector(pos_x, pos_y, pos_z)
            boid.velocity = Vector(vel_x, vel_y, vel_z)
            self.boids_list.append(boid)

    def move_all_boids_to_new_positions(self):
        """
        Moves all boids to new positions.
        Rule 1: cohesion
        Rule 2: separation
        Rule 3: alignment
        Rule 4: wind
        Rule 5: perching
        """
        temp_boids_list = []
        current_time = time.time()
        for boid in self.boids_list:
            v1 = Vector.multiply_constant(self.c_1, self.rule1(boid))
            v2 = Vector.multiply_constant(self.c_2, self.rule2(boid))
            v3 = Vector.multiply_constant(self.c_3, self.rule3(boid))
            if self.wind_start_time <= current_time <= self.wind_end_time:
                v4 = Vector.multiply_constant(self.c_4, self.rule4(boid))
            else:
                v4 = Vector(0, 0, 0)
            v5 = Vector.multiply_constant(self.c_5, self.rule5(boid))
            v6 = self.bound_position(boid)

            temp_boid = Boid()
            temp_boid.velocity = Vector.add(boid.velocity, v1, v2, v3, v4, v5, v6)
            # temp_boid.velocity = Vector.add(boid.velocity, v2, v5, v6)  # if only 1 boid.
            self.limit_velocity(temp_boid)

            temp_boid.position = Vector.add(boid.position, temp_boid.velocity)
            temp_boids_list.append(temp_boid)
            # self.print_boids_list()
        self.boids_list = temp_boids_list
        # self.print_boids_list()

    def limit_velocity(self, boid):
        """
        Limit the velocity of the boid. If the boid's velocity is larger than the maximum velocity allowed,
        then set the boid's velocity to the maximum velocity allowed.
        :param boid: a boid
        """
        boid_velocity = boid.velocity
        if Vector.norm_2(boid_velocity) > self.max_velocity:
            boid.velocity = Vector.multiply_constant(self.max_velocity, Vector.unit(boid_velocity))

    def bound_position(self, boid):
        force = 2
        delta_vel = Vector(0, 0, 0)

        boid_position = boid.position
        if boid_position.x < 0:
            delta_vel.x = force
        elif boid_position.x > self.field_length:
            delta_vel.x = - force
        if boid_position.y < 0:
            delta_vel.y = force
        elif boid_position.y > self.field_width:
            delta_vel.y = - force
        if boid_position.z < 0:
            delta_vel.z = force
        elif boid_position.z > self.field_height:
            delta_vel.z = - force
        return delta_vel

    def rule1(self, boid):
        """
        This rule simulates flock cohesion.
        :param boid: the position of a selected boid
        :return: a vector representing the displacement for the boid
        """
        delta_pos = Vector(0, 0, 0)
        for b in self.boids_list:
            if b != boid:
                delta_pos = Vector.add(delta_pos, b.position)

        # the following line calculates: delta_pos = delta_pos / (N-1)
        delta_pos = Vector.multiply_constant(1 / (self.num_boids - 1), delta_pos)
        # the following line returns delta_pos - boid.position
        return Vector.add(delta_pos, Vector.multiply_constant(-1, boid.position))

    def rule2(self, boid):
        """
        This rule simulates separation.
        :param boid: the position of a selected boid
        :return: a vector representing the displacement for the boid
        """
        delta_vel = Vector(0, 0, 0)
        for b in self.boids_list:
            if b != boid:
                if Vector.euclidean_distance(b.position, boid.position) < self.safe_distance:
                    # The formula is:
                    # delta_vel = delta_vel - (b.position - boid.position)
                    #           = delta_vel - b.position + boid.position
                    delta_vel = Vector.add(delta_vel, Vector.multiply_constant(-1, b.position), boid.position)
        return delta_vel

    def rule3(self, boid):
        """
        This rule simulates alignment.
        :param boid: the position of a selected boid
        :return: a vector representing the displacement for the boid
        """
        delta_vel = Vector(0, 0, 0)
        for b in self.boids_list:
            if b != boid:
                delta_vel = Vector.add(delta_vel, b.velocity)

        # The following line calculates: delta_vel = delta_vel / (N-1)
        delta_vel = Vector.multiply_constant(1 / (self.num_boids - 1), delta_vel)
        return delta_vel

    def rule4(self, boid):
        """
        This rule simulates wind.
        :param boid: the position of a selected boid
        :return: a unit vector representing direction of wind.
        """
        # todo: implement many more rules
        x = -1
        y = 0
        z = 0

        vec = Vector(x, y, z)
        # vec = Vector.unit(vec)
        return vec

    def rule5(self, boid):
        """
        This rule simulates perching.
        :param boid: the position of a selected boid
        :return: a vector representing the displacement for the boid
        """
        # todo: implement perching and more rules.
        return Vector(0, 0, 0)

    def build_graph(self):
        matplotlib.interactive(True)
        matplotlib.use('Qt5Agg')
        # plt.axis('equal')
        # plt.axis('scaled')
        # plt.figure(figsize=(10, 8))
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(1, 1, 1, projection='3d')
        self.ax.set_title("Craig Reynolds' Boids System")
        self.ax.set_xlabel("x-axis")
        self.ax.set_ylabel("y-axis")
        self.ax.set_zlabel("z-axis (height)")
        self.ax.set_xlim3d(0, self.field_length)
        self.ax.set_ylim3d(0, self.field_width)
        self.ax.set_zlim3d(0, self.field_height)

    def draw_boids(self):
        xs = []
        ys = []
        zs = []
        for boid in self.boids_list:
            boid_position = boid.position
            xs.append(boid_position.x)
            ys.append(boid_position.y)
            zs.append(boid_position.z)

        if self.surface is not None:
            self.surface.remove()  # clear graph

        self.surface = self.ax.scatter(xs, ys, zs, color='red')  # redraw boids on graph
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(0.00001)

    def print_boids_list(self):
        print("This is the start of boids_list")
        for boid in self.boids_list:
            print(boid)
        print("This is the end of boids_list")


def main():
    num_boids = 10
    length = 1000
    width = 500
    height = 100
    boids_simulation = BoidsSimulation(length, width, height, num_boids)
    boids_simulation.boids_simulation()


main()
