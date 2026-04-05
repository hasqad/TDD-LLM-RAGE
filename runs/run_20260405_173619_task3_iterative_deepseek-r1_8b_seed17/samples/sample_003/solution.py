from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    costs = [r[1] for r in recipes]
    calories = [r[2][0] for r in recipes]
    protein_list = [r[2][1] for r in recipes]
    
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
    for mask in range(1 << n):
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
            total_cost = 0
            for i in range(n):
                if (mask >> i) & 1:
                    total_cost += costs[i]
            if total_cost < min_cost:
                min_cost = total_cost
    
    return min_cost