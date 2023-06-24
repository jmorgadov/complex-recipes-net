import streamlit as st

from recipesnet.api import RecipesApi
from recipesnet.st_helpers import recip_ingr_widget

st.set_page_config("Recipes net", layout="wide")

with st.spinner("Loading data..."):
    if "api" not in st.session_state:
        st.session_state["api"] = RecipesApi()
    api: RecipesApi = st.session_state.api

c1, c2 = st.columns(2)

with c1:
    st.header("Similar recipes")

    recipes = api.recipes
    selected_recipe = st.selectbox(
        "Recipes similar to ...",
        recipes,
        recipes.index(st.session_state.recipe) if "recipe" in st.session_state else 0,
    )
    st.session_state.recipe = selected_recipe

    similar = api.similar_recipes(selected_recipe)
    for rec, score in similar:
        if st.button(f"{score:.1%}: {rec.capitalize()}"):
            st.session_state.recipe = rec

with c2:
    recip_ingr_widget()
