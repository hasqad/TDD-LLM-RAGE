from typing import List, Dict

def sort_library_books(books: List[Dict]) -> List[str]:
    def has_circular_dependency(book_id: str, visited: set, recursion_stack: set) -> bool:
        if book_id in recursion_stack:
            return True
        if book_id in visited:
            return False
        
        visited.add(book_id)
        recursion_stack.add(book_id)
        
        for reservation in books_dict[book_id]['reservations']:
            for other_book_id, other_reservations in books_dict.items():
                if other_book_id == book_id:
                    continue
                for start, end in other_reservations['reservations']:
                    if not (reservation[1] <= start or reservation[0] >= end):
                        if has_circular_dependency(other_book_id, visited, recursion_stack):
                            return True
        
        recursion_stack.remove(book_id)
        return False

    books_dict = {book['id']: book for book in books}
    visited = set()
    for book_id in books_dict:
        if has_circular_dependency(book_id, visited, set()):
            raise ValueError("Circular reservation dependencies detected")

    # Sort by due date, priority, genre popularity (assuming more popular genres are listed first),
    # and then by book ID lexicographically
    sorted_books = sorted(books, key=lambda x: (x['due_date'], -x['priority'], books_dict[x['genre']]['popularity'], x['id']))

    # Group books with overlapping reservation periods
    result = []
    current_group = []
    for book in sorted_books:
        if not current_group:
            current_group.append(book)
        else:
            overlap = False
            for start, end in book['reservations']:
                for other_book in current_group:
                    for other_start, other_end in other_book['reservations']:
                        if not (start >= other_end or end <= other_start):
                            overlap = True
                            break
                    if overlap:
                        break
            if overlap:
                result.append([b['id'] for b in sorted(current_group, key=lambda x: (-x['priority'], x['genre']))])
                current_group = [book]
            else:
                current_group.append(book)
    
    if current_group:
        result.append([b['id'] for b in sorted(current_group, key=lambda x: (-x['priority'], x['genre']))])

    return [book_id for group in result for book_id in group]

# Example usage
books = [
    {'id': 'B001', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[50, 80], [90, 110]], 'priority': 3},
    {'id': 'B002', 'due_date': 120, 'genre': 'Science', 'reservations': [[60, 100]], 'priority': 1},
    {'id': 'B003', 'due_date': 80, 'genre': 'Fiction', 'reservations': [[70, 90]], 'priority': 2}
]
print(sort_library_books(books))