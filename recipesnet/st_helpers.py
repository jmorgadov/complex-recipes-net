import enum
import urllib.request

import streamlit as st
from bs4 import BeautifulSoup

from recipesnet.api import RecipesApi

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
)


def get_api() -> RecipesApi:
    with st.spinner("Loading data..."):
        if "api" not in st.session_state:
            st.session_state["api"] = RecipesApi()
        return st.session_state.api


def find_recipes():
    st.header("Search recipes")
    st.session_state.selected_ingr = st.session_state.get("selected_ingr", set())
    st.session_state.ignored_ingr = st.session_state.get("ignored_ingr", set())
    limit = st.session_state.limit = st.session_state.get("limit", -1)

    api = get_api()

    selected_ingrd = st.multiselect(
        "Recipes that use ...",
        api.ingredients,
        list(st.session_state.selected_ingr),
        key="ingr",
    )

    only = st.checkbox("Only those ingredients")

    ignored_ingrd = (
        []
        if only
        else st.multiselect(
            "but not use ...",
            api.ingredients,
            list(st.session_state.ignored_ingr),
            key="ignored",
        )
    )

    recipes = api.recipes_that_use(selected_ingrd, ignored_ingrd, only)
    recipes_ing_count = [
        len(list(api.recp_ingr_graph.neighbors(rec))) for rec in recipes
    ]

    if not only and recipes:
        max_value = max(recipes_ing_count)
        if limit == -1:
            limit = max_value
        if limit > max_value:
            st.session_state.limit = limit
        limit = st.slider(
            "Ingridients limit",
            min_value=1,
            max_value=max_value,
            value=limit,
            key="lim",
        )

    if st.button("Save search", disabled=not selected_ingrd):
        st.session_state.selected_ingr = selected_ingrd
        st.session_state.ignored_ingr = ignored_ingrd
        st.session_state.limit = limit
        st.experimental_rerun()

    recipes = [rec for i, rec in enumerate(recipes) if recipes_ing_count[i] <= limit]
    st.header(f"Recipes ({len(recipes)})")
    st.write(f"Recipes you can prepare using: {', '.join(selected_ingrd)}")
    for i, rec in enumerate(recipes):
        if st.button(rec, key=f"recipes_{i}"):
            st.session_state.selected_ingr = selected_ingrd
            st.session_state.recipe = rec


def recip_ingr_widget():
    st.header("Recipes info")
    st.session_state.selected_ingr = st.session_state.get("selected_ingr", set())
    selected_ingrd = list(st.session_state.selected_ingr)
    api = get_api()
    recipes = api.recipes
    selected_recipe = st.selectbox(
        "Ingredients of ...",
        recipes,
        recipes.index(st.session_state.recipe) if "recipe" in st.session_state else 0,
    )
    ingrs = sorted(api.ingr_of(selected_recipe))
    raw_ingrs_str = ", ".join(ingrs)
    ingrs = [
        i.capitalize() if i not in selected_ingrd else f":red[{i.capitalize()}]"
        for i in ingrs
    ]
    st.write(", ".join(ingrs))

    if selected_recipe and st.button(
        f"🔎 How to prepare {selected_recipe.capitalize()}"
    ):
        query = f"how to cook or prepare {selected_recipe} using: {raw_ingrs_str}"

        query = "+".join(query.split(" "))
        url = f"https://google.com/search?q={query}"

        # Perform the request
        with st.spinner("Searching ..."):
            request = urllib.request.Request(url)

        # Set a normal User Agent header, otherwise Google will block the request.
        request.add_header(
            "User-Agent",
            USER_AGENT,
        )
        raw_response = urllib.request.urlopen(request).read()

        # Read the repsonse as a utf-8 string
        html = raw_response.decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")

        title_result = []
        link_result = []
        description_result = []

        # Find all the search result divs
        divs = soup.select("#search div.g")
        for div in divs:
            results = div.find_all("h3")
            if len(results) >= 1:
                link_result.append(str(results[0].parent["href"]))
                title_result.append(results[0].get_text())

                tmp = results[0].parent.parent.parent.parent
                spans = tmp.find_all("span")

                description_result.append(" ".join([s.get_text() for s in spans]))

        for i in range(len(title_result)):
            link_url = link_result[i]
            link_text = title_result[i]

            link_md = f"#### {i + 1}. [{link_text}]({link_url})"
            st.markdown(link_md, unsafe_allow_html=True)

            st.write(description_result[i])
