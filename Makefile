rundemo:
	python demo/demo.py

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt
