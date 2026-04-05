def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix and matrix[0]:
        # Append first row to result
        result += matrix.pop(0)
        # Rotate the remaining matrix clockwise
        matrix = (list(zip(*matrix)))[::-1]
    return result