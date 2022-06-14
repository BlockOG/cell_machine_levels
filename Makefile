format:
	python3 -m black .
build:
	make format
	python3 tests
	rm -rf dist/
	python3 -m build
	twine upload -r pypi dist/*
install:
	pip3 install -U cell_machine_levels