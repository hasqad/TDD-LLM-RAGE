def recipe_chain_optimization(n: int, recipes: list, graph: list, min_cal: int, min_protein: int) -> int:
    if n == 0:
        return 0
    
    ancestor_mask = [0] * n
    for i in range(n):
        stack = [i]
        while stack:
            node = stack.pop()
            for parent in graph[node]:
                if not (ancestor_mask[i] & (1 << parent)):
                    ancestor_mask[i] |= (1 << parent)
                    stack.append(parent)
    
    min_cost = float('inf')
    for mask in range(1 << n):
        valid = True
        for i in range(n):
            if mask & (1 << i):
                if (mask & ancestor_mask[i]) != ancestor_mask[i]:
                    valid = False
                    break
        
        if not valid:
            continue
        
        total_cal = 0
        total_protein = 0
        total_cost = 0
        for i in range(n):
            if mask & (1 << i):
                _, cost, (cal, prot) = recipes[i]
                total_cal += cal
                total_protein += prot
                total_cost += cost
        
        if total_cal >= min_cal and total_protein >= min_protein:
            if total_cost < min_cost:
                min_cost = total_cost
    
    return min_cost if min_cost != float('inf') else -1