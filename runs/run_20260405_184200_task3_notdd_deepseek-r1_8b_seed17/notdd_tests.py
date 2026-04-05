from solution import recipe_chain_optimization

def test_example():
    recipes = [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))]
    graph = [[], [0], [0]]
    min_cal = 20
    min_protein = 10
    assert recipe_chain_optimization(3, recipes, graph, min_cal, min_protein) == 40

def test_one_recipe_meets():
    recipes = [("Recipe1", 10, (20, 10))]
    graph = [[]]
    min_cal = 20
    min_protein = 10
    assert recipe_chain_optimization(1, recipes, graph, min_cal, min_protein) == 10

def test_two_recipes_dependency():
    recipes = [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10))]
    graph = [[], [0]]
    min_cal = 15
    min_protein = 5
    assert recipe_chain_optimization(2, recipes, graph, min_cal, min_protein) == 30

def test_two_recipes_dependency_with_parents():
    recipes = [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))]
    graph = [[], [0, 2], [0]]
    min_cal = 20
    min_protein = 10
    assert recipe_chain_optimization(3, recipes, graph, min_cal, min_protein) == 40