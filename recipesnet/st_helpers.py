import streamlit as st

from recipesnet.api import RecipesApi


def get_api() -> RecipesApi:
    with st.spinner("Loading data..."):
        if "api" not in st.session_state:
            st.session_state["api"] = RecipesApi()
        return st.session_state.api


def recip_ingr_widget(selected_ingrd=None):
    st.header("Recipes ingredients")
    selected_ingrd = [] if selected_ingrd is None else selected_ingrd
    api = get_api()
    recipes = api.recipes
    selected_recipe = st.selectbox(
        "Ingredients of ...",
        recipes,
        recipes.index(st.session_state.recipe) if "recipe" in st.session_state else 0,
    )
    ingrs = sorted(api.ingr_of(selected_recipe))
    ingrs = [
        i.capitalize() if i not in selected_ingrd else f":red[{i.capitalize()}]"
        for i in ingrs
    ]
    st.write(", ".join(ingrs))

    if selected_recipe and st.button(
        f"🔎 How to prepare {selected_recipe.capitalize()}"
    ):
        st.write("TODO!")
