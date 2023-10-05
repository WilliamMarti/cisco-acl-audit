# Cisco ACL Audit 

1. Print a list of all Access Lists on device
1. Print a list of all applied Access Lists
   1. Check for 'access-group' in interfaces
   1. Check for 'match ip address' in route-maps
   1. Check for 'snmp-server community' for SNMP community strings
1. Print a list of Access Lists that are not used

Usage:

```
# python audit.py $hostname $username $password
```
