import logging

BLACK = 255
WHITE = 0

class Image_graph(object):


    def __init__(self, matrix):
        self.matrix = matrix.reshape(28, 28)
        self.width = 28
        self.height = 28
        self.connected_components = None
        self.black_points = None


    def get_black_points(self):
        if (self.black_points == None):
            self.black_points = []
            for x in range(self.width):
                for y in range(self.height):
                    if (self.matrix[x][y] == WHITE):
                        self.black_points += [(x, y)]
#        print("black point count:", len(self.black_points))
        return self.black_points


    def search_connected_components(self):
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.get_black_points()
#        if (self.connected_components == None):
        self.connected_components = []

        black_points = set(self.black_points)

#            steps = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while (len(black_points) != 0):
            using = [black_points.pop()]
            visited = [using[0]]

            my_using = using
            i = 0
            while (len(using) != 0):
                new_using = []

                for point in using:
                    x = point[0]
                    y = point[1]
                    for step in steps:
                        next_point = (x + step[0], y + step[1])
                        if next_point in black_points:
                            visited += [next_point]
                            black_points.remove(next_point)
                            new_using += [next_point]
                            my_using += [next_point]


                using = new_using
            self.connected_components += [visited]

        return self.connected_components

