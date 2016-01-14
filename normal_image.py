from __future__ import print_function
import numpy as np
import logging

import graph

BLACK = 255
WHITE = 0

class NormalImage(object):
    logging.basicConfig(format='%(asctime)s %(message)s')

    def __init__(self, image, ind=-1, need_bin=True):
        self.image = image.reshape(28, 28)
        self.i = ind

        self.width = 28
        self.height = 28
        self.image_graph = None
        self.need_bin = need_bin

        if self.i != -1:
            self.file = open("bad_samples.txt", "a")

    def binarize(self):
        # color_index = 0.7 * np.percentile(self.image, 55) + 0.3 * np.mean(self.image)
        color_index = np.percentile(self.image, 55)

        for x in range(self.height):
            for y in range(self.width):
                if self.image[x][y] > color_index:
                    self.image[x][y] = BLACK
                else:
                    self.image[x][y] = WHITE

        for x in (1, 27):
            for y in range(1, 27):
                self.image[x][y] = WHITE
                self.image[x][y] = WHITE

        self.image_graph = graph.ImageGraph(self.image)

    def noise_removal(self):
        self.image_graph = graph.ImageGraph(self.image)
        components = self.image_graph.connected_components

        if len(components) <= 1:
            return

        sizes = [float(max(i.width, i.height)) for i in components]
        sizes.sort(reverse=True)

        min_letter_size = sizes[-1]

        for i in range(1, len(sizes)):
            if sizes[i - 1] / sizes[i] > 1.5:
                min_letter_size = sizes[i - 1]
                break

        for c in components:
            if max(c.width, c.height) < min_letter_size:
                c.delete(self.image)

        self.image_graph = graph.ImageGraph(self.image)
        components = self.image_graph.get_connected_components()

        if len(components) <= 1:
            return

        sizes = [float(i.num_points) for i in components]
        sizes.sort(reverse=True)

        min_letter_size = sizes[-1]

        for i in range(1, len(sizes)):
            if sizes[i - 1] / sizes[i] > 2:
                min_letter_size = sizes[i - 1]
                break

        for c in components:
            if c.num_points < min_letter_size:
                c.delete(self.image)

        self.image_graph = graph.ImageGraph(self.image)
        components = self.image_graph.get_connected_components()

        if len(components) != 1:
            if self.i != -1:
                print(self.i, file=self.file)

    def __str__(self):
        st = ""
        st += "--------------------------------------------------------\n"
        for x in range(self.height):
            for y in range(self.width):
                if self.image[x][y] == BLACK:
                    st += "X "
                else:
                    st += ". "

            st += '\n'
        st += "--------------------------------------------------------\n"

        return st

    def get_np_array(self):
        return self.image.reshape(28*28)

    def get_img(self):
        return self.image

    def smooth(self):
        if self.need_bin:
            self.binarize()

        acount = 1

        while acount > 0:
            acount = 0
            self.noise_removal()
            self.image_graph = graph.ImageGraph(self.image)

            black_points = self.image_graph.get_black_points()
            for x, y in black_points:
                steps = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
                if self.image[x][y] == BLACK:
                    count = 0
                    for dx, dy in steps:
                        next_point = (x + dx, y + dy)
                        if 0 <= next_point[0] < 28 and \
                                0 <= next_point[1] < 28 and self.image[next_point[0]][next_point[1]] == WHITE:
                                    count += 1

                    if count > 5:
                        self.image[x][y] = WHITE
                        acount += 1

                    if 0 < x < 27 and 0 < y < 27 and (
                        self.image[x + 1][y] == WHITE and self.image[x - 1][y] == WHITE or
                            self.image[x][y + 1] == WHITE and self.image[x][y - 1] == WHITE):
                                self.image[x][y] = WHITE
                                acount += 1

            self.noise_removal()

    def __del__(self):
        if self.i != -1:
            self.file.close()
