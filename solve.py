import numpy as np
from PIL import Image
import pandas as pd


class Point:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self


def IsBadPoint(point):
    return Point((-1, -1)) == point


def CountSquareDist(point, count):
    return (point.x ** 2 + point.y ** 2) * (count ** 2)


beams = [(1, 0), (2, 1), (3, 2), (1, 1), (2, 3), (1, 2), (0, 1), (-1, 2), (-2, 3), (-1, 1), (-3, 2), (-2, 1), (3, 4),
         (-3, 4), (4, 3), (-4, 3), (1, 3)]


class Field:

    def __init__(self, array):
        self.array = array
        self.maxX = array.shape[0] - 1
        self.minX = 0
        self.maxY = array.shape[1] - 1
        self.minY = 0
        self.maxIterations = 15
        self.allBeams = [(beams[i], (-beams[i][0], -beams[i][1])) for i in range(len(beams))]

    def IsAvailable(self, point):
        if not (self.minX <= point.x <= self.maxX and self.minY <= point.y <= self.maxY):
            return False
        return self.array[point.x][point.y] == 0

    def GoDeep(self, point, delta):
        point += Point(delta)
        if self.IsAvailable(point):
            return point
        else:
            return Point((-1, -1))

    def IsIntersection(self, point):
        linesCount = 0
        for beamPair in self.allBeams:
            counter = [0, 0]
            for i in range(2):
                tempPoint = Point((0, 0))
                tempPoint += point
                while not IsBadPoint(tempPoint) and counter[i] <= 20:
                    tempPoint = self.GoDeep(tempPoint, beamPair[i])
                    counter[i] += 1
            if CountSquareDist(Point(beamPair[0]), counter[0]) >= 400 and CountSquareDist(Point(beamPair[1]),
                                                                                          counter[1]) >= 400:
                linesCount += 1
            if linesCount >= 2:
                return True
        return False


class Solve:
    def __init__(self, image):
        self.field = Field(np.array((Image.open(image)).convert('1')))
        self.shape = self.field.array.shape
        self.pointArea = np.zeros(self.shape, dtype=np.int8)
        self.interPoints = []
        self.marked = []

    def FindIntesectionPoints(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                if self.field.array[i][j] == 1:
                    continue
                elif self.field.IsIntersection(Point((i, j))):
                    self.pointArea[i][j] = 1
                    self.interPoints.append(Point((i, j)))

    def MarkNeighbours(self, point):
        x = point.x
        y = point.y
        if not self.field.IsAvailable(point):
            return
        if self.pointArea[x][y] == 0 or self.marked[x][y] == 1:
            return
        self.marked[x][y] = 1
        for d1 in range(-1, 2, 1):
            for d2 in range(-1, 2, 1):
                if 0 == d2 and d1 == 0:
                    continue
                self.MarkNeighbours(Point((x + d1, y + d2)))

    def ConnectIntersetionPoints(self):
        countIntesections = 0
        self.marked = np.zeros(self.shape, dtype=np.int8)
        for point in self.interPoints:
            x = point.x
            y = point.y
            if self.marked[x][y] == 0:
                print(point.x, point.y)
                countIntesections += 1
                self.MarkNeighbours(point)
        return countIntesections

    def Process(self):
        self.FindIntesectionPoints()
        return self.ConnectIntersetionPoints()


a = Solve('img.png')
print(a.shape)
print(a.Process())
pd.DataFrame(1 * np.array((Image.open('img.png')).convert('1'))).to_csv('1.csv', sep='.')
