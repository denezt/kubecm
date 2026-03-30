APPNAME=kubecm
EXT=py

.PHONY: all setup test

all: setup test
	@printf "Finished, running setup!\n"

setup:
	@printf "Installing Requirements...\n"
	@command -v ssdeep || sudo apt install ssdeep -y
	@sudo uv sync
	@test -d $(HOME)/$(CONF_VAULT) || mkdir -v $(HOME)/$(CONF_VAULT) # Initial creation of the vault

test:
	@printf "\033[36mRunning, test on \033[32mutils/$(APPNAME).$(EXT)\033[0m\n"
	@uv run utils/$(APPNAME).$(EXT) -h