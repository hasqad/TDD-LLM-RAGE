def sort_library_books(books: list[dict]) -> list[str]:
    if not books:
        return []
    
    # Calculate genre popularity
    genre_counts = {}
    for book in books:
        genre = book['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Create book objects with calculated properties
    book_objects = []
    for book in books:
        # Calculate max reservation priority (highest priority first)
        max_priority = max([r[2] for r in book['reservations']], default=0) if book['reservations'] else 0
        
        # Calculate earliest reservation start time
        earliest_start = min([r[0] for r in book['reservations']], default=float('inf')) if book['reservations'] else float('inf')
        
        book_objects.append({
            'id': book['id'],
            'due_date': book['due_date'],
            'genre': book['genre'],
            'priority': book['priority'],
            'reservations': book['reservations'],
            'max_priority': max_priority,
            'earliest_start': earliest_start,
            'genre_popularity': genre_counts[book['genre']]
        })
    
    # Sort books by the specified criteria
    book_objects.sort(key=lambda x: (
        x['due_date'],           # 1) Due date (earliest first)
        -x['max_priority'],      # 2) Reservation priority (highest first)
        -x['genre_popularity'],  # 3) Genre popularity (most popular first)
        x['id']                  # 4) Book ID (lexicographically)
    ))
    
    # Check for circular dependencies
    # Create a graph of reservation overlaps
    reservation_graph = {}
    for book in book_objects:
        reservation_graph[book['id']] = []
    
    # Build dependency graph based on overlapping reservations
    for i, book1 in enumerate(book_objects):
        for j, book2 in enumerate(book_objects):
            if i != j:
                # Check if reservations overlap
                if has_overlapping_reservations(book1['reservations'], book2['reservations']):
                    reservation_graph[book1['id']].append(book2['id'])
    
    # Detect cycles using DFS
    visited = set()
    rec_stack = set()
    
    def is_cyclic(book_id):
        if book_id not in visited:
            visited.add(book_id)
            rec_stack.add(book_id)
            
            for neighbor in reservation_graph[book_id]:
                if neighbor not in visited:
                    if is_cyclic(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(book_id)
        return False
    
    # Check for any circular dependencies
    for book_id in reservation_graph:
        if book_id not in visited:
            if is_cyclic(book_id):
                # Circular dependency detected - return empty list or handle as needed
                return []
    
    # Group books with overlapping reservations together
    result = []
    processed = set()
    
    for book in book_objects:
        if book['id'] not in processed:
            # Find all books that have overlapping reservations with this book
            group = [book['id']]
            processed.add(book['id'])
            
            # Check for overlapping reservations
            for other_book in book_objects:
                if other_book['id'] not in processed and other_book['id'] != book['id']:
                    if has_overlapping_reservations(book['reservations'], other_book['reservations']):
                        group.append(other_book['id'])
                        processed.add(other_book['id'])
            
            # Sort group by book ID lexicographically
            group.sort()
            result.extend(group)
    
    # If no overlapping reservations, return sorted list
    if not result:
        return [book['id'] for book in book_objects]
    
    return result

def has_overlapping_reservations(res1, res2):
    """Check if two lists of reservation intervals have overlapping periods."""
    if not res1 or not res2:
        return False
    
    for r1 in res1:
        for r2 in res2:
            # Check if intervals [start1, end1] and [start2, end2] overlap
            if r1[0] <= r2[1] and r2[0] <= r1[1]:
                return True
    return False