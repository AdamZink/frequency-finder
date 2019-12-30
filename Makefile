.PHONY: app_count run_count app_values run_values


# Find the number of unique frequencies
app_count:
	docker build -f Dockerfile --build-arg PYTHON_FILE=app_count.py -t frequency-finder:dev-count .

run_count:
	docker run --rm -it --name frequency-finder frequency-finder:dev-count


# Find the value of each frequency
app_values:
	docker build -f Dockerfile --build-arg PYTHON_FILE=app_frequency_values.py -t frequency-finder:dev-values .

run_values:
	docker run --rm -it --name frequency-finder frequency-finder:dev-values
