def sort_library_books(books: list[dict]) -> list[str]:
    from collections import defaultdict
    from functools import cmp_to_key

    # Helper function to detect circular dependencies
    def has_cycle(graph):
        visited = set()
        rec_stack = set()

        def dfs(node):
            if node in rec_stack:
                return True
            if node in visited:
                return False
            visited.add(node)
            rec_stack.add(node)
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True
            rec_stack.remove(node)
            return False

        for node in graph:
            if dfs(node):
                return True
        return False

    # Build the reservation graph to detect cycles
    reservation_graph = defaultdict(list)
    for i, book1 in enumerate(books):
        for start1, end1 in book1['reservations']:
            for j, book2 in enumerate(books):
                if i != j:
                    for start2, end2 in book2['reservations']:
                        if not (end1 <= start2 or end2 <= start1):
                            reservation_graph[book1['id']].append(book2['id'])

    # Check for cycles
    if has_cycle(reservation_graph):
        raise ValueError("Circular reservation dependencies detected")

    # Sort books based on the given priority rules
    def book_cmp(b1, b2):
        if b1['due_date'] != b2['due_date']:
            return b1['due_date'] - b2['due_date']
        if b1['priority'] != b2['priority']:
            return b2['priority'] - b1['priority']
        genre_popularity = {genre: i for i, genre in enumerate(sorted(set(b['genre'] for b in books), reverse=True))}
        if genre_popularity[b1['genre']] != genre_popularity[b2['genre']]:
            return genre_popularity[b1['genre']] - genre_popularity[b2['genre']]
        return (b1['id'] > b2['id']) - (b1['id'] < b2['id'])

    sorted_books = sorted(books, key=cmp_to_key(book_cmp))

    # Group books with overlapping reservations
    grouped_books = []
    current_group = [sorted_books[0]['id']]
    for book in sorted_books[1:]:
        overlaps = any(
            any(start1 < end2 and start2 < end1 for start1, end1 in book['reservations'] for start2, end2 in b['reservations'])
            for b in books if b['id'] in current_group
        )
        if not overlaps:
            grouped_books.append(current_group)
            current_group = []
        current_group.append(book['id'])

    # Add the last group
    if current_group:
        grouped_books.append(current_group)

    # Flatten the list of groups into a single sorted list
    return [book_id for group in grouped_books for book_id in group]