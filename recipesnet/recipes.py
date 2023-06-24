import json
import zipfile
from collections import defaultdict
from pathlib import Path

import networkx as nx

import recipesnet

DATA_PATH = Path(recipesnet.__file__).parent / Path("data")
ZIP_DATA_PATH = DATA_PATH / Path("recipe_jsons.zip")

DATA_NITZA = DATA_PATH / Path("recipes_nitza.json")
DATA_5K = DATA_PATH / Path("recipes_5k.json")
FINAL_DATA = DATA_PATH / Path("data.json")

RECIPES_GRAPH = DATA_PATH / Path("recipes_graph.gz")
RECP_INGR_GRAPH = DATA_PATH / Path("recp_ingr_graph.gz")

GRAPH_PATHS = [
    RECIPES_GRAPH,
    RECP_INGR_GRAPH,
]


def unzip_data():
    with zipfile.ZipFile(str(ZIP_DATA_PATH), "r") as zip_ref:
        zip_ref.extractall(DATA_PATH)


def preprocess_nitza(data: dict) -> dict:
    new_data = defaultdict(list)
    for rec_name, rec_data in data.items():
        new_data[rec_name] = [ing["name"] for ing in rec_data["ingredients"]]
    return new_data


def preprocess_data_5k(data: dict) -> dict:
    new_data = defaultdict(list)
    for rec_name, rec_data in data.items():
        new_data[rec_name] = [ing["name"] for ing in rec_data["ingredients_simplified"]]
    return new_data


def load_data():
    if FINAL_DATA.exists():
        with open(str(FINAL_DATA), "r", encoding="utf-8") as datafd:
            return json.load(datafd)

    if not DATA_NITZA.exists() or not DATA_5K.exists():
        unzip_data()

    data = {}

    with open(str(DATA_NITZA), "r", encoding="utf-8") as datafd:
        data_nitza = preprocess_nitza(json.load(datafd))
        data.update(data_nitza)

    with open(str(DATA_5K), "r", encoding="utf-8") as datafd:
        data_5k = preprocess_data_5k(json.load(datafd))
        data.update(data_5k)

    with open(str(FINAL_DATA), "w", encoding="utf-8") as datafd:
        json.dump(data, datafd, indent=4, ensure_ascii=False)

    return data


def create_graph(name: str):
    data = load_data()

    if name == str(RECIPES_GRAPH):
        recipes = list(data.keys())

        # Recipies graph:
        #  V: Recipe
        #  E: % of ing in common (more than 0.3)
        G = nx.Graph()
        for i, r1 in enumerate(recipes):
            ing1 = set(data[r1])
            for j in range(i + 1, len(recipes)):
                r2 = recipes[j]
                ing2 = set(data[r2])
                union = ing1 | ing2
                if len(union) == 0:
                    continue
                inter = ing1 & ing2
                w = len(inter) / len(union)
                if w > 0.3:
                    G.add_edge(r1, r2, weight=w)

        nx.write_graphml(G, name, encoding="utf-8")
        return G

    if name == str(RECP_INGR_GRAPH):
        recipes = list(data.keys())

        # Recp-Ingr bipartite graph:
        #  V: Ingredient | Recipe
        #  E: (u, v) means u is ingridient of recipe v (or vice versa)
        G = nx.Graph()
        for i, rec in enumerate(recipes):
            ingrs = set(data[rec])
            G.add_node(rec, is_recipe=True, is_ingr=False)
            for ing in ingrs:
                G.add_node(ing, is_recipe=False, is_ingr=True)
                G.add_edge(ing, rec)

        nx.write_graphml(G, name, encoding="utf-8")
        return G


def load_graph(name):
    for graph in GRAPH_PATHS:
        if name == str(graph):
            if not graph.exists():
                return create_graph(name)
            return nx.read_graphml(name)


def load_all_graphs() -> dict:
    graphs = {}
    for graph in GRAPH_PATHS:
        path = str(graph)
        graphs[path] = load_graph(path)
    return graphs
