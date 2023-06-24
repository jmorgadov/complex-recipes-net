import streamlit as st
import urllib.request

from bs4 import BeautifulSoup
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
        query = selected_recipe

        query = "+".join(query.split(" "))
        url = f"https://google.com/search?q={query}"

        # Perform the request
        request = urllib.request.Request(url)

        # Set a normal User Agent header, otherwise Google will block the request.
        request.add_header(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        )
        raw_response = urllib.request.urlopen(request).read()

        # Read the repsonse as a utf-8 string
        html = raw_response.decode("utf-8")

        soup = BeautifulSoup(html, 'html.parser')

        title_result = []
        link_result = []
        description_result = []
        # Find all the search result divs
        divs = soup.select("#search div.g")
        for div in divs:
            results = div.select("h3")
            if (len(results) >= 1):
                title_result.append(results[0].get_text())
        

        for i in range(len(title_result)):
            link_url = link_result[i]
            link_text = title_result[i]

            link_md = f"[{link_text}]({link_url})"
            st.markdown(link_md, unsafe_allow_html=True)

            st.write(description_result[i])
        