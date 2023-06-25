import streamlit as st

from recipesnet.st_helpers import find_recipes, get_api, recip_ingr_widget

st.set_page_config("Recipes net", layout="wide")

api = get_api()

c1, c2 = st.columns(2)

with c1:
    find_recipes()

with c2:
    recip_ingr_widget()
