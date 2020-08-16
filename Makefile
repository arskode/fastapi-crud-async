.PHONY: test
test:
	docker-compose run --rm backend pytest -v --cov-report term-missing --cov=src
	docker-compose stop
