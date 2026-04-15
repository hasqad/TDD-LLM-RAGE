def sort_library_books(books: list[dict]) -> list[str]:
    if not books:
        return []
    
    # Calculate genre popularity
    genre_count = {}
    for book in books:
        genre = book['genre']
        genre_count[genre] = genre_count.get(genre, 0) + 1
    
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
            'latest_reservation': latest_reservation,
            'genre_popularity': genre_count[book['genre']]
        })
    
    # Sort by due date, then reservation priority, then genre popularity, then book ID
    books_with_info.sort(key=lambda x: (
        x['book']['due_date'],
        -x['book']['priority'],
        -x['genre_popularity'],
        x['book']['id']
    ))
    
    # Check for circular dependencies
    # Build a graph of reservation overlaps
    n = len(books_with_info)
    # Create a mapping from book ID to index
    id_to_index = {book['book']['id']: i for i, book in enumerate(books_with_info)}
    
    # Build adjacency list for dependencies
    # A book A depends on book B if A's reservations overlap with B's reservations
    # and A has a later earliest reservation start time
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            
            book_a = books_with_info[i]['book']
            book_b = books_with_info[j]['book']
            
            # Check if reservations overlap
            overlap = False
            for start_a, end_a in book_a['reservations']:
                for start_b, end_b in book_b['reservations']:
                    if start_a <= end_b and start_b <= end_a:
                        overlap = True
                        break
                if overlap:
                    break
            
            if overlap:
                # If book A's earliest reservation starts after book B's latest reservation,
                # then book A depends on book B
                if books_with_info[i]['earliest_reservation'] > books_with_info[j]['latest_reservation']:
                    graph[j].append(i)
    
    # Detect cycles using DFS
    visited = [0] * n  # 0 = unvisited, 1 = visiting, 2 = visited
    stack = []
    
    def has_cycle(node):
        if visited[node] == 1:  # Currently visiting
            return True
        if visited[node] == 2:  # Already visited
            return False
            
        visited[node] = 1
        stack.append(node)
        
        for neighbor in graph[node]:
            if has_cycle(neighbor):
                return True
                
        visited[node] = 2
        stack.pop()
        return False
    
    # Check for cycles
    for i in range(n):
        if visited[i] == 0:
            if has_cycle(i):
                # Return empty list if circular dependency detected
                return []
    
    # Group books with overlapping reservations together
    # Create groups based on overlapping reservations
    groups = []
    used = [False] * n
    
    for i in range(n):
        if used[i]:
            continue
            
        # Start a new group
        group = [i]
        used[i] = True
        
        # Find all books that overlap with this book
        for j in range(n):
            if used[j]:
                continue
                
            book_a = books_with_info[i]['book']
            book_b = books_with_info[j]['book']
            
            # Check if reservations overlap
            overlap = False
            for start_a, end_a in book_a['reservations']:
                for start_b, end_b in book_b['reservations']:
                    if start_a <= end_b and start_b <= end_a:
                        overlap = True
                        break
                if overlap:
                    break
            
            if overlap:
                group.append(j)
                used[j] = True
        
        groups.append(group)
    
    # Sort each group by the original sorting criteria
    result = []
    for group in groups:
        # Sort the group by the original criteria
        group.sort(key=lambda x: (
            books_with_info[x]['book']['due_date'],
            -books_with_info[x]['book']['priority'],
            -books_with_info[x]['genre_popularity'],
            books_with_info[x]['book']['id']
        ))
        # Add book IDs to result
        result.extend([books_with_info[x]['book']['id'] for x in group])
    
    return result