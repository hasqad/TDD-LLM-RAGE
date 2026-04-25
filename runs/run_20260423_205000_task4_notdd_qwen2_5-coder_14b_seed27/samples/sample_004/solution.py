def sort_library_books(books):
    from collections import defaultdict

    # Step 1: Check for circular reservation dependencies
    def has_circular_dependency(book_id, visited, recursion_stack, book_map):
        if book_id in recursion_stack:
            return True
        if book_id in visited:
            return False
        
        visited.add(book_id)
        recursion_stack.add(book_id)
        
        for other_book_id in book_map[book_id]:
            if has_circular_dependency(other_book_id, visited, recursion_stack, book_map):
                return True
        
        recursion_stack.remove(book_id)
        return False

    # Step 2: Build a graph to detect circular dependencies
    book_map = defaultdict(set)
    for i in range(len(books)):
        for j in range(i + 1, len(books)):
            if any(r1[0] < r2[1] and r1[1] > r2[0] for r1 in books[i]['reservations'] for r2 in books[j]['reservations']):
                book_map[books[i]['id']].add(books[j]['id'])
                book_map[books[j]['id']].add(books[i]['id'])

    # Step 3: Detect circular dependencies
    visited = set()
    recursion_stack = set()
    for book in books:
        if has_circular_dependency(book['id'], visited, recursion_stack, book_map):
            raise ValueError("Circular reservation dependency detected")

    # Step 4: Sort books based on the given criteria
    sorted_books = sorted(books, key=lambda x: (x['due_date'], -x['priority'], genres.popularity.get(x['genre'], 0), x['id']))

    # Step 5: Group overlapping reservations together
    result = []
    current_group = []
    for book in sorted_books:
        if not current_group or not any(r1[0] < r2[1] and r1[1] > r2[0] for r1 in book['reservations'] for r2 in current_group):
            if current_group:
                result.extend(sorted(current_group, key=lambda x: x['id']))
                current_group = []
        current_group.append(book)
    if current_group:
        result.extend(sorted(current_group, key=lambda x: x['id']))

    return [book['id'] for book in result]