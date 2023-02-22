from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
    name: health_check_view
    author: Rohit Thakur (@rohitthakur2590)
    version_added: "1.0.0"
    short_description: Generate the filtered health check dict based on the provided target.
    description:
        - Generate the filtered health check dict based on the provided target.
    options:
      health_facts:
        description: Specify the health check dictionary.
        type: dict
"""

EXAMPLES = r"""
- name: health_check
    vars:
      checks:
        - name: all_neighbors_up
          ignore_errors: true
        - name: all_neighbors_down
          ignore_errors: true
        - name: min_neighbors_up
          min_count: 2
        - name: ospf_status_summary

- set_fact:
   "ospf_health":{
        "neighbors": [
            {
                "address": "11.0.13.3",
                "dead_time": "00:00:38",
                "interface": "GigabitEthernet0/1",
                "neighbor_id": "3.3.3.3",
                "peer_state": "FULL/BDR",
                "priority": 1
            },
            {
                "address": "10.0.12.2",
                "dead_time": "00:00:33",
                "interface": "GigabitEthernet0/0",
                "neighbor_id": "2.2.2.2",
                "peer_state": "FULL/BDR",
                "priority": 1
            }
        ]
    }

- name: Set health checks fact
  ansible.builtin.set_fact:
     health_checks: "{{ ospf_health | health_check_view(item) }}"

ok: [192.168.22.43] => {
    "failed_when_result": false,
    "health_checks": {
        "all_neighbors_down": {
            "check_status": "unsuccessful",
            "details": {
                "neighbors": []
            },
            "down": 0,
            "total": 2,
            "up": 2
        },
        "all_neighbors_up": {
            "check_status": "successful",
            "details": {
                "neighbors": [
                    {
                        "address": "11.0.13.3",
                        "dead_time": "00:00:38",
                        "interface": "GigabitEthernet0/1",
                        "neighbor_id": "3.3.3.3",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    },
                    {
                        "address": "10.0.12.2",
                        "dead_time": "00:00:33",
                        "interface": "GigabitEthernet0/0",
                        "neighbor_id": "2.2.2.2",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    }
                ]
            },
            "down": 0,
            "total": 2,
            "up": 2
        },
        "min_neighbors_up": {
            "check_status": "successful",
            "details": {
                "neighbors": [
                    {
                        "address": "11.0.13.3",
                        "dead_time": "00:00:38",
                        "interface": "GigabitEthernet0/1",
                        "neighbor_id": "3.3.3.3",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    },
                    {
                        "address": "10.0.12.2",
                        "dead_time": "00:00:33",
                        "interface": "GigabitEthernet0/0",
                        "neighbor_id": "2.2.2.2",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    }
                ]
            },
            "down": 0,
            "total": 2,
            "up": 2
        },
        "ospf_status_summary": {
            "details": {
                "neighbors": [
                    {
                        "address": "11.0.13.3",
                        "dead_time": "00:00:38",
                        "interface": "GigabitEthernet0/1",
                        "neighbor_id": "3.3.3.3",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    },
                    {
                        "address": "10.0.12.2",
                        "dead_time": "00:00:33",
                        "interface": "GigabitEthernet0/0",
                        "neighbor_id": "2.2.2.2",
                        "peer_state": "FULL/BDR",
                        "priority": 1
                    }
                ]
            },
            "down": 0,
            "total": 2,
            "up": 2
        },
        "status": "successful"
    }
}
"""

RETURN = """
  health_checks:
    description: OSPF health checks 
    type: dict

"""

from ansible.errors import AnsibleFilterError

ARGSPEC_CONDITIONALS = {}
OSPF_FULL_STATES = ["FULL/BDR", "FULL/DR"]

def health_check_view(*args, **kwargs):
    params = ["health_facts", "target"]
    data = dict(zip(params, args))
    data.update(kwargs)
    if len(data) < 2:
        raise AnsibleFilterError(
            "Missing either 'health facts' or 'other value in filter input,"
            "refer 'health_check_view' filter plugin documentation for details",
        )

    ospf_summary = data["health_facts"]
    v4_health = ospf_summary.get("v4")
    v6_health = ospf_summary.get("v6")
    if v4_health:
        health_facts = v4_health
    else:
        health_facts = v6_health
    target = data["target"]
    health_checks = {}
    health_checks['status'] = 'successful'
    if target['name'] == 'health_check':
        vars = target.get('vars')
        if vars:
            checks = vars.get('checks')
            dn_lst = []
            un_lst = []
            for item in health_facts['neighbors']:
                if item['peer_state'] in OSPF_FULL_STATES:
                    un_lst.append(item)
                else:
                    dn_lst.append(item)
            stats = {}
            stats['up'] = len(un_lst)
            stats['down'] = len(dn_lst)
            stats['total'] = stats['up'] + stats['down']

            details = {}
            data = get_health(checks)
            if data['summary']:
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                health_checks[data['summary'].get('name')] = n_dict

            if data['all_up']:
                n_dict = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'up')
                if n_dict['check_status'] == 'unsuccessful' and not data['all_up'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks[data['all_up'].get('name')] = n_dict

            if data['all_down']:
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = dn_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'down')
                if n_dict['check_status'] == 'unsuccessful' and not data['all_down'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks[data['all_down'].get('name')] = n_dict

            opr = is_present(checks, 'min_neighbors_up')
            if opr:
                n_dict = {}
                details = {}
                n_dict.update(stats)
                if vars.get('details'):
                    details['neighbors'] = un_lst
                    n_dict['details'] = details
                n_dict['check_status'] = get_status(stats, 'min', data['min_up']['min_count'])
                if n_dict['check_status'] == 'unsuccessful'  and not data['min_up'].get('ignore_errors'):
                    health_checks['status'] = 'unsuccessful'
                health_checks['min_neighbors_up'] = n_dict
        else:
            health_checks = health_facts
    return health_checks


def get_status(stats, check, count=None):
    if check in ('up', 'down'):
        return 'successful' if stats['total'] == stats[check] else 'unsuccessful'
    else:
        return 'successful' if count <= stats['up'] else 'unsuccessful'

def get_health(checks):
    dict = {}
    dict['summary'] = is_present(checks, 'ospf_status_summary')
    dict['all_up'] = is_present(checks, 'all_neighbors_up')
    dict['all_down'] = is_present(checks, 'all_neighbors_down')
    dict['min_up'] = is_present(checks, 'min_neighbors_up')

    return dict

def get_ignore_status(item):
    if not item.get("ignore_errors"):
        item['ignore_errors'] = False
    return item

def is_present(health_checks, option):
    for item in health_checks:
        if item['name'] == option:
             return get_ignore_status(item)
    return None


class FilterModule(object):
    """health_check_view"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"health_check_view": health_check_view}
