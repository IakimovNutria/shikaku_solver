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
