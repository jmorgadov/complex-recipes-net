install:
	pip install -e .

remove:
	pip uninstall recipesnet

clean-graphs:
	rm -f ./recipesnet/data/*.gz

clean: clean-graphs
	rm -f ./recipesnet/data/*.json
