.PHONY: docker-build docker-run build clean

VERSION := $(shell git rev-parse --short HEAD 2>/dev/null || echo "latest")
CURDIR := $(CURDIR)

NAME = configos
IMAGE := $(NAME):$(VERSION)
IMAGE_BASE_NAME := ghcr.io/anaticulae/$(NAME)
IMAGE_TEST_NAME := ghcr.io/anaticulae/$(NAME)-test

docker-build:
	docker build -t $(IMAGE_BASE_NAME) .

# --progress=plain
docker-build-test:
	docker build -f env/test/Dockerfile -t $(IMAGE_TEST_NAME) .

docker-build-base:
	docker build -f env/base/Dockerfile -t $(IMAGE_BASE_NAME) .

docker-upload:
	docker push $(IMAGE_BASE_NAME)

docker-upload-test:
	docker push $(IMAGE_TEST_NAME)

docker-upload-base:
	docker push $(IMAGE_BASE_NAME)

docker-doctest: docker-build
	docker run -v $(CURDIR):/var/workdir $(IMAGE_BASE_NAME) "baw test docs"

docker-fasttest: docker-build
	docker run -v $(CURDIR):/var/workdir $(IMAGE_BASE_NAME) "baw test fast -n1"

docker-longtest: docker-build
	docker run -v $(CURDIR):/var/workdir $(IMAGE_BASE_NAME) "baw test long -n1"

docker-alltest: docker-build
	docker run -v $(CURDIR):/var/workdir $(IMAGE_BASE_NAME) "baw test all -n1"

docker-lint: docker-build
	docker run -v $(CURDIR):/var/workdir $(IMAGE_BASE_NAME) "baw lint all"

docker-release: docker-build
	docker run -v $(CURDIR):/var/workdir\
			-e GH_TOKEN=$(GH_TOKEN) $(IMAGE_BASE_NAME)\
			"baw release --no_test --no_linter"
