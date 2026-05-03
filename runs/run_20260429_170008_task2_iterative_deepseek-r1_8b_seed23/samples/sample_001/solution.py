def spiral_order(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    
    top, bottom, left, right = 0, len(matrix)-1, 0, len(matrix[0])-1
    res = []
    
    while left <= right and top <= bottom:
        # Traverse top row
        for j in range(left, right+1):
            res.append(matrix[top][j])
        top += 1
        
        # Traverse right column
        for i in range(top, bottom+1):
            res.append(matrix[i][right])
        right -= 1
        
        # Traverse bottom row if there are rows left and columns left
        if top <= bottom and left <= right:
            for j in range(right, left-1, -1):
                res.append(matrix[bottom][j])
            bottom -= 1
            
        # Traverse left column if there are rows left and columns left
        if top <= bottom and left <= right:
            for i in range(bottom, top-1, -1):
                res.append(matrix[i][left])
            left += 1
            
    return res