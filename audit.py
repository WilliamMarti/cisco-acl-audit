import sys
from netmiko import ConnectHandler



def main(hostname, username, password):


    cisco_device = {
        'device_type': 'cisco_ios',
        'ip':   hostname,
        'username': username,
        'password': password,
    }

    try:

        net_connect = ConnectHandler(**cisco_device)

    except:

        print "Could not connect to host"
        sys.exit

    # get ACLs
    acls = net_connect.send_command('sh access-lists | i list')
    acls = acls.split("\n")

    acllist = []

    for line in acls:

        line = line.split("list")[1]

        acllist.append(line.strip())

    for acl in acllist:

        print acl

    print "====================================="


    ## Get Config
    config = net_connect.send_command_expect('sh run | i access-group')
    config = config.split("\n")

    configlines = []

    for line in config:

        configlines.append(line.strip())

    for line in configlines:

        print line

    print "====================================="

    aclsfound = []
    found = False

    for cline in configlines:

        for aline in acllist:

            if aline in cline:

                aclsfound.append(aline)
                break

    print aclsfound




#boiler plate setup
if __name__ == "__main__":

  hostname = sys.argv[1]
  username = sys.argv[2]
  password = sys.argv[3]

  main(hostname, username, password)