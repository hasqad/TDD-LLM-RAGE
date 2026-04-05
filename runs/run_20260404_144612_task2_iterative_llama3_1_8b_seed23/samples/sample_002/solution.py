def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    while matrix and matrix[0]:
        # Traverse from left to right
        for i in range(len(matrix[0])):
            result.append(matrix[0][i])
        matrix[0] = matrix[0][1:]
        
        # Traverse from top to bottom
        for i in range(1, len(matrix)):
            result.append(matrix[i][len(matrix[0]) - 1])
        matrix.pop()
        
        # Traverse from right to left
        if matrix and matrix[0]:
            for i in range(len(matrix[0]) - 2, -1, -1):
                result.append(matrix[len(matrix) - 1][i])
            matrix[len(matrix) - 1] = matrix[len(matrix) - 1][:-1]
        
        # Traverse from bottom to top
        if matrix and matrix[0]:
            for i in range(len(matrix) - 2, 0, -1):
                result.append(matrix[i][0])
            matrix.pop(0)
    
    return result