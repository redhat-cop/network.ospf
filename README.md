# Network OSPF Validated Content

This repository contains the `network.ospf` Ansible Collection.

## Description

The `network.ospf` enables user to manage the OSPF resources independent of platforms and perform SPF health checks.

**Capabilities**
- `Build Brownfield Inventory`: Users want to be able to get the facts for OSPF resources and store it as host_vars thus enabling the capability to get facts for all the hosts within the inventory and store facts in a structured format which acts as SOT.
- `OSPF Resource Management`: Users want to be able to manage the OSPFv2, OSPFv3 and OSPF interfaces configurations.This also includes the enablement of gathering facts, updating OSPF resource host-vars and deploying config onto the appliance.
- `OSPF Health Checks`: Users want to be able to perform health checks for OSPF neighborship.These health checks should be able to provide the OSPF neighborship status with necessary details.

### Usage
- This platform agnostic role enables the user to perform OSPF health checks.Users can perfrom following health checks:
       `all_neigbors_up`
       `all_neighbors_down`
       `min_neighbors_up`
       `ospf_summary_status`
- This role enables users to create a runtime brownfield inventory with all the OSPF configuration in terms of host vars. These host vars are ansible facts which have been gathered through the *ospfv2, *opfv3 and *ospf_interfaces network resource module.The tasks offered by this role could be observed as below:

### Perform OSPF Health Checks
- Health Checks operation fetch the current status of OSPF Neighborship health.
- This can also include the details about the OSPF metrics(state, peer, priority, etc).

```yaml
health_checks.yml
---
- name: Perform health checks
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: health_check
          vars:
            details: True
            checks:
              - name: all_neighbors_up
              - name: all_neighbors_down
              - name: min_neighbors_up
                min_count: 1
              - name: ospf_status_summary
```


### Building Brownfield Inventory with Persist
- Persist operation fetch the ospfv2, ospfv3 and ospf_interfaces facts and store them as host vars.
- Result of successful Persist operation would be an Inventory directory having facts as host vars acting as SOT
  for operations like deploy, etc.

```yaml
- name: Persist the facts into host vars
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: persist
          inventory_directory: './inventory'
```

#### Gather OSPF Facts
- Gather operation gathers the running-confguration specific to ospfv2, ospfv3 and ospf_interfaces resources.

```yaml
- name: Gather Facts
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: gather
```

#### Deploy OSPF Configuration
- Deploy operation will read the facts from the provided/default inventory and deploy the changes on to the appliances.

```yaml
- name: Deploy host vars facts
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: deploy
```

#### Detect configuration drift in OSPF Configuration
- Detect operation will read the facts from the provided/default inventory and detect if any configuration changes are there on the appliances using overridden state.

```yaml
- name: 
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: detect
```

#### Remediate configuration drift in OSPF Configuration
- Remediate operation will read the facts from the provided/default inventory and Remediate if any configuration changes are there on the appliances using overridden state.

```yaml
- name: 
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      actions:
        - name: remediate
      
### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.ospf/blob/main/CHANGELOG.rst).

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
