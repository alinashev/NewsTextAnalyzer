linter:
	pip install flake8
	flake8 .

packages:
	python setup.py build && python setup.py install
	cd project && python setup.py build && python setup.py install

dependencies:
	python -m pip install --upgrade pip
	pip install -r project/requirements.txt

test:
	python -m unittest discover -s tests/ingestion/url
	python -m unittest discover -s tests/ingestion/scraping
	python -m unittest discover -s tests/transformation
