from functools import reduce
from operator import add
from typing import List, Tuple

import networkx as nx

from recipesnet import recipes


class RecipesApi:
    def __init__(self):
        self.raw_data = recipes.load_data()
        self.graphs = recipes.load_all_graphs()
        self.recipes = sorted(
            [n for n, d in self.recp_ingr_graph.nodes(data=True) if d["is_recipe"]]
        )
        self.ingredients = sorted(
            [n for n, d in self.recp_ingr_graph.nodes(data=True) if d["is_ingr"]]
        )
        # self.ingredients = sorted(list(reduce(add, self.raw_data.values())))

    @property
    def recipes_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.RECIPES_GRAPH)]

    @property
    def recp_ingr_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.RECP_INGR_GRAPH)]

    def ingr_of(self, recipe) -> List[str]:
        return list(self.recp_ingr_graph.neighbors(recipe))

    def recipes_that_use(self, ingrds: List[str]):
        if not ingrds:
            return []
        recipes = set(self.recp_ingr_graph.neighbors(ingrds[0]))
        for ing in ingrds[1:]:
            recipes = recipes & set(self.recp_ingr_graph.neighbors(ing))
        return sorted(list(recipes))

    def similar_recipes(self, recipe: str) -> List[Tuple[str, float]]:
        G = self.recipes_graph
        data = []
        for nb in G.neighbors(recipe):
            w = G.edges[recipe, nb]["weight"]
            data.append((nb, w))
        return sorted(data, key=lambda x: x[1], reverse=True)
