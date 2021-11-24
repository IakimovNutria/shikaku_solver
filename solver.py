import copy
from field import get_cells, get_changed_puzzle, get_field_solution
from rectangles import get_clear_rectangles

all_solutions = []


def solve_puzzle(puzzle):
    numbers_coordinates = get_cells(puzzle)
    all_solutions.clear()
    get_rectangles_solution(copy.deepcopy([]),
                            copy.deepcopy(numbers_coordinates),
                            copy.deepcopy(puzzle))
    return get_all_answers(len(puzzle))


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


def get_all_answers(puzzle_size):
    result = set()
    for i in all_solutions:
        result.add(get_field_solution(i, puzzle_size))
    return result
