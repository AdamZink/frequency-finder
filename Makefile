.PHONY: app test run

app:
	docker build -f Dockerfile -t frequency-finder:dev .

run:
	docker run --rm -it --name frequency-finder frequency-finder:dev
