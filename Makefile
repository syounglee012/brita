# Build the Docker container
build:
	docker build -t brita-app .

# Run the Docker container
run:
	docker run -p 8501:8501 brita-app

# Delete the Docker container
delete:
	docker stop $$(docker ps -a -q --filter ancestor=brita-app) && docker rm $$(docker ps -a -q --filter ancestor=brita-app)
