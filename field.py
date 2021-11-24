from rectangles import Cell, Point
import copy


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


def get_field_part(field, left_top, right_bottom):
    field_part = []
    for x in range(left_top.x, right_bottom.x + 1):
        for y in range(left_top.y, right_bottom.y + 1):
            field_part.append(field[x][y])
    return field_part


def get_cells(field):
    coordinates = []
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] != '*':
                coordinates.append(Cell(Point(i, j), field[i][j]))
    return coordinates


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


def get_changed_puzzle(old_puzzle, rectangle):
    new_puzzle = copy.deepcopy(old_puzzle)
    left_top = rectangle.left_top
    right_bottom = rectangle.right_bottom
    for x in range(left_top.x, right_bottom.x + 1):
        for y in range(left_top.y, right_bottom.y + 1):
            new_puzzle[x][y] = '+'
    return new_puzzle
