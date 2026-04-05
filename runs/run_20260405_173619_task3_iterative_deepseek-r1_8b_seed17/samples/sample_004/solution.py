def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    costs_arr = [0] * n
    cal_arr = [0] * n
    pro_arr = [0] * n
    for i in range(n):
        name, cost, (cal_val, pro_val) = recipes[i]
        costs_arr[i] = cost
        cal_arr[i] = cal_val
        pro_arr[i] = pro_val
        
    parent_mask = [0] * n
    for i in range(n):
        for parent in graph[i]:
            parent_mask[i] |= (1 << parent)
            
    N = 1 << n
    best = float('inf')
    
    for mask in range(N):
        valid_flag = True
        for i in range(n):
            if mask & (1 << i):
                if (mask & parent_mask[i]) != parent_mask[i]:
                    valid_flag = False
                    break
                    
        if not valid_flag:
            continue
            
        total_cal_val = 0
        total_pro_val = 0
        total_cost_val = 0
        for i in range(n):
            if mask & (1 << i):
                total_cal_val += cal_arr[i]
                total_pro_val += pro_arr[i]
                total_cost_val += costs_arr[i]
                
        if total_cal_val >= min_cal and total_pro_val >= min_protein:
            if total_cost_val < best:
                best = total_cost_val
                
    return best if best != float('inf') else -1