# Network OSPF Validated Content
[![CI](https://github.com/redhat-cop/network.ospf/actions/workflows/tests.yml/badge.svg?event=schedule)](https://github.com/redhat-cop/network.ospf/actions/workflows/tests.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7662/badge)](https://bestpractices.coreinfrastructure.org/projects/7662)

This repository contains the `network.ospf` Ansible Collection.

## Description

The `network.ospf` enables users to manage the OSPF resources independent of platforms and perform SPF health checks.

## Tested with Ansible

Tested with ansible-core 2.14 releases.

## Installation
#### Install from Automation Hub

To consume this Validated Content from Automation Hub, the following needs to be added to `ansible.cfg`:

```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://cloud.redhat.com/api/automation-hub/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```
Get the required token from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

With this configured, simply run the following commands:

```
ansible-galaxy collection install network.ospf
```

**Capabilities**
- `Build Brownfield Inventory`: This enables users to fetch the YAML structured resource module facts for OSPF resources OSPFv2, OSPFv3, OSPF interfaces and save it as host_vars to the local or remote data store which could be used as a single SOT for other operations.
- `OSPF Resource Management`: Users want to be able to manage the OSPFv2, OSPFv3 and OSPF interface configurations. This also includes the enablement of gathering facts, updating OSPF resource host-vars and deploying config onto the network appliances.
- `OSPF Health Checks`: Users want to be able to perform health checks for OSPF neighborship. These health checks should be able to provide the OSPF neighborship status with necessary details.

### Usage
- This platform-agnostic role enables the user to perform OSPF health checks. Users can perform the following health checks:
       `all_neigbors_up`
       `all_neighbors_down`
       `min_neighbors_up`
       `ospf_summary_status`
- This role enables users to create a runtime brownfield inventory with all the OSPF configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *ospfv2, *opfv3 and *ospf_interfaces network resource module. The tasks offered by this role could be observed below:

### Perform OSPF Health Checks
- Health Checks operation fetches the current status of OSPF Neighborship health.
- This can also include details about the OSPF metrics(state, peer, priority, etc).

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
      ansible_network_os: cisco.ios.ios
      operations:
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
- Persist operation fetches the ospfv2, ospfv3 and ospf_interfaces facts and store them as host vars.
- Result of successful Persist operation would be an Inventory directory having facts as host vars acting as SOT
  for operations like deploy, remediate, detect, etc.

#### fetch ospf resource facts and build local data_store.
```yaml
- name: Persist the facts into host vars
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
      data_store:
        local: "~/backup/network"
```

#### gather OSPF resource facts and publish persisted host_vars inventory to GitHub repository.
```yaml
- name: Persist the facts into remote data_store which is a github repository
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: persist
      persist_empty: false
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```
### Display Structured Data with Gather
- Gather operation gathers the running-configuration specific to ospfv2, ospfv3 and ospf_interfaces resources.

```yaml
- name: Display OSPF resources in structured format
  hosts: ios
  gather_facts: false
  tasks:
  - name: OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: gather
```

#### Deploy OSPF Configuration
- Deploy operation will read the facts from the provided/default or remote inventory and deploy the changes onto the appliances.

#### read host_vars from local data_store and deploy onto the field.
```yaml
- name: Deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
      data_store:
        local: "~/backup/network"
```

#### retrieve host_cars from GitHub repository and deploy changes onto the field.
```yaml
- name: retrieve config from github repo and deploy changes
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: deploy
      persist_empty: false
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

#### Detect configuration drift in OSPF Configuration
- Detect operation will read the facts from the local provided/default inventory and detect if any configuration diff exists w.r.t running-config.

```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        local: "~/backup/network"
```

- Detect operation will read the facts from GitHub repository inventory and detect if any configuration diff exists w.r.t running-config.

#### detect the config difference between host_vars in local data_store and running-config.
```yaml
- name: Configuration drift detection
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: detect
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
```

#### Remediate configuration drift in OSPF Configuration
- Remediate operation will read the facts from the locally provided/default inventory and remediate if any configuration changes are there on the appliances using overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        local: "~/backup/network"
```
- Remediate operation will read the facts from github repository and remediate if any configuration changes are there on the appliances using overridden state.

```yaml
- name: Remediate configuration
  hosts: rtr1
  gather_facts: false
  tasks:
  - name: Network OSPF Manager
    include_role:
      name: network.ospf.run
    vars:
      ansible_network_os: cisco.ios.ios
      operations:
        - name: remediate
      data_store:
        scm:
          origin:
            url: "{{ your_github_repo }}"
            token: "{{ github_access_token }}"
            user:
              name: "{{ ansible_github }}"
              email: "{{ your_email@example.com }}"
      
### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.


## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.ospf/blob/main/CHANGELOG.rst).

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
