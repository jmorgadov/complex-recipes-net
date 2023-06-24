import streamlit as st

from recipesnet.st_helpers import get_api, recip_ingr_widget

st.set_page_config("Recipes net", layout="wide")

api = get_api()

c1, c2 = st.columns(2)

with c1:
    st.header("Recipes")
    selected_ingrd = st.multiselect("Recipes tha use ...", api.ingredients)
    recipes = api.recipes_that_use(selected_ingrd)
    for rec in recipes:
        if st.button(rec):
            st.session_state.recipe = rec

with c2:
    recip_ingr_widget(selected_ingrd=selected_ingrd)
