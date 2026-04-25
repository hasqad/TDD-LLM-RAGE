from typing import List, Dict

def sort_library_books(books: List[Dict]) -> List[str]:
    def has_circular_dependency(book_id: str, visited: set, recursion_stack: set) -> bool:
        if book_id in recursion_stack:
            return True
        if book_id in visited:
            return False
        
        visited.add(book_id)
        recursion_stack.add(book_id)
        
        for other_book in books:
            if any(start <= end and start >= other_start or end >= start and end <= other_end 
                   for start, end in books[book_id]['reservations'] 
                   for other_start, other_end in other_book['reservations']):
                if has_circular_dependency(other_book['id'], visited, recursion_stack):
                    return True
        
        recursion_stack.remove(book_id)
        return False

    def detect_circular_dependencies() -> bool:
        visited = set()
        for book in books:
            if has_circular_dependency(book['id'], visited, set()):
                return True
        return False

    if detect_circular_dependencies():
        raise ValueError("Circular reservation dependencies detected")

    # Sort by due date, then by priority (descending), then by genre popularity (descending), then by ID
    sorted_books = sorted(books, key=lambda x: (x['due_date'], -x['priority'], genres_popularity[x['genre']], x['id']))

    # Group books with overlapping reservation periods
    result = []
    for book in sorted_books:
        if not any(start <= end and start >= other_start or end >= start and end <= other_end 
                   for start, end in book['reservations'] 
                   for other_start, other_end in b['reservations']):
            result.append(book['id'])
    
    return result