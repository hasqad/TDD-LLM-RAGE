from solution import sort_library_books

def test_verified_example():
    books = [
        {'id': 'B001', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[50, 80], [90, 110]], 'priority': 3},
        {'id': 'B002', 'due_date': 120, 'genre': 'Science', 'reservations': [[60, 100]], 'priority': 1},
        {'id': 'B003', 'due_date': 80, 'genre': 'Fiction', 'reservations': [[70, 90]], 'priority': 2}
    ]
    expected = ['B003', 'B001', 'B002']
    assert sort_library_books(books) == expected

def test_no_reservation_overlap():
    books = [
        {'id': 'B001', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[50, 80]], 'priority': 3},
        {'id': 'B002', 'due_date': 120, 'genre': 'Science', 'reservations': [[90, 100]], 'priority': 1},
        {'id': 'B003', 'due_date': 80, 'genre': 'Fiction', 'reservations': [[70, 90]], 'priority': 2}
    ]
    expected = ['B003', 'B001', 'B002']
    assert sort_library_books(books) == expected

def test_same_due_date_different_priorities():
    books = [
        {'id': 'B001', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[50, 80]], 'priority': 1},
        {'id': 'B002', 'due_date': 100, 'genre': 'Science', 'reservations': [[60, 100]], 'priority': 3},
        {'id': 'B003', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[70, 90]], 'priority': 2}
    ]
    expected = ['B002', 'B003', 'B001']
    assert sort_library_books(books) == expected

def test_genre_popularity():
    books = [
        {'id': 'B001', 'due_date': 100, 'genre': 'Fiction', 'reservations': [[50, 80]], 'priority': 3},
        {'id': 'B002', 'due_date': 120, 'genre': 'Science', 'reservations': [[60, 100]], 'priority': 1},
        {'id': 'B003', 'due_date': 80, 'genre': 'Science', 'reservations': [[70, 90]], 'priority': 2}
    ]
    expected = ['B003', 'B001', 'B002']
    assert sort_library_books(books) == expected