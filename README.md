# Ansible Network Collection for Fujitsu PSWITCH


### Collection contents

delete

### Collection core modules

- **fos_command.py** — Run commands on devices running PSWITCH

- **fos_config.py** — Manage configuration on devices running PSWITCH

- **fos_facts.py** — Collect facts devices running PSWITCH


## Installation
### From source

The [fujitsu/ansible-collection-for-fos repository](https://github.com/fujitsu/ansible-collection-for-fos) contains the code for the collection.

### From Ansible Galaxy

TODO

## Version compatibility

* Ansible version 2.10 or later.
* Python 2.7 or higher and Python 3.5 or higher


## Using this collection

#### Before your begin

Install ansible.netcommon
```
ansible-galaxy collection install ansible.netcommon
```

#### Example
You can refer to the files in the example folder, modify the IP and other contents and execute:

```
ansible-playbook -i ./inventory playbook.yaml
```

**inventory**

```
[host]
10.10.10.10

[host:vars]
ansible_ssh_user=****
ansible_ssh_pass=****
ansible_connection=network_cli
ansible_network_os=fos
```

**playbook.yaml**

```
- hosts: host
  gather_facts: no

  tasks:
  - name: "show version"
    fos_command:
      commands:
        - show version
        - show hardware

  - name: "get hardware fact"
    fos_facts:
      gather_subset:
       - "config"

  - name: "configure interface settings"
    fos_config:
      lines:
        - lldp transmit
        - lldp receive
      parents: interface 0/16
```
