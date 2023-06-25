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

    @property
    def recipes_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.RECIPES_GRAPH)]

    @property
    def recp_ingr_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.RECP_INGR_GRAPH)]

    @property
    def ingr_graph(self) -> nx.Graph:
        return self.graphs[str(recipes.INGR_GRAPH)]

    def ingr_of(self, recipe) -> List[str]:
        return list(self.recp_ingr_graph.neighbors(recipe))

    def recipes_that_use(
        self,
        ingrds: List[str],
        ignore: List[str],
        only: bool = False,
        limit: int = -1,
    ):
        if not ingrds:
            return []

        recipes = set()
        for ing in ingrds:
            nb = set(self.recp_ingr_graph.neighbors(ing))
            new_recipes = set()

            for rec in nb:
                if limit != -1 and len(self.recp_ingr_graph.neighbors((rec))) > limit:
                    continue
                new_recipes.add(rec)
            recipes = recipes & new_recipes if recipes else new_recipes

        ans = []
        if only:
            ingr_set = set(ingrds)
            for rec in recipes:
                rec_ingrd = set(self.recp_ingr_graph.neighbors(rec))
                if ingr_set == rec_ingrd:
                    ans.append(rec)
        else:
            for rec in recipes:
                for ig_ing in ignore:
                    if self.recp_ingr_graph.has_edge(rec, ig_ing):
                        break
                else:
                    ans.append(rec)
        return sorted(ans)

    def similar_recipes(self, recipe: str) -> List[Tuple[str, float]]:
        G = self.recipes_graph
        data = []
        for nb in G.neighbors(recipe):
            w = G.edges[recipe, nb]["weight"]
            data.append((nb, w))
        return sorted(data, key=lambda x: x[1], reverse=True)

    def ingrd_comb(self, ingrd):
        G = self.ingr_graph
        data = []
        for nb in G.neighbors(ingrd):
            w = G.edges[ingrd, nb]["weight"]
            data.append((nb, w))
        return sorted(data, key=lambda x: x[1], reverse=False)
