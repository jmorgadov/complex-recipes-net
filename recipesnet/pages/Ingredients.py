import streamlit as st

from recipesnet.api import RecipesApi
from recipesnet.st_helpers import find_recipes, recip_ingr_widget

st.set_page_config("Recipes net", layout="wide")

st.title("Ingredients that goes with ...")
st.write(
    """
In this section you can search what ingredients you can use with others to 
make a delicius recipe.
    """
)

with st.spinner("Loading data..."):
    if "api" not in st.session_state:
        st.session_state["api"] = RecipesApi()
    api: RecipesApi = st.session_state.api

c1, c2, c3 = st.columns([1, 2, 2])



with c1:
    ingrd = st.selectbox("Select ingredient", api.ingredients)
    st.write("Click an ingredient to add it as selected")

    ingredients = api.ingrd_comb(ingrd)
    i = 0
    for ing, score in ingredients:
        print(ing, score, flush=True)
        if st.button(
            f"{ing.capitalize()}",
            key=f"ingr_btn_{i}",
        ):
            st.session_state.selected_ingr.add(ing)

        i += 1

with c2:
    find_recipes()

with c3:
    recip_ingr_widget()
