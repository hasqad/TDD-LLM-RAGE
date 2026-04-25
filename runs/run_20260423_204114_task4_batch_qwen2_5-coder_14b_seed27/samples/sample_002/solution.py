def sort_library_books(books: list[dict]) -> list[str]:
    from collections import defaultdict

    # Step 1: Detect circular reservation dependencies
    def has_circular_dependency(book):
        visited = set()
        stack = set()

        def dfs(b):
            if b in stack:
                return True
            if b in visited:
                return False
            visited.add(b)
            stack.add(b)
            for res in books[b]['reservations']:
                for other_book, other_res in zip(books, [b['reservations'] for b in books]):
                    if other_book != books[b] and not (other_res[0] > res[1] or other_res[1] < res[0]):
                        if dfs(other_book):
                            return True
            stack.remove(b)
            return False

        return dfs(book)

    # Check for circular dependencies
    for book in books:
        if has_circular_dependency(book['id']):
            raise ValueError("Circular reservation dependency detected")

    # Step 2: Sort books by the given criteria
    def sort_key(book):
        return (
            book['due_date'],
            -book['priority'],
            genre_popularity[book['genre']],
            book['id']
        )

    # Calculate genre popularity based on number of books in each genre
    genre_count = defaultdict(int)
    for book in books:
        genre_count[book['genre']] += 1
    genre_popularity = {genre: count for genre, count in sorted(genre_count.items(), key=lambda x: (-x[1], x[0]))}

    # Sort the books
    sorted_books = sorted(books, key=sort_key)

    # Step 3: Group books with overlapping reservation periods
    grouped_books = []
    current_group = []

    for book in sorted_books:
        if not current_group:
            current_group.append(book)
        else:
            overlap = False
            for res in current_group[-1]['reservations']:
                for other_res in book['reservations']:
                    if not (other_res[0] > res[1] or other_res[1] < res[0]):
                        overlap = True
                        break
                if overlap:
                    break
            if overlap:
                current_group.append(book)
            else:
                grouped_books.extend(b['id'] for b in sorted(current_group, key=lambda x: sort_key(x)))
                current_group = [book]

    if current_group:
        grouped_books.extend(b['id'] for b in sorted(current_group, key=lambda x: sort_key(x)))

    return grouped_books