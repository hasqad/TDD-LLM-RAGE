def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse from left to right on top row
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        if top > bottom:
            break
        # Traverse from top to bottom on right column
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if left > right:
            break
        # Traverse from right to left on bottom row
        for i in range(right, left - 1, -1):
            result.append(matrix[bottom][i])
        bottom -= 1
        if top > bottom:
            break
        # Traverse from bottom to top on left column
        for i in range(bottom, top - 1, -1):
            result.append(matrix[i][left])
        left += 1
    
    return result