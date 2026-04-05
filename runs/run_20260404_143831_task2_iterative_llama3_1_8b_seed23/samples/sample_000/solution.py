def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix and matrix[0]:
        result += matrix.pop(0)
        matrix = (list(zip(*matrix)))[::-1]
    return result