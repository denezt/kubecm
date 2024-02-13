# KUBECM - Kubernetes Configuration Management Program
## Easy Configuration Tools for Kubernetes Infrastructure engineers

### Prerequisities
* GNU Make v4.3
* Python v3.5+

### Purpose
This project is for creating and managing a vault for configuration storage.

### Important Tips
1. It is important that you have an initial configuration in the `~/.kube` directory.
2. You can create several different vaults of the same `~/.kube/config` configuration.
3. **CAUTION: You can also overwrite a vault if you use the same name during the backup.**

### Installation Process
``` sh
# Install and test kubecm
$ make all
```
<pre>
Removing, older instances of program.
Successfully Removed, kubecm!
Installing, kubecm
utils/kubecm.py
'utils/kubecm.py' -> '/usr/bin/kubecm'
Changing owner to toor
Done!
Running, test on kubecm
usage: kubecm [-h] --action ACTION [--config CONFIG] [--debug | --no-debug]

Kubernetes Configuration Manager

options:
  -h, --help           show this help message and exit
  --action ACTION      Action to perform (init, activate, declare, view)
  --config CONFIG      Configuration name
  --debug, --no-debug  Show debugging output
Finished, running setup!
</pre>


### Quick Step up for `kubecm` 
``` sh
# Initializing the first configuration
$ kubecm --action init
```

### Usages

``` sh
# Display the help menu
$ kubecm --help
```

<pre>
OUTPUT:
usage: kubecm [-h] --action ACTION [--config CONFIG] [--debug | --no-debug]

Kubernetes Configuration Manager

options:
  -h, --help           show this help message and exit
  --action ACTION      Action to perform (init, activate, declare, view)
  --config CONFIG      Configuration name
  --debug, --no-debug  Show debugging output
</pre>


``` sh
# Active a configuration from the `kubecm` vault named "aws"
# and saved the current configuration in ~/.kube/config as "digital-ocean"
$ kubecm --action activate --config aws
```
<pre>
Success:	Found file /home/toor/kubecm_vault/aws/.config.kcv.aws
WARNING:	First, we need to create a backup of the current configuration!
Proceed? [(y)/(n)]: y
Name the current configuration: digital-ocean
Success:	Generated config vault: /home/toor/kubecm_vault/digital-ocean
Success:	Cloning /home/toor/.kube/config as /home/toor/kubecm_vault/digital-ocean/config
Success:	Initialize for digital-ocean is Complete!
Success:	Activated Configuration from Vault: aws
</pre>


``` sh
# View all configurations stored in the `kubecm` vault
$ kubecm --action view
```
<pre>
Current Stored K8s Configurations:
aws
digital-ocean
google-cloud
vaporcloud
pluspower-servers
local
</pre>
