#!/usr/bin/env python

import os
import sys
import shutil
import subprocess
import pydeep
from datetime import datetime
from argparse import ArgumentParser, BooleanOptionalAction

vault_name = "kubecm_vault"
current_k8s_config = os.path.join(os.path.expanduser('~'), '.kube', 'config')
vault_dir = os.path.join(os.path.expanduser('~'), vault_name)
metadata_file_prefix = ".config.kcv"

def log_error(message):
    print(f"\033[35mError:\t\033[31m{message}\033[0m")
    print("\033[33m(try '-h' to review usage)\033[0m")
    sys.exit(1)

def log_warning(message):
    print(f"\033[35mWARNING:\t\033[31m{message}\033[0m")

def log_success(message):
    print(f"\033[35mSuccess:\t\033[32m{message}\033[0m")

def confirm_action():
    confirmation = input("Proceed? [(y)/(n)]: ").lower()
    return confirmation in ['y', 'yes']

def currentConfigInVault():
    curr_config_stored = False
    curr_config_hash = pydeep.hash_file(current_k8s_config)
    for root, dirs, files in os.walk(vault_dir):
        for file in files:
            if file.startswith("config"):
                vault_config_hash = pydeep.hash_file(os.path.join(root, file))
                comparing_hash = pydeep.compare(curr_config_hash, vault_config_hash)
                if comparing_hash:
                    curr_config_stored = True
                    break
    return curr_config_stored

# Will initial the vault for `kubecm`
def initialize_k8s_conf(srcname):
    vault_config_path = os.path.join(vault_dir, srcname)
    if os.path.isdir(vault_config_path):
        timestamp = datetime.now().strftime('%s')
        metadata_path = os.path.join(vault_config_path, f"{metadata_file_prefix}.{srcname}")
        with open(metadata_path, 'w') as f:
            f.write(f"{timestamp}|initialized")
        log_success(f"Initialize for {srcname} is Complete!")
    else:
        log_error(f"Config Source Directory {srcname} doesn't exist or no configuration was found")

def createBackup(srcname):
    # Ensure that the configuration source name is set
    if srcname:        
        config_vault_path = os.path.join(vault_dir, srcname)
        # Create the vault directory
        os.makedirs(config_vault_path, exist_ok=True)
        log_success(f"Generated config vault: {config_vault_path}")
        # Copies the current configuration to the vault directory
        shutil.copy(current_k8s_config, config_vault_path)
        log_success(f"Cloning {current_k8s_config} as {config_vault_path}/config")
        # Initialize the new vault
        initialize_k8s_conf(srcname)
    else:
        log_error("Missing configuration source name")

def activate_k8s_config(srcname):
    # Ensure that the configuration source name is set
    if not srcname:
        log_error("Missing configuration source name")
    # Search through file structure for metadata
    for root, dirs, files in os.walk(os.path.join(vault_dir, srcname)):
        for file in files:
            if file.startswith(metadata_file_prefix):
                metadata_file = os.path.join(root, file)
                log_success(f"Found file {metadata_file}")
                break
    # Create the Backup of current configuration to the vault
    if os.path.isfile(current_k8s_config) and not currentConfigInVault():
        log_warning("First, we need to create a backup of the current configuration!")
        if confirm_action():
            current_config_name = input("Name the current configuration: ")
            if current_config_name:
                timestamp = datetime.now().strftime('%s')
                config_vault_path = os.path.join(vault_dir, current_config_name)
                # Create the vault directory
                os.makedirs(config_vault_path, exist_ok=True)
                log_success(f"Generated config vault: {config_vault_path}")
                # Copies the current configuration to the vault directory
                shutil.copy(current_k8s_config, config_vault_path)
                log_success(f"Cloning {current_k8s_config} as {config_vault_path}/config")
                # Initialize the new vault
                initialize_k8s_conf(current_config_name)
            else:
                log_error("Missing or invalid configuration name")
        else:
            log_error("Backup is required before proceeding.")
    config_file = os.path.join(vault_dir, srcname, "config")
    if os.path.isfile(config_file):
        shutil.copy(config_file, current_k8s_config)
        log_success(f"Activated Configuration from Vault: {srcname}")
    else:
        log_error(f"Unable to find configuration source {srcname} from vault")

def view_k8s_configs():
    configs_found = False
    for root, dirs, files in os.walk(vault_dir):
        for file in files:
            if file.startswith(metadata_file_prefix):
                if not configs_found:
                    print("\033[36mCurrent Stored K8s Configurations:\033[0m")
                    configs_found = True
                print(f"\033[35m{file[len(metadata_file_prefix)+1:]}\033[0m")
    if not configs_found:
        print("No configurations found.")

def createInitialConfig():
    if os.path.exists(current_k8s_config):
        config_name = input(f"What is the name of the current configuration?: ")
        vault_item = os.path.join(vault_dir, config_name)
        if not os.path.exists(vault_item):
            os.makedirs(vault_item)
            shutil.copy(current_k8s_config, vault_item)
            initialize_k8s_conf(config_name)
            log_success("Saving configuration as {}".format(config_name))
        else:
            log_success("Configuration {} was already created".format(config_name))

def main():
    parser = ArgumentParser(description='Kubernetes Configuration Manager')
    parser.add_argument('--action', required=True, help='Action to perform (init, activate, backup, declare, view)')
    parser.add_argument('--config', help='Configuration name')
    parser.add_argument('--debug', action=BooleanOptionalAction, help='Show debugging output')
    args = parser.parse_args()    
    if args.action == 'backup':
        createBackup(args.config)
    elif args.action == 'declare':
        if not args.config:
            log_error("Configuration name is required for init action")
        initialize_k8s_conf(args.config)
    elif args.action == 'view':
        view_k8s_configs()
    elif args.action == 'activate':
        if not args.config:
            log_error("Configuration name is required for activate action")
        activate_k8s_config(args.config)
    elif args.action == 'init':
        createInitialConfig()
    else:
        log_error("Invalid action specified")

    if args.debug:
        print(args)
        print(f"Executed action: {args.action}")

if __name__ == "__main__":
    main()
