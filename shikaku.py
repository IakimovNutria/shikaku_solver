import math
import copy
import argparse
import random

min_random_puzzle_len = 1
max_random_puzzle_len = 6

parser = argparse.ArgumentParser(description='Shikaku helper')
parser.add_argument('-s', '--solve_puzzle', type=str, default='puzzle.txt',
                    help='Solve puzzle from file', metavar='file_with_puzzle')
parser.add_argument('-g', '--out_the_puzzle',
                    help='Out the puzzle with number_of_solutions '
                         'solutions to out_file_solution',
                    type=str, nargs=2, metavar=('number_of_solutions',
                                                'out_file_solution'))

args = parser.parse_args()


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


def get_puzzle_from_file(path):
    result = []
    f = open(path, 'r')
    for line in f:
        if '*' in line:
            result.append([])
            element = ''
            for letter in line:
                if (letter == ' ' or letter == '\n') and element != '':
                    result[-1].append(int(element))
                    element = ''
                else:
                    if letter == '*':
                        result[-1].append('*')
                    elif letter != ' ' and letter != '\n':
                        element += letter
            if element != '':
                result[-1].append(int(element))
    return result


all_solutions = []


def get_rectangles_solution(local_solution, local_cells, local_puzzle):
    if len(local_cells) == 0:
        return local_solution

    cell = local_cells.pop()
    rectangles = get_clear_rectangles(cell, local_puzzle)

    if len(rectangles) == 1:
        local_solution.append(rectangles[0])
        return get_rectangles_solution(copy.deepcopy(local_solution),
                                       copy.deepcopy(local_cells),
                                       get_changed_puzzle(local_puzzle,
                                                          rectangles[0]))

    if len(rectangles) != 0:
        for rectangle in rectangles:
            perhaps_local_solution = copy.deepcopy(local_solution)
            perhaps_local_solution.append(rectangle)
            perhaps_solution = get_rectangles_solution(
                copy.deepcopy(perhaps_local_solution),
                copy.deepcopy(local_cells),
                get_changed_puzzle(local_puzzle, rectangle))
            if perhaps_solution != -1:
                all_solutions.append(perhaps_solution)

    return -1


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


def get_changed_puzzle(old_puzzle, rectangle):
    new_puzzle = copy.deepcopy(old_puzzle)
    left_top = rectangle.left_top
    right_bottom = rectangle.right_bottom
    for x in range(left_top.x, right_bottom.x + 1):
        for y in range(left_top.y, right_bottom.y + 1):
            new_puzzle[x][y] = '+'
    return new_puzzle


def get_cells(field):
    coordinates = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != '*':
                coordinates.append(Cell(Point(i, j), field[i][j]))
    return coordinates


def get_divisors(number):
    result = []
    for x in range(1, int(math.ceil(math.sqrt(number))) + 1):
        if number % x == 0:
            result.append(x)
    return result


def get_field_solution(rectangles_solution, puzzle_size):
    field = []
    for i in range(puzzle_size):
        field.append([])
        for j in range(puzzle_size):
            field[-1].append(-1)
    for i in range(len(rectangles_solution)):
        for x in range(rectangles_solution[i].left_top.x,
                       rectangles_solution[i].right_bottom.x + 1):
            for y in range(rectangles_solution[i].left_top.y,
                           rectangles_solution[i].right_bottom.y + 1):
                if field[x][y] == -1:
                    field[x][y] = i if i < 10 else chr(ord('A') + (i - 10))
                else:
                    return -1
    for x in range(puzzle_size):
        for y in range(puzzle_size):
            if field[x][y] == -1:
                return -1
    for i in range(len(field)):
        field[i] = tuple(field[i])
    return tuple(field)


def get_all_answers(puzzle_size):
    result = set()
    for i in all_solutions:
        result.add(get_field_solution(i, puzzle_size))
    return result


def get_puzzle(solutions_count):
    if solutions_count == 1:
        return get_random_puzzle_from_field_puzzle(
            get_random_field_puzzle([],
                                    random.randint(min_random_puzzle_len,
                                                   max_random_puzzle_len)))
    if solutions_count == 2:
        solution_variant = random.randint(1, 2)
        if solution_variant == 1:
            return get_first_variant_two_solutions_puzzle()
        if solution_variant == 2:
            return get_random_puzzle_from_field_puzzle(
                get_second_variant_two_solutions_puzzle())
    if solutions_count == 3:
        solution_variant = random.randint(1, 2)
        if solution_variant == 1:
            return get_random_puzzle_from_field_puzzle(
                get_first_variant_three_solutions_puzzle())
        if solution_variant == 2:
            return get_random_puzzle_from_field_puzzle(
                get_second_variant_three_solutions_puzzle())


def get_first_variant_two_solutions_puzzle():
    answer = ''
    puzzle_len = random.randint(3, max_random_puzzle_len)
    puzzle_len += -1 if puzzle_len % 2 == 0 else 0
    for i in range(puzzle_len):
        answer_line = ''
        for j in range(puzzle_len):
            answer_line += (str(puzzle_len) + ' ') if i == j else '* '
        answer += answer_line + '\n'
    return answer


def get_second_variant_two_solutions_puzzle():
    puzzle_len = random.randint(max(2, min_random_puzzle_len),
                                max_random_puzzle_len)
    left = random.randint(0, puzzle_len - 2)
    top = random.randint(0, puzzle_len - 2)
    rectangle = Rectangle(Point(left, top), Point(left + 1, top + 1))
    return get_random_field_puzzle([rectangle], puzzle_len)


