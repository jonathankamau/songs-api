PROJECT_NAME := songs
REPO_NAME ?= songs-api
ORG_NAME ?= songs-api
# File names
DOCKER_TEST_COMPOSE_FILE := docker/test/docker-compose.yml
DOCKER_DEV_COMPOSE_FILE := docker/dev/docker-compose.yml

# Docker compose project names
DOCKER_TEST_PROJECT := "$(PROJECT_NAME)"
DOCKER_DEV_PROJECT := "$(PROJECT_NAME)"
APP_SERVICE_NAME := api
DOCKER_REGISTRY ?= gcr.io

# Repository Filter
ifeq ($(DOCKER_REGISTRY), docker.io)
	REPO_FILTER := $(ORG_NAME)/$(REPO_NAME)
else
	REPO_FILTER := $(DOCKER_REGISTRY)/$(ORG_NAME)/$(REPO_NAME)[^[:space:]|\$$]*
endif

.PHONY: help


## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '${YELLOW} make ${RESET} ${GREEN}<target> [options]${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
    	message = match(lastLine, /^
	@echo ''

## Generate .env file from the provided sample
env_file:
	@ chmod +x scripts/utils.sh && scripts/utils.sh addEnvFile
	@ echo " "

## Build the project image
dev:env_file
	${INFO} "Building required container image for the application on development..."
	@ echo " "
	@ docker-compose -p $(DOCKER_DEV_PROJECT) -f $(DOCKER_DEV_COMPOSE_FILE) build api
	${INFO} "Development Build Completed successfully"
	@ echo " "
	@ ${INFO} "Running the project environment..."
	@ echo " "
	@ docker-compose -p $(DOCKER_DEV_PROJECT) -f $(DOCKER_DEV_COMPOSE_FILE) up api

## Build project image on test environment and run tests
test:env_file
	${INFO} "Building required docker images for testing"
	@ echo " "
	@ docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) build --pull test
	${INFO} "Build Completed successfully"
	@ echo " "
	@ ${INFO} "Running tests in docker container..."
	@ echo " "
	@ docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) up test

  # COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
NC := "\e[0m"
RESET  := $(shell tput -Txterm sgr0)
# Shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE

APP_CONTAINER_ID := $$(docker-compose -p $(DOCKER_STG_PROJECT) -f $(DOCKER_STG_COMPOSE_FILE) ps -q $(APP_SERVICE_NAME))

IMAGE_ID := $$(docker inspect -f '{{ .Image }}' $(APP_CONTAINER_ID))

# Introspect repository tags
REPO_EXPR := $$(docker inspect -f '{{range .RepoTags}}{{.}} {{end}}' $(IMAGE_ID) | grep -oh "$(REPO_FILTER)" | xargs)