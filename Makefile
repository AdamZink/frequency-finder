.PHONY: app_count run_count

app_count:
	docker build -f Dockerfile -t frequency-finder:dev-count .

run_count:
	docker run --rm -it --name frequency-finder frequency-finder:dev-count
