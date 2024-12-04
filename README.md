# Ansible Network OSPF
[![CI](https://github.com/redhat-cop/network.ospf/actions/workflows/tests.yml/badge.svg?event=schedule)](https://github.com/redhat-cop/network.ospf/actions/workflows/tests.yml)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/7662/badge)](https://bestpractices.coreinfrastructure.org/projects/7662)

This repository contains the `network.ospf` Ansible Collection.

## About

- Ansible Network OSPF Collection contains the role that provides a platform-agnostic way of
  managing OSPF protocol/resources. This collection provides the user the capabilities to gather,
  deploy, remediate, detect, persist and perform health checks for network OSPF resources.

- Network OSPF collection can be used by anyone who is looking to manage and maintain ospf protocol/resources. This includes system administrators and IT professionals.

This collection includes the following roles:
- **`deploy`**: Ensure consistent configuration deployment across network devices.
- **`detect`**: Identify configuration drifts between desired and actual states.
- **`remediate`**: Automatically correct configuration drifts and restore compliance.
- **`gather`**: Collect facts and running configurations from network devices.
- **`persist`**: Save network device configurations and facts to local or remote repositories for backup or audit
purposes.
- **`health_checks`**: Enables to perform health checks for OSPF neighborship.

## Included content

Click on the name of a role to view its documentation:

<!--start collection content-->
### Roles
Name | Description
--- | ---
[network.ospf.deploy](roles/deploy/README.md) | Deploy consistent network configurations.
[network.ospf.detect](roles/detect/README.md) | Identify configuration drifts and discrepancies.
[network.ospf.remediate](roles/remediate/README.md) | Correct configuration drifts and restore compliance.
[network.ospf.gather](roles/gather/README.md) | Collect facts and running configurations from network devices.
[network.ospf.persist](roles/persist/README.md) | Save configurations and facts to local or remote repositories.
[network.ospf.health_checks](roles/health_checks/README.md) | Perform health checks for the OSPF neighborship.
<!--end collection content-->

## Requirements
- [Requires Ansible](https://github.com/ansible-network/network.ospf/blob/main/meta/runtime.yml)
- [Requires Content Collections](https://github.com/ansible-network/network.ospf/blob/main/galaxy.yml#L5https://forum.ansible.com/c/news/5/none)
- [Testing Requirements](https://github.com/ansible-network/network.ospf/blob/main/test-requirements.txt)
- Users also need to include platform collections as per their requirements. The supported platform collections are:
  - [arista.eos](https://github.com/ansible-collections/arista.eos)
  - [cisco.ios](https://github.com/ansible-collections/cisco.ios)
  - [cisco.iosxr](https://github.com/ansible-collections/cisco.iosxr)
  - [cisco.nxos](https://github.com/ansible-collections/cisco.nxos)
  - [junipernetworks.junos](https://github.com/ansible-collections/junipernetworks.junos)

## Installation
To consume this Validated Content from Automation Hub, the following needs to be added to ansible.cfg:
```
[galaxy]
server_list = automation_hub

[galaxy_server.automation_hub]
url=https://console.redhat.com/api/automation-hub/content/validated/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=<SuperSecretToken>
```

Utilize the current Token, and if the token has expired, obtain the necessary
token from the [Automation Hub Web UI](https://console.redhat.com/ansible/automation-hub/token).

With this configured, simply run the following commands:

```
ansible-galaxy collection install network.base
ansible-galaxy collection install network.ospf
```

## Use Cases


`Build Brownfield Inventory`:
- The `persist` role enables users to fetch the YAML structured resource module facts for OSPF resources OSPFv2, OSPFv3, OSPF interfaces and save it as host_vars to the local or remote data store which could be used as a single SOT for other operations.

`Configuration Deployment`:
- The `deploy` role enables a user to read the host_vars from a local or remote data store and deploys if any changes are found.

`Display Structured Configuration`:
- The `gather` role enables users to be able to gather and display the structured facts for provided network resources.

`Configuration Drift`:
- The `detect` role will read the facts from the default/local or remote inventory host_vars and detect if any configuration changes are there between running and the provided config configuration.

`Remediate Configuration`:
- The `remediate` role will read the facts from the provided/default or remote inventory and remediate if there are any configuration changes on the appliances. This is done by overriding the running configuration with read facts from the provided inventory host vars.

`Health Checks`:
- The `health_checks` role enables users to perform health checks for OSPF neighborship. These health checks should be able to provide the OSPF neighborship status with necessary details.Users can perform the following health checks:
  - `all_neigbors_up`
  - `all_neighbors_down`
  - `min_neighbors_up`
  - `ospf_summary_status`
- This role enables users to create a runtime brownfield inventory with all the OSPF configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *ospfv2, *opfv3 and *ospf_interfaces network resource module. The tasks offered by this role can be observed below:

## Testing

The project uses tox to run `ansible-lint` and `ansible-test sanity`.
Assuming this repository is checked out in the proper structure,
e.g. `collections_root/ansible_collections/network/ospf`, run:

```shell
  tox -e ansible-lint
  tox -e py39-sanity
```

To run integration tests, ensure that your inventory has a `network_ospf` group.
Depending on what test target you are running, comment out the host(s).

```shell
[network_hosts]
ios
junos

[ios:vars]
< enter inventory details for this group >

[junos:vars]
< enter inventory details for this group >
```

```shell
  ansible-test network-integration -i /path/to/inventory --python 3.9 [target]
```

## Contributing

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against this repository.

Don't know how to start? Refer to the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html)!

Want to submit code changes? Take a look at the [Quick-start development guide](https://docs.ansible.com/ansible/devel/community/create_pr_quick_start.html).

We also use the following guidelines:

* [Collection review checklist](https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_reviewing.html)
* [Ansible development guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible collection development guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Release notes

Release notes are available [here](https://github.com/redhat-cop/network.ospf/blob/main/CHANGELOG.rst).

## Related information

- [Developing network resource modules](https://github.com/ansible-network/networking-docs/blob/main/rm_dev_guide.md)
- [Ansible Networking docs](https://github.com/ansible-network/networking-docs)
- [Ansible Collection Overview](https://github.com/ansible-collections/overview)
- [Ansible Roles overview](https://docs.ansible.com/ansible/2.9/user_guide/playbooks_reuse_roles.html)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
