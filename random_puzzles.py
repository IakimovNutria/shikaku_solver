from field import there_is_empty_spaces, there_is_not_empty_spaces
import random
from rectangles import Point, Rectangle
from field import get_field_part

min_random_puzzle_len = 1
max_random_puzzle_len = 6


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
