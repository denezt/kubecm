# ADD THE FOLLOWING AS A PARAMETER or use current default user
# USER=myuser
CONF_VAULT=kubecm_vault
APPNAME=kubecm
TARGET_DIR=/usr/bin
EXT=py

all: clean preinstall install test
	@printf "Finished, running setup!\n"

preinstall:
	@printf "Installing Requirements...\n"
	@command -v ssdeep || sudo apt install ssdeep -y
	@sudo pip install -r requirements.txt
	@test -d $(HOME)/$(CONF_VAULT) || mkdir -v $(HOME)/$(CONF_VAULT) # Initial creation of the vault

clean:
	@printf "Removing, older instances of program.\n"
	@sudo find $(TARGET_DIR) -type f -name "$(APPNAME)" -delete && \
	printf "Successfully Removed, $(APPNAME)!\n"

install:
	@printf "Installing, $(APPNAME)\n"
	@find "utils/" -type f -name "$(APPNAME).$(EXT)"
	@sudo cp -a -v utils/$(APPNAME).$(EXT) $(TARGET_DIR)/$(APPNAME)
	@printf "Changing owner to $(USER)\n"
	@sudo chown $(USER):$(USER) $(TARGET_DIR)/$(APPNAME)
	@sudo chmod a+x $(TARGET_DIR)/$(APPNAME)
	@printf "Done!\n"

test:
	@printf "\033[36mRunning, test on \033[32m$(APPNAME)\033[0m\n"
	@[ -f $(TARGET_DIR)/$(APPNAME) ] && $(APPNAME) -h || \
	printf "\033[35mError:\t\033[31mUnable to test no program $(APPNAME) was found!\033[0m\n"
