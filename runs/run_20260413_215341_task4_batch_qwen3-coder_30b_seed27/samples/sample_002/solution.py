def sort_library_books(books: list[dict]) -> list[str]:
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
            'reservation_groups': []
        }
        book_objects.append(book_obj)
    
    # Find overlapping reservation groups
    reservation_groups = []
    visited = set()
    
    for i, book1 in enumerate(book_objects):
        if i in visited:
            continue
            
        # Start a new group
        group = [i]
        visited.add(i)
        
        # Check for overlaps with other books
        for j, book2 in enumerate(book_objects):
            if j in visited or i == j:
                continue
                
            # Check if reservations overlap
            overlaps = False
            for res1 in book1['reservations']:
                for res2 in book2['reservations']:
                    if res1[0] <= res2[1] and res2[0] <= res1[1]:
                        overlaps = True
                        break
                if overlaps:
                    break
            
            if overlaps:
                group.append(j)
                visited.add(j)
        
        reservation_groups.append(group)
    
    # Sort groups by the earliest due date in the group
    for group in reservation_groups:
        group.sort(key=lambda x: book_objects[x]['due_date'])
    
    # Sort books within each group by the specified criteria
    for group in reservation_groups:
        group.sort(key=lambda x: (
            book_objects[x]['due_date'],
            -book_objects[x]['priority'],
            -book_objects[x]['genre_popularity'],
            book_objects[x]['id']
        ))
    
    # Flatten groups into final order
    final_order = []
    for group in reservation_groups:
        final_order.extend([book_objects[i]['id'] for i in group])
    
    # If there are books not in any group, add them at the end
    all_grouped_ids = set()
    for group in reservation_groups:
        all_grouped_ids.update([book_objects[i]['id'] for i in group])
    
    ungrouped_books = [book for book in book_objects if book['id'] not in all_grouped_ids]
    ungrouped_books.sort(key=lambda x: (
        x['due_date'],
        -x['priority'],
        -x['genre_popularity'],
        x['id']
    ))
    
    final_order.extend([book['id'] for book in ungrouped_books])
    
    return final_order