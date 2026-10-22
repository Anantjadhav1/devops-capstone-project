install:
	python -m pip install -r requirements.txt

test:
	pytest --cov=service --cov-report=term-missing

lint:
	flake8 service tests

run:
	flask --app service run --host=0.0.0.0 --port=8080

docker-build:
	docker build -t customer-accounts:latest .