def get_first_variant_three_solutions_puzzle():
    puzzle_len = random.randint(max(3, min_random_puzzle_len),
                                max_random_puzzle_len)
    left = random.randint(0, puzzle_len - 2)
    top = random.randint(0, puzzle_len - 3)
    rectangle = Rectangle(Point(left, top), Point(left + 1, top + 2))
    return get_random_field_puzzle([rectangle], puzzle_len)


def get_second_variant_three_solutions_puzzle():
    puzzle_len = random.randint(max(3, min_random_puzzle_len),
                                max_random_puzzle_len)
    left = random.randint(0, puzzle_len - 3)
    top = random.randint(0, puzzle_len - 2)
    rectangle = Rectangle(Point(left, top), Point(left + 2, top + 1))
    return get_random_field_puzzle([rectangle], puzzle_len)


def get_random_field_puzzle(rectangles, puzzle_len):
    field = []
    for i in range(puzzle_len):
        field.append([])
        for j in range(puzzle_len):
            field[-1].append('*')
    used_symb = 0
    for i in range(len(rectangles)):
        for x in range(rectangles[i].left_top.x,
                       rectangles[i].right_bottom.x + 1):
            for y in range(rectangles[i].left_top.y,
                           rectangles[i].right_bottom.y + 1):
                field[x][y] = chr(ord('a') + i)
                used_symb = i
    while there_is_empty_spaces(field):
        z = False
        left = 0
        top = 0
        while field[left][top] != '*':
            left += 1
            if left == puzzle_len:
                left = 0
                top += 1
        right = random.randint(left, puzzle_len - 1)
        bottom = random.randint(top, puzzle_len - 1)
        local_right = right
        field_part = get_field_part(field, Point(left, top),
                                    Point(local_right, bottom))
        while there_is_not_empty_spaces(field_part):
            local_right -= 1
            if local_right == left:
                local_right = right
                bottom -= 1
            field_part = get_field_part(field, Point(left, top),
                                        Point(local_right, bottom))

        for x in range(left, local_right + 1):
            for y in range(top, bottom + 1):
                field[x][y] = chr(ord('A') + used_symb)
                z = True
        if z:
            used_symb += 1
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 'a':
                if i % 2 != j % 2:
                    field[i][j] = '*'
                else:
                    field[i][j] = '2'
    return field


def get_field_part(field, left_top, right_bottom):
    field_part = []
    for x in range(left_top.x, right_bottom.x + 1):
        for y in range(left_top.y, right_bottom.y + 1):
            field_part.append(field[x][y])
    return field_part


def there_is_not_empty_spaces(field):
    for i in range(len(field)):
        if field[i] != '*':
            return True
    return False


def there_is_empty_spaces(field):
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == '*':
                return True
    return False


def get_random_puzzle_from_field_puzzle(field_puzzle):
    a = {}
    cells = {}
    for i in range(len(field_puzzle)):
        for j in range(len(field_puzzle[i])):
            if field_puzzle[i][j] != '*' and \
                    not ('1' <= str(field_puzzle[i][j]) <= '9'):
                if field_puzzle[i][j] in a:
                    a[field_puzzle[i][j]].append((i, j))
                else:
                    a[field_puzzle[i][j]] = [(i, j)]
    z = {}
    for key in a:
        points = a[key]
        random_point = points[random.randint(0, len(points) - 1)]
        cells[random_point] = key
        z[key] = 0
    for i in range(len(field_puzzle)):
        for j in range(len(field_puzzle[i])):
            if field_puzzle[i][j] != '*' and \
                    not ('1' <= str(field_puzzle[i][j]) <= '9'):
                z[field_puzzle[i][j]] += 1
    result = ''
    for i in range(len(field_puzzle)):
        for j in range(len(field_puzzle[i])):
            if '1' <= str(field_puzzle[i][j]) <= '9':
                result += str(field_puzzle[i][j]) + ' '
            else:
                result += '* ' if (i, j) not in cells \
                    else f'{z[cells[(i, j)]]} '
        result += '\n'
    return result


def solve_puzzle(puzzle):
    numbers_coordinates = get_cells(puzzle)
    all_solutions.clear()
    get_rectangles_solution(copy.deepcopy([]),
                            copy.deepcopy(numbers_coordinates),
                            copy.deepcopy(puzzle))
    return get_all_answers(len(puzzle))


if __name__ == '__main__':
    if args.out_the_puzzle is not None:
        arguments = args.out_the_puzzle
        try:
            count_of_solutions = int(arguments[0])
            out_file_name = arguments[1]
        except ValueError:
            raise Exception('Invalid arguments')
        if count_of_solutions > 3 or count_of_solutions < 1:
            raise Exception('Invalid arguments')
        if '.txt' not in out_file_name:
            out_file_name += '.txt'

        all_answers = []
        get_except = False
        while len(all_answers) != count_of_solutions or get_except:
            try:
                f = open(out_file_name, 'w')
                puzzle = get_puzzle(count_of_solutions)
                f.write(puzzle)
                f.close()
                all_answers = solve_puzzle(get_puzzle_from_file(
                    out_file_name))
                get_except = False
            except Exception:
                get_except = True
    else:
        puzzle = get_puzzle_from_file(args.solve_puzzle)
        all_answers = solve_puzzle(puzzle)
        if len(all_answers) == 0:
            print("There's no solution")
        else:
            for i in all_answers:
                for j in i:
                    print(*j)
                break
