def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix:
        # Add the first row to the result and remove it from the matrix
        result.extend(matrix.pop(0))
        
        # If the matrix is not empty, add the last column to the result and remove it
        if matrix:
            for row in matrix:
                result.append(row.pop())
        
        # If the matrix is not empty, add the last row to the result in reverse order and remove it
        if matrix:
            result.extend(matrix.pop()[::-1])
        
        # If the matrix is not empty, add the first column to the result in reverse order and remove it
        if matrix:
            for i in range(len(matrix) - 1, -1, -1):
                result.append(matrix[i].pop(0))
    return result