# Network OSPF Role.

The role enables user to manage the OSPF resources independent of platforms and perform OSPF health checks.

## Capabilities

**OSPF Resource Management** :
- Allows users to manage the OSPFv2, OSPFv3 and OSPF interface configurations. This also includes the enablement of gathering facts, updating OSPF resource host-vars and deploying config onto the network appliances.

**OSPF Health Checks** :
- Enables users to perform health checks for OSPF neighborship.This platform-agnostic role enables the user to perform OSPF health checks.
- Users can perform the following health checks:
  - `all_neighbors_up`: Check if all OSPF neighbors are up.
  - `all_neighbors_down`: Check if all OSPF neighbors are down.
  - `min_neighbors_up`: Ensure a minimum number of OSPF neighbors are up.
  - `ospf_summary_status`: Get a summary status of OSPF neighbors.

This role enables users to create a runtime brownfield inventory with all the OSPF configurations in terms of host vars. These host vars are ansible facts that have been gathered through the *ospfv2, *opfv3 and *ospf_interfaces network resource module. The tasks offered by this role can be observed below:

**Runtime Brownfield Inventory** :
- Helps users create a runtime inventory with all OSPF configurations. These configurations are stored as host variables (host vars) and are gathered using the following network resource modules:
- `ospfv2`
- `ospfv3`
- `ospf_interfaces`