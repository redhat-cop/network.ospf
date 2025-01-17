=====================================
Network Ospf Collection Release Notes
=====================================

.. contents:: Topics

v6.0.0
======

Major Changes
-------------

- Restructured the network.ospf collection by converting supported operations into separate roles.

v5.0.0
======

Release Summary
---------------

With this release, the minimum required version of `ansible-core` for this collection is `2.15.0`. The last version known to be compatible with `ansible-core` versions below `2.15` is v4.0.0.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.15.0`, since previous ansible-core versions are EoL now.

Documentation Changes
---------------------

- Revised the instructions on when to utilize the token.
- Update readme as per the common template.
- Updated the URL to point to validated content instead of certified content.

v4.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. The last known version compatible with ansible-core<2.14 is `v3.0.0`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

v3.0.0
======

Major Changes
-------------

- Change `actions` to `operations`

Documentation Changes
---------------------

- Update docs, tests and GH matrix.

v2.0.0
======

Major Changes
-------------

- Add support for scm operations and remove inventory_directory attribute.

Bugfixes
--------

- rename var in task.

v1.0.0
======

Minor Changes
-------------

- place remediate task in include dir.

Bugfixes
--------

- Fix when no neighbor is present.
- Update directory structure for filter plugin.
