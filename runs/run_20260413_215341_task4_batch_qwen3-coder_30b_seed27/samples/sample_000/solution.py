def sort_library_books(books: list[dict]) -> list[str]:
    # Calculate genre popularity
    genre_count = {}
    for book in books:
        genre = book['genre']
        genre_count[genre] = genre_count.get(genre, 0) + 1
    
    # Create a list of books with additional sorting information
    books_with_info = []
    for book in books:
        # Calculate the earliest reservation start time
        earliest_reservation = min(res[0] for res in book['reservations'])
        # Calculate the latest reservation end time
        latest_reservation = max(res[1] for res in book['reservations'])
        
        books_with_info.append({
            'id': book['id'],
            'due_date': book['due_date'],
            'genre': book['genre'],
            'priority': book['priority'],
            'earliest_reservation': earliest_reservation,
            'latest_reservation': latest_reservation,
            'genre_popularity': genre_count[book['genre']]
        })
    
    # Sort by due date, then priority, then genre popularity, then book ID
    books_with_info.sort(key=lambda x: (
        x['due_date'],
        -x['priority'],
        -x['genre_popularity'],
        x['id']
    ))
    
    # Group books with overlapping reservations
    groups = []
    visited = set()
    
    for i, book1 in enumerate(books_with_info):
        if i in visited:
            continue
            
        # Start a new group
        group = [book1]
        visited.add(i)
        
        # Find all books that overlap with this book's reservation period
        for j, book2 in enumerate(books_with_info):
            if j in visited or i == j:
                continue
                
            # Check if reservations overlap
            overlap = False
            for res1 in book1['reservations']:
                for res2 in book2['reservations']:
                    if res1[0] <= res2[1] and res2[0] <= res1[1]:
                        overlap = True
                        break
                if overlap:
                    break
            
            if overlap:
                group.append(book2)
                visited.add(j)
        
        groups.append(group)
    
    # Sort each group by the same criteria
    result = []
    for group in groups:
        group.sort(key=lambda x: (
            x['due_date'],
            -x['priority'],
            -x['genre_popularity'],
            x['id']
        ))
        result.extend([book['id'] for book in group])
    
    return result