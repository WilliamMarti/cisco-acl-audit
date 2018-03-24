# Cisco ACL Aduit 
[![Build Status](https://travis-ci.org/WilliamMarti/Cisco-ACL-Audit.svg?branch=master)](https://travis-ci.org/WilliamMarti/Cisco-ACL-Audit)


1. Print a list of all Access Lists on device
2. Print a list of all applied Access Lists
  * Check for 'access-group' in interfaces
  * Check for 'match ip address' in route-maps
  * Check for 'snmp-server community' for SNMP community strings
3. Print a list of Access Lists that are not used

Usage:

```
# python audit.py $hostname $username $password
```
