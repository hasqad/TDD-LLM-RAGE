def sort_library_books(books: list[dict]) -> list[str]:
    if not books:
        return []
    
    # Calculate genre popularity
    genre_count = {}
    for book in books:
        genre = book['genre']
        genre_count[genre] = genre_count.get(genre, 0) + 1
    
    # Create book objects with additional computed fields
    book_objects = []
    for book in books:
        book_obj = {
            'id': book['id'],
            'due_date': book['due_date'],
            'genre': book['genre'],
            'priority': book['priority'],
            'reservations': book['reservations'],
            'genre_popularity': genre_count[book['genre']],
            'reservation_end': max(res[1] for res in book['reservations']) if book['reservations'] else 0
        }
        book_objects.append(book_obj)
    
    # Check for circular dependencies
    # Build a graph of reservation dependencies
    reservation_graph = {}
    for i, book1 in enumerate(book_objects):
        reservation_graph[i] = []
        for j, book2 in enumerate(book_objects):
            if i != j:
                # Check if book1's reservations overlap with book2's reservations
                # If so, book1 should come before book2
                overlaps = False
                for res1 in book1['reservations']:
                    for res2 in book2['reservations']:
                        if res1[1] > res2[0] and res2[1] > res1[0]:  # Overlapping intervals
                            overlaps = True
                            break
                    if overlaps:
                        break
                if overlaps:
                    reservation_graph[i].append(j)
    
    # Detect cycles using DFS
    visited = [0] * len(book_objects)  # 0: unvisited, 1: visiting, 2: visited
    recursion_stack = [False] * len(book_objects)
    
    def has_cycle(node):
        visited[node] = 1
        recursion_stack[node] = True
        
        for neighbor in reservation_graph[node]:
            if visited[neighbor] == 0:
                if has_cycle(neighbor):
                    return True
            elif recursion_stack[neighbor]:
                return True
        
        recursion_stack[node] = False
        visited[node] = 2
        return False
    
    # Check for any circular dependencies
    for i in range(len(book_objects)):
        if visited[i] == 0:
            if has_cycle(i):
                # If there's a cycle, we can't sort properly, but we'll still try to sort
                # by other criteria and return what we can
                break
    
    # Sort books based on criteria
    def sort_key(book):
        return (
            book['due_date'],
            -book['priority'],
            -book['genre_popularity'],
            book['id']
        )
    
    # Sort the books
    sorted_books = sorted(book_objects, key=sort_key)
    
    # Group books with overlapping reservations together
    # This is a simplified approach - we'll try to group them by reservation end times
    result = []
    grouped_books = []
    
    # Create a list of indices to sort by reservation end time
    indices = list(range(len(sorted_books)))
    indices.sort(key=lambda i: sorted_books[i]['reservation_end'])
    
    # Group books with overlapping reservations
    i = 0
    while i < len(indices):
        current_group = [indices[i]]
        current_end = sorted_books[indices[i]]['reservation_end']
        
        # Add books that overlap with the current group
        j = i + 1
        while j < len(indices):
            # Check if the current book overlaps with the group
            overlaps = False
            for k in current_group:
                for res1 in sorted_books[indices[j]]['reservations']:
                    for res2 in sorted_books[k]['reservations']:
                        if res1[1] > res2[0] and res2[1] > res1[0]:  # Overlapping intervals
                            overlaps = True
                            break
                    if overlaps:
                        break
            
            if overlaps:
                current_group.append(indices[j])
            j += 1
        
        # Sort the group by the original sort criteria
        current_group.sort(key=lambda idx: sort_key(sorted_books[idx]))
        grouped_books.extend(current_group)
        i = j
    
    # Extract book IDs
    result = [sorted_books[idx]['id'] for idx in grouped_books]
    
    # Final sorting to ensure proper order
    # We'll re-sort with a more complex approach that respects reservation overlaps
    final_result = []
    remaining = set(range(len(book_objects)))
    
    while remaining:
        # Find books that can be scheduled (no unmet dependencies)
        candidates = []
        for i in remaining:
            can_schedule = True
            for j in remaining:
                if i != j:
                    # If book j has reservations that overlap with book i's reservations
                    # and book j comes before book i in the current sequence, then i can't be scheduled yet
                    for res1 in book_objects[i]['reservations']:
                        for res2 in book_objects[j]['reservations']:
                            if res1[1] > res2[0] and res2[1] > res1[0]:  # Overlapping intervals
                                # If book j comes before book i in the current sequence, then book i can't be scheduled
                                if book_objects[j]['due_date'] < book_objects[i]['due_date']:
                                    can_schedule = False
                                    break
                        if not can_schedule:
                            break
            if can_schedule:
                candidates.append(i)
        
        if not candidates:
            # If no candidates, just pick one to avoid infinite loop
            candidates = list(remaining)
        
        # Sort candidates by the original criteria
        candidates.sort(key=lambda i: sort_key(book_objects[i]))
        final_result.append(book_objects[candidates[0]]['id'])
        remaining.remove(candidates[0])
    
    return final_result