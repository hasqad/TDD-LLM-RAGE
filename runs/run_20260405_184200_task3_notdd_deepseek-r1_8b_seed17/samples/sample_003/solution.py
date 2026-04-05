from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    costs = [0] * n
    calories = [0] * n
    protein_list = [0] * n
    for i, (name, cost, nut) in enumerate(recipes):
        costs[i] = cost
        calories[i] = nut[0]
        protein_list[i] = nut[1]
    
    ancestors = [set() for _ in range(n)]
    for i in range(n):
        stack = [i]
        while stack:
            node = stack.pop()
            if node not in ancestors[i]:
                ancestors[i].add(node)
                for parent in graph[node]:
                    if parent not in ancestors[i]:
                        stack.append(parent)
    
    min_cost = float('inf')
    total_masks = 1 << n
    for mask in range(total_masks):
        valid = True
        for i in range(n):
            if (mask >> i) & 1:
                for j in ancestors[i]:
                    if not (mask >> j) & 1:
                        valid = False
                        break
                if not valid:
                    break
        
        if not valid:
            continue
        
        total_cal = 0
        total_prot = 0
        for i in range(n):
            if (mask >> i) & 1:
                total_cal += calories[i]
                total_prot += protein_list[i]
        
        if total_cal >= min_cal and total_prot >= min_protein:
            cost_here = 0
            for i in range(n):
                if (mask >> i) & 1:
                    cost_here += costs[i]
            if cost_here < min_cost:
                min_cost = cost_here
    
    return min_cost