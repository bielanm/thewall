PHONY: .dev .test

dev:
	docker-compose --profile dev up

test:
	docker-compose --profile tests up --abort-on-container-exit