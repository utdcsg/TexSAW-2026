CC = gcc
SRC = whatsthetime.c
FLAGS = -Wall -fno-stack-protector -m32 -no-pie
TARGET = whatsthetime

.PHONY: help
help: ## Show help for each Makefile recipes.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

.PHONY: build
build: ## Build the binary.
	$(CC) $(FLAGS) $(SRC) -o $(TARGET)

.PHONY: clean
clean: ## Delete the binary.
	rm $(TARGET)
