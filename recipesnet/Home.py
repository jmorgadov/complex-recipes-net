import streamlit as st

from recipesnet.api import RecipesApi


def get_api() -> RecipesApi:
    if "api" not in st.session_state:
        st.session_state["api"] = RecipesApi()
    return st.session_state.api


st.set_page_config("Recipes net", layout="wide")

with st.spinner("Loading data..."):
    api = get_api()

st.header("Recipes")
selected_recipe = st.selectbox("Ingredients of ...", api.recipes)

ingrs = api.ingr_of(selected_recipe)
half1 = ingrs[: len(ingrs) // 2]
half2 = ingrs[len(ingrs) // 2 :]
c1, c2 = st.columns(2)

with c1:
    for ing in half1:
        st.write(ing)

with c2:
    for ing in half2:
        st.write(ing)
