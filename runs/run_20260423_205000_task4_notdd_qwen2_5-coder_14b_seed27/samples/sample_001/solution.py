def sort_library_books(books):
    from collections import defaultdict
    from functools import cmp_to_key

    # Step 1: Check for circular reservation dependencies
    def detect_cycles():
        graph = defaultdict(list)
        for book in books:
            for start, end in book['reservations']:
                for other_book in books:
                    if other_book != book and any(start <= r_end and end >= r_start for r_start, r_end in other_book['reservations']):
                        graph[book['id']].append(other_book['id'])

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

        for book in books:
            if dfs(book['id']):
                raise ValueError("Circular reservation dependencies detected")

    # Step 2: Sort books based on the given criteria
    def compare_books(b1, b2):
        if b1['due_date'] != b2['due_date']:
            return b1['due_date'] - b2['due_date']
        if b1['priority'] != b2['priority']:
            return b2['priority'] - b1['priority']
        genre_popularity = {genre: i for i, genre in enumerate(sorted(set(book['genre'] for book in books), reverse=True))}
        if genre_popularity[b1['genre']] != genre_popularity[b2['genre']]:
            return genre_popularity[b1['genre']] - genre_popularity[b2['genre']]
        return (b1['id'] > b2['id']) - (b1['id'] < b2['id'])

    # Step 3: Group books with overlapping reservation periods
    def group_books():
        grouped = []
        for book in sorted(books, key=cmp_to_key(compare_books)):
            if not any(any(start <= r_end and end >= r_start for start, end in book['reservations']) for _, reservations in grouped):
                grouped.append((book['id'], book['reservations']))
        return [book_id for book_id, _ in grouped]

    detect_cycles()
    return group_books()