def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> list[str]:
    if target_w == seed and target_h == seed:
        return []
    
    # If target dimensions are larger than seed, it's impossible
    if target_w > seed or target_h > seed:
        return []
    
    # If either target dimension is 1, we need to fold it down to 1
    # We can only fold if the dimension is > 1
    
    w, h = seed, seed
    sequence = []
    
    # We need to find a sequence of folds that gets us to target_w, target_h
    # We'll use a greedy approach: at each step, decide whether to fold width or height
    
    # Since we want the minimal sequence, we can think of this as finding the shortest path
    # from (seed, seed) to (target_w, target_h) where each step is dividing one dimension by 2
    
    # We can use BFS or a greedy approach. Let's try a greedy approach first:
    # At each step, if we can fold to get closer to target, do it
    
    # Actually, let's think differently - we can work backwards from target to seed
    # But that might be more complex. Let's try forward simulation with BFS logic
    
    # Let's use a simple approach: simulate the process
    # We'll try to reach the target by folding
    
    # Greedy approach: fold the dimension that's further from target
    # But we need to be more careful - we can only fold if dimension > 1
    
    # Actually, let's just simulate the process
    # We'll try to reach target by folding, but we need to be smart about it
    
    # BFS approach would be more accurate, but let's try a simpler greedy method
    # that tries to get to the target as quickly as possible
    
    # But we also need to make sure we can reach the exact target
    # The key insight is that we can only reach dimensions that are powers of 2
    # or can be reduced to powers of 2 by halving
    
    # Let's think: if we have seed = 8, target = 4, 4
    # We can fold W to get 4, 8, then H to get 4, 4
    # So we want to go from (8,8) to (4,4)
    
    # A better approach: we can use BFS to find the shortest path
    # But let's first check if it's even possible
    
    # Check if target dimensions are reachable (they must be divisors of powers of 2)
    # Actually, that's not quite right. We can reach any dimension that divides the seed
    
    # Simpler approach: we'll simulate the process, but we need to be smart about it
    
    # We can use a greedy approach:
    # At each step, if we can fold to get closer to target, we do it
    # But we also need to be careful about the order
    
    # Actually, let's just simulate it properly:
    # We'll try to reach the target using BFS or a simple simulation
    
    # Let's use a simple greedy simulation
    # But we must be very careful to make sure we don't miss anything
    
    # The correct approach: we can only reach dimensions that are of the form seed / 2^k
    # where k is a non-negative integer, and the final dimensions must be <= seed
    
    # But we also need to make sure we can get to the exact target
    
    # Let's do a proper simulation approach:
    # We'll try to find a path from (seed, seed) to (target_w, target_h)
    # by applying operations: W (fold width) or H (fold height)
    
    # We'll use BFS to find the minimal sequence
    from collections import deque
    
    queue = deque([(seed, seed, [])])  # (width, height, sequence)
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        w, h, seq = queue.popleft()
        
        if w == target_w and h == target_h:
            return seq
            
        # Try folding width
        if w > 1:
            new_w = w // 2
            if (new_w, h) not in visited:
                visited.add((new_w, h))
                queue.append((new_w, h, seq + ['W']))
        
        # Try folding height
        if h > 1:
            new_h = h // 2
            if (w, new_h) not in visited:
                visited.add((w, new_h))
                queue.append((w, new_h, seq + ['H']))
    
    return []