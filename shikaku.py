import argparse
from random_puzzles import get_puzzle
from solver import solve_puzzle
from file_work import get_puzzle_from_file


parser = argparse.ArgumentParser(description='Shikaku helper')
parser.add_argument('-s', '--solve_puzzle', type=str, default='puzzle.txt',
                    help='Solve puzzle from file', metavar='file_with_puzzle')
parser.add_argument('-g', '--out_the_puzzle',
                    help='Out the puzzle with number_of_solutions '
                         'solutions to out_file_solution',
                    type=str, nargs=2, metavar=('number_of_solutions',
                                                'out_file_solution'))

args = parser.parse_args()


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
