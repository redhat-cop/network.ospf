# Health Checks

The role enables user to manage the OSPF resources independent of platforms and perform OSPF health checks.

## Capabilities

**OSPF Health Checks** :
- Enables users to perform health checks for OSPF neighborship.This platform-agnostic role enables the user to perform OSPF health checks.
- Users can perform the following health checks:
  - `all_neighbors_up`: Check if all OSPF neighbors are up.
  - `all_neighbors_down`: Check if all OSPF neighbors are down.
  - `min_neighbors_up`: Ensure a minimum number of OSPF neighbors are up.
  - `ospf_summary_status`: Get a summary status of OSPF neighbors.

This role enables users to create a runtime brownfield inventory with all the OSPF configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *ospfv2, *opfv3 and *ospf_interfaces network resource module. The tasks offered by this role can be observed below:

## Variables

| Variable Name        | Default Value | Required | Type | Description                                                   | Example |
|:---------------------|:-------------:|:--------:|:----:|:-------------------------------------------------------------|:-------:|
| `ansible_network_os` | `""`          | no      | str  | Network OS to be used during detection.                      | `"cisco.nxos.nxos"` |
| `resources`          | `['ospfv2', 'ospfv3', 'ospf_interfaces']`       | no       | list | List of resources to check for configuration drift.           | `['ospf_interfaces', 'ospfv2', 'ospfv3]` |
| `data_store`         | `""`          | yes      | dict | Specifies the data store to be used (local or SCM).           | See examples below. |
| `operations`         | `[]`          | yes      | list | List of operations to perform during the health checks.        | See examples below. |

### Perform OSPF Health Checks
- Health Checks operation fetches the current status of OSPF Neighborship health.
- This can also include details about the OSPF metrics(state, peer, priority, etc).

```yaml
health_checks.yml
---
- name: Perform OSPF health checks
  hosts: nxos
  gather_facts: false
  tasks:
  - name: OSPF Manager
    ansible.builtin.include_role:
      name: network.ospf.health_checks
    vars:
      ansible_network_os: cisco.nxos.nxos
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

## License
GNU General Public License v3.0 or later.
See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

## Author Information
- Ansible Network Content Team