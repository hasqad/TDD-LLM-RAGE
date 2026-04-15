def sort_library_books(books: list[dict]) -> list[str]:
    if not books:
        return []
    
    # Calculate genre popularity
    genre_counts = {}
    for book in books:
        genre = book['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Create a list of books with additional sorting information
    books_with_info = []
    for book in books:
        # Calculate the earliest reservation start time
        earliest_reservation = float('inf')
        for start, end in book['reservations']:
            earliest_reservation = min(earliest_reservation, start)
        
        # Calculate the latest reservation end time
        latest_reservation = float('-inf')
        for start, end in book['reservations']:
            latest_reservation = max(latest_reservation, end)
        
        books_with_info.append({
            'book': book,
            'earliest_reservation': earliest_reservation,
            'latest_reservation': latest_reservation
        })
    
    # Sort by due date, then reservation priority, then genre popularity, then book ID
    books_with_info.sort(key=lambda x: (
        x['book']['due_date'],
        -x['book']['priority'],
        -genre_counts[x['book']['genre']],
        x['book']['id']
    ))
    
    # Group books with overlapping reservations
    groups = []
    visited = set()
    
    for i in range(len(books_with_info)):
        if i in visited:
            continue
            
        # Start a new group
        group = [i]
        visited.add(i)
        
        # Find all books that overlap with this book's reservation period
        current_book = books_with_info[i]
        current_start = current_book['earliest_reservation']
        current_end = current_book['latest_reservation']
        
        # Check for overlaps with remaining books
        for j in range(i + 1, len(books_with_info)):
            if j in visited:
                continue
                
            other_book = books_with_info[j]
            other_start = other_book['earliest_reservation']
            other_end = other_book['latest_reservation']
            
            # Check if intervals overlap
            if current_start <= other_end and other_start <= current_end:
                group.append(j)
                visited.add(j)
        
        groups.append(group)
    
    # Check for circular dependencies
    # Build a dependency graph
    graph = {}
    for i in range(len(books_with_info)):
        graph[i] = set()
    
    # For each pair of books, check if one's reservations conflict with another's
    for i in range(len(books_with_info)):
        for j in range(len(books_with_info)):
            if i == j:
                continue
                
            book1 = books_with_info[i]
            book2 = books_with_info[j]
            
            # Check if book1's reservations conflict with book2's reservations
            conflict = False
            for start1, end1 in book1['book']['reservations']:
                for start2, end2 in book2['book']['reservations']:
                    if start1 <= end2 and start2 <= end1:
                        conflict = True
                        break
                if conflict:
                    break
            
            if conflict:
                graph[i].add(j)
    
    # Detect cycles using DFS
    def has_cycle(node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    # Check for any cycles
    visited = set()
    rec_stack = set()
    
    for i in range(len(books_with_info)):
        if i not in visited:
            if has_cycle(i, visited, rec_stack):
                # If there's a cycle, we need to handle it by sorting by due date only
                books_with_info.sort(key=lambda x: x['book']['due_date'])
                return [book['book']['id'] for book in books_with_info]
    
    # Sort groups by the earliest due date in each group
    final_order = []
    
    # Process groups
    for group in groups:
        # Sort the books in this group by the original sorting criteria
        group_books = [books_with_info[i] for i in group]
        group_books.sort(key=lambda x: (
            x['book']['due_date'],
            -x['book']['priority'],
            -genre_counts[x['book']['genre']],
            x['book']['id']
        ))
        
        # Add the books in this group to the final order
        final_order.extend([book['book']['id'] for book in group_books])
    
    # If there are groups that are not sorted by due date, sort them by due date
    # Create a list of groups and their earliest due dates
    group_info = []
    for i, group in enumerate(groups):
        earliest_due = min(books_with_info[j]['book']['due_date'] for j in group)
        group_info.append((i, earliest_due))
    
    # Sort groups by earliest due date
    group_info.sort(key=lambda x: x[1])
    
    # Reorder final order by group due dates
    result = []
    for group_idx, _ in group_info:
        group = groups[group_idx]
        group_books = [books_with_info[i] for i in group]
        group_books.sort(key=lambda x: (
            x['book']['due_date'],
            -x['book']['priority'],
            -genre_counts[x['book']['genre']],
            x['book']['id']
        ))
        result.extend([book['book']['id'] for book in group_books])
    
    return result