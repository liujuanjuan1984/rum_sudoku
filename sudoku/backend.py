import random

matrix = [([0] * 9) for i in range(9)]


def print_matrix(matrix):
    note = "—" * 9 + "\n"
    for row in matrix:
        note += "| " + " ".join([str(col) for col in row]) + " |\n"
    note += "—" * 9
    print(note)
    return note


def check(matrix, i, j, number):
    if number in matrix[i]:
        return False
    if number in [row[j] for row in matrix]:
        return False
    group_i, group_j = int(i / 3), int(j / 3)
    if number in [
        matrix[i][j]
        for i in range(group_i * 3, (group_i + 1) * 3)
        for j in range(group_j * 3, (group_j + 1) * 3)
    ]:
        return False
    return True


def build_game(matrix, i, j, number):
    if i > 8 or j > 8:
        return matrix
    if check(matrix, i, j, number):
        _matrix = [[col for col in row] for row in matrix]
        _matrix[i][j] = number
        next_i, next_j = (i + 1, 0) if j == 8 else (i, j + 1)
        _list = list(range(1, 10))
        random.shuffle(_list)
        for _number in _list:
            __matrix = build_game(_matrix, next_i, next_j, _number)
            if __matrix and sum([sum(row) for row in __matrix]) == (
                sum(range(1, 10)) * 9
            ):
                return __matrix
    return None


def give_me_a_game(blank_size=9):
    matrix_all = build_game(matrix, 0, 0, random.choice(range(1, 10)))
    set_ij = set()
    while len(list(set_ij)) < blank_size:
        set_ij.add(f"{random.choice(range(9))},{random.choice(range(9))}")
    matrix_blank = [[col for col in row] for row in matrix_all]
    blank_ij = []
    for ij in list(set_ij):
        i, j = int(ij.split(",")[0]), int(ij.split(",")[1])
        blank_ij.append((i, j))
        matrix_blank[i][j] = 0
    return matrix_all, matrix_blank, blank_ij
