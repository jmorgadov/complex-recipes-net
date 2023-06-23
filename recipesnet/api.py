from functools import reduce
from operator import add
from typing import List

import networkx as nx

from recipesnet import recipes


class RecipesApi:
    def __init__(self):
        self.raw_data = recipes.load_data()
        self.graphs = recipes.load_all_graphs()
        self.recipes = list(self.raw_data.keys())
        self.ingredients = set(reduce(add, self.raw_data.values()))

    @property
    def recipes_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.RECIPES_GRAPH)]

    def similar_recipes(self, recipe: str) -> List[str]:
        G = self.recipes_graph
        data = []
        for nb in G.neighbors(recipe):
            w = G.edges[recipe, nb]["weight"]
            data.append((nb, w))
        return sorted(data, key=lambda x: x[1], reverse=True)
