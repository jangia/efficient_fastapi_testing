cq:
	poetry run ruff format .
	poetry run ruff check --fix .

ute:
	poetry run pytest efficient_testing

uti:
	poetry run pytest inefficient_testing