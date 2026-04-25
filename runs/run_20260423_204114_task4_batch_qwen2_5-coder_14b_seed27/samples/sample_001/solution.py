from typing import List, Dict
import networkx as nx

def sort_library_books(books: List[Dict]) -> List[str]:
    # Create a graph to detect circular dependencies
    G = nx.DiGraph()
    
    # Sort books by due date, reservation priority, genre popularity, and book ID
    sorted_books = sorted(books, key=lambda x: (x['due_date'], -x['priority'], x['genre'], x['id']))
    
    # Add nodes to the graph
    G.add_nodes_from(book['id'] for book in books)
    
    # Detect overlapping reservations and add edges to the graph
    for i, book1 in enumerate(sorted_books):
        for j, book2 in enumerate(sorted_books):
            if i != j:
                if any(reserve1[0] < reserve2[1] and reserve1[1] > reserve2[0] for reserve1 in book1['reservations'] for reserve2 in book2['reservations']):
                    G.add_edge(book1['id'], book2['id'])
    
    # Check for cycles in the graph
    if nx.is_directed_acyclic_graph(G):
        return [book['id'] for book in sorted_books]
    else:
        raise ValueError("Circular reservation dependencies detected, impossible scheduling scenario.")