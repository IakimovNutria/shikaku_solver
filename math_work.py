import math


def get_divisors(number):
    result = []
    for x in range(1, int(math.ceil(math.sqrt(number))) + 1):
        if number % x == 0:
            result.append(x)
    return result
