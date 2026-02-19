IMAGE_NAME=strong-locks
CONTAINER_NAME=strong-locks

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker run -d -p 8080:80 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker rm -f $(CONTAINER_NAME)

clean:
	docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker image rm $(IMAGE_NAME) 2>/dev/null || true

