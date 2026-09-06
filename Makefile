build:
	docker build -t drone-missions-api .

run:
	docker run -d --name drone-missions -p 8000:8000 drone-missions-api

stop:
	docker rm -f drone-missions