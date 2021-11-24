import copy
from math_work import get_divisors


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ' ' + str(self.y) + ')'

    def __repr__(self):
        return str(self)


class Rectangle:
    def __init__(self, left_top, right_bottom):
        self.left_top = left_top
        self.right_bottom = right_bottom

    def __str__(self):
        return '(' + str(self.left_top) + ' ' + str(self.right_bottom) + ')'

    def __repr__(self):
        return str(self)


class Cell:
    def __init__(self, point, value):
        self.point = point
        self.value = value


def get_clear_rectangles(cell, field):
    result = []
    number = cell.value
    point = cell.point
    not_coordinate_rectangles = []

    for divisor in get_divisors(number):
        not_coordinate_rectangles.append(Rectangle(
            Point(0, 0), Point(divisor - 1, number // divisor - 1)))
        not_coordinate_rectangles.append(Rectangle(
            Point(0, 0), Point(number // divisor - 1, divisor - 1)))

    for rectangle in not_coordinate_rectangles:
        while rectangle.right_bottom.x < len(field):
            rect = copy.deepcopy(rectangle)
            while rect.right_bottom.y < len(field[0]):
                is_rectangle_clear = False

                if (rect.left_top.x <= point.x <= rect.right_bottom.x) and \
                        (rect.left_top.y <= point.y <= rect.right_bottom.y):
                    is_rectangle_clear = True
                    for x in range(rect.left_top.x, rect.right_bottom.x + 1):
                        for y in range(rect.left_top.y,
                                       rect.right_bottom.y + 1):
                            if (x != point.x or y != point.y) and \
                                    field[x][y] != '*':
                                is_rectangle_clear = False

                if is_rectangle_clear:
                    result.append(rect)
                rect = copy.deepcopy(rect)

                rect.right_bottom.y += 1
                rect.left_top.y += 1

            rectangle.right_bottom.x += 1
            rectangle.left_top.x += 1
    return result
