from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    if n == 0:
        return -1

    graph_parents = graph

    ancestor_mask = [0] * n
    for i in range(n):
        stack = [i]
        visited = set()
        mask_val = 0
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                mask_val |= (1 << node)
                for parent in graph_parents[node]:
                    if parent not in visited:
                        stack.append(parent)
        ancestor_mask[i] = mask_val

    min_cost = 10**9

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
        total_cost_val = 0
        for i in range(n):
            if mask & (1 << i):
                _, cost_val, (cal, prot) = recipes[i]
                total_cal += cal
                total_protein += prot
                total_cost_val += cost_val

        if total_cal >= min_cal and total_protein >= min_protein:
            if total_cost_val < min_cost:
                min_cost = total_cost_val

    if min_cost == 10**9:
        return -1
    else:
        return min_cost