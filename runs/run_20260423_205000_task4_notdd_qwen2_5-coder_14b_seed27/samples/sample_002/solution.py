from typing import List, Dict

def sort_library_books(books: List[Dict]) -> List[str]:
    # Step 1: Detect circular reservation dependencies
    def has_circular_dependency(book_id: str, visited: set, rec_stack: set) -> bool:
        if book_id in rec_stack:
            return True
        if book_id in visited:
            return False
        
        visited.add(book_id)
        rec_stack.add(book_id)
        
        for book in books:
            if any(start <= res[0] <= end or start <= res[1] <= end or res[0] <= start <= end or res[1] >= end for start, end in book['reservations']):
                if has_circular_dependency(book['id'], visited, rec_stack):
                    return True
        
        rec_stack.remove(book_id)
        return False
    
    # Check for circular dependencies
    for book in books:
        if has_circular_dependency(book['id'], set(), set()):
            raise ValueError("Circular reservation dependencies detected")
    
    # Step 2: Sort books by the given criteria
    genre_popularity = {}
    for book in books:
        if book['genre'] not in genre_popularity:
            genre_popularity[book['genre']] = 0
        genre_popularity[book['genre']] += 1
    
    books.sort(key=lambda x: (x['due_date'], -x['priority'], -genre_popularity[x['genre']], x['id']))
    
    # Step 3: Group overlapping reservation periods
    def is_overlapping(book1, book2):
        for res1 in book1['reservations']:
            for res2 in book2['reservations']:
                if not (res1[1] < res2[0] or res2[1] < res1[0]):
                    return True
        return False
    
    grouped_books = []
    while books:
        current_group = [books.pop(0)]
        for book in books[:]:
            if is_overlapping(current_group[-1], book):
                current_group.append(book)
                books.remove(book)
        grouped_books.append(current_group)
    
    # Flatten the grouped books into a single sorted list
    sorted_ids = []
    for group in grouped_books:
        group.sort(key=lambda x: (x['due_date'], -x['priority'], -genre_popularity[x['genre']], x['id']))
        sorted_ids.extend(book['id'] for book in group)
    
    return sorted_ids