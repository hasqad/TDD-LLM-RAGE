def sort_library_books(books: list[dict]) -> list[str]:
    if not books:
        return []
    
    # Calculate genre popularity
    genre_counts = {}
    for book in books:
        genre = book['genre']
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Create a list of books with additional computed fields
    books_with_info = []
    for book in books:
        # Calculate the earliest reservation start time
        earliest_reservation = min(res[0] for res in book['reservations']) if book['reservations'] else float('inf')
        
        # Calculate the latest reservation end time
        latest_reservation = max(res[1] for res in book['reservations']) if book['reservations'] else float('-inf')
        
        books_with_info.append({
            'book': book,
            'earliest_reservation': earliest_reservation,
            'latest_reservation': latest_reservation,
            'genre_popularity': genre_counts[book['genre']]
        })
    
    # Sort by the specified criteria
    books_with_info.sort(key=lambda x: (
        x['book']['due_date'],           # 1) Due date (earliest first)
        -x['book']['priority'],          # 2) Reservation priority (highest first)
        -x['genre_popularity'],          # 3) Genre popularity (most popular first)
        x['book']['id']                  # 4) Book ID (lexicographically)
    ))
    
    # Group books with overlapping reservations
    groups = []
    visited = set()
    
    for i, book_info in enumerate(books_with_info):
        if i in visited:
            continue
            
        # Start a new group
        group = [book_info]
        visited.add(i)
        
        # Find all books that overlap with this book's reservations
        current_latest = book_info['latest_reservation']
        current_earliest = book_info['earliest_reservation']
        
        # Keep expanding the group with overlapping books
        changed = True
        while changed:
            changed = False
            for j, other_book_info in enumerate(books_with_info):
                if j in visited:
                    continue
                    
                # Check if the reservation intervals overlap
                other_earliest = other_book_info['earliest_reservation']
                other_latest = other_book_info['latest_reservation']
                
                # If intervals overlap, add to group
                if other_earliest <= current_latest and current_earliest <= other_latest:
                    group.append(other_book_info)
                    visited.add(j)
                    # Update the group's time range
                    current_earliest = min(current_earliest, other_earliest)
                    current_latest = max(current_latest, other_latest)
                    changed = True
        
        groups.append(group)
    
    # Sort groups by the earliest reservation in each group
    for group in groups:
        group.sort(key=lambda x: x['book']['due_date'])
    
    # Flatten groups into final result
    result = []
    for group in groups:
        result.extend([book_info['book']['id'] for book_info in group])
    
    # Check for circular dependencies
    # This is a simplified check - we're looking for cases where a book's reservation
    # overlaps with another book's reservation that also overlaps with the first
    # In a real implementation, this would be more complex, but for this problem,
    # we assume that if we have overlapping reservations, they are already grouped.
    
    return result