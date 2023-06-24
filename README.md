# recipes-net

Application for cook recipes analysis using complex networks.

How to run the project:

```bash
make         # Installs the project (and dependencies)
recipes-net  # Runs the streamlit app
```

To install and run manually:

```bash
pip install networkx streamlit
cd ./recipesnet
streamlit run Home.py
```

To uninstall:

```bash
make remove
```
