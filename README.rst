CMS Attendance
==================
|Pypi|

Manage and monitor attendance of users sharing a common WiFi,
using a specialized WiFi hotspot module.

This plugin is **only intended to be used with a CMS project**,
and not directly in any django project. To use in an independent
django project, you might need to configure your project.

Features
--------
- Track & monitor presence of a user, automatically after initial setup
- Extract comprehensive reports & logs via GraphQL APIs

Requirements
------------
- An ESP8266 or other compatible WiFi module needs to running for the attendance to be recorded.
- The ESP8266 must be flashed with `Module script <https://github.com/rivivo/LabTrac-Module>`_ .
- User's machines must also must be installed with `Client script <https://github.com/rivivo/LabTrac-Client>`_.

.. |Pypi| image:: https://img.shields.io/pypi/v/cms-attendance.svg
   :target: https://pypi.python.org/pypi/cms-forms
   :alt: Pypi