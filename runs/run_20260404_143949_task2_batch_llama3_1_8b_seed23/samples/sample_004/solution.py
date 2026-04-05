def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix and matrix[0]:
        result += matrix.pop(0)
        for row in matrix:
            if row:
                result.append(row.pop())
        if matrix and matrix[0]:
            result += matrix.pop()[::-1]
        if matrix:
            for row in matrix[::-1]:
                if row:
                    result.append(row.pop(0))
    return result