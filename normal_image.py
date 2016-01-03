#import Image
import graph
import os
import sys
import numpy as np
import component
import logging

BLACK = 255
WHITE = 0

class Normal_image(object):

    logging.basicConfig(format='%(asctime)s %(message)s')

    def __init__(self, image, contrast=10, in_line=False):
        self.image = image.reshape(28, 28)
#        print(self.image)


        self.width = 28
        self.height = 28

        color_index = np.percentile(image, 55)

        for x in range(0, self.width):
            for y in range(0, self.height):
                if (self.image[x][y] > color_index):
                    self.image[x][y] = WHITE
                else:
                    self.image[x][y] = BLACK

        for i in (0, 27):
            for j in range(1, 28):
                self.image[i][j] = BLACK
                self.image[j][i] = BLACK
        self.image_graph = graph.Image_graph(self.image)



    def noise_removal(self):
#        print("\n----------before noise_removal-----------")

#        self.print_im()
        self.image_graph = graph.Image_graph(self.image)

        self.image_graph.search_connected_components()

        components = []

#        print("")
#        self.pr(im)
        for c in self.image_graph.connected_components:
            cm = component.Component(c)
            components.append(cm)
#            cm.delete(im)
#            self.pr(im)

        if len(components) <= 1:
            return



        sizes = []
        for i in components:
                sizes += [-max(i.width, i.height)]

        sizes.sort()

        min_letter_size = sizes[len(sizes) - 1];

        for i in range(1, len(sizes)):
            if (float(sizes[i - 1]) / float(sizes[i]) > 1.5):
                min_letter_size = sizes[i - 1];
                break;



        min_letter_size = -min_letter_size
#
#        print("min_letter_size", min_letter_size)

#        self.print_im()
        for c in components:
#            print("delete")
            if (max(c.width, c.height) < min_letter_size):
                c.delete(self.image)
#                print("THERE")
#                for point in c.points:
#
#                    print(point)
#                    self.image[point[0]][point[1]] = BLACK
#                self.print_im()
#            self.print_im()

#        print("\n----------after noise_removal-----------")
#        self.print_im()


        self.image_graph = graph.Image_graph(self.image)
        self.image_graph.search_connected_components()

        components = []

#        print("")
#        self.pr(im)
        for c in self.image_graph.connected_components:
            cm = component.Component(c)
            components.append(cm)
#            cm.delete(im)
#            self.pr(im)


#        print("c count", len(components))

        if len(components) <= 1:
            return



        sizes = []
        for i in components:
                sizes += [-i.points_count]

        sizes.sort()

        min_letter_size = sizes[len(sizes) - 1];

        for i in range(1, len(sizes)):
            if (float(sizes[i - 1]) / float(sizes[i]) > 2):
                min_letter_size = sizes[i - 1];
                break;



        min_letter_size = -min_letter_size
#
#        print("min_letter_size", min_letter_size)

#        self.print_im()
        for c in components:
#            print("delete")
            if (c.points_count < min_letter_size):
#                print("THERE")
                for point in c.points:
#                    print(point)
                    self.image[point[0]][point[1]] = BLACK



    def print_im(self):
        self.pr(self.image)

    def pr(self, im):
        print("----------------------------")
        for x in range(0, 28):
            for y in range(0,28):
                if (im[x][y] == BLACK):
                    print("X ", end="")
                else:
                    print(". ", end="")


            print("")
        print("----------------------------")



    def get_np_array(self):
        self.print_im()
        return self.image.reshape(28*28)


    def smooth(self):
        acount = 1

        while acount > 0:
            acount = 0
            self.noise_removal()
            self.image_graph = graph.Image_graph(self.image)

            black_points = self.image_graph.get_black_points()
            for p in black_points:
                steps = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
                if (self.image[p[0]][p[1]] == WHITE):

                    count = 0
                    for step in steps:
                        next_point = (p[0] + step[0], p[1] + step[1])
                        if (0 <= next_point[0] < 28 and 0 <= next_point[1] < 28 and self.image[next_point[0]][next_point[1]] == BLACK):
                            count += 1

                    if (count > 5):
#                        print("smooth smooth smooth !!!! ", p)
                        self.image[p[0]][p[1]] = BLACK
                        acount += 1

                    if (
                        0 < p[0] < 27
                        and 0 < p[1] < 27
                        and (
                            (
                                self.image[p[0] + 1][p[1]] == BLACK
                                and self.image[p[0] - 1][p[1]] == BLACK
                            )
                            or ( # так почему то лучше
                                self.image[p[0]][p[1] + 1] == BLACK
                                and self.image[p[0]][p[1] - 1] == BLACK
                            )
                        )
                    ):
#                        print("smooth smooth smooth paralel !!!! ", p)
                        self.image[p[0]][p[1]] = BLACK
                        acount += 1
            self.noise_removal()


#            print("count ", acount)

