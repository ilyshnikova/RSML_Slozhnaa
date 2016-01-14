import logging

from component import Component

BLACK = 255
WHITE = 0

class ImageGraph(object):
    def __init__(self, matrix):
        self.matrix = matrix.reshape(28, 28)
        self.width = 28
        self.height = 28

        self.black_points = None
        self.black_points = self.get_black_points()

        self.connected_components = None
        self.connected_components = self.get_connected_components()

    def get_black_points(self):
        if self.black_points is None:
            self.black_points = []

            for x in range(self.height):
                for y in range(self.width):
                    if self.matrix[x][y] == BLACK:
                        self.black_points.append((x, y))

        return self.black_points

    def get_connected_components(self):
        logging.basicConfig(format='%(asctime)s %(message)s')

        self.connected_components = []
        black_points = set(self.black_points)

        steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while len(black_points) != 0:
            queue = [black_points.pop()]
            used_points = [queue[0]]

            while len(queue) != 0:
                new_queue = []

                for x, y in queue:
                    for dx, dy in steps:
                        next_point = (x + dx, y + dy)
                        if next_point in black_points:
                            used_points.append(next_point)
                            new_queue.append(next_point)
                            black_points.remove(next_point)

                queue = new_queue

            self.connected_components.append(Component(used_points))

        return self.connected_components
