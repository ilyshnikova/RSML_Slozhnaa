BLACK = 255
WHITE = 0

class Component(object):
    def __init__(self, points):
        self.points = points
        (self.width, self.height) = self.size()
        self.points_count = len(points)
#        print("points count", self.points_count)

    def size(self):
        x = [point[0] for point in self.points]
        y = [point[1] for point in self.points]
        return (max(x) - min(x) + 1, max(y) - min(y) + 1)

    def delete(self, im):
        for i in self.points:
            im[i[0]][i[1]] = BLACK



