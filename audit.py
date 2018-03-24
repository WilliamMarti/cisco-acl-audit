import sys
from netmiko import ConnectHandler



class Audit():


    # Return a List of the differences of 2 Lists
    def diff(self, first, second):

        if not isinstance (first, list) or not isinstance (second, list):
            raise TypeError('Please provide List type arguments')

        second = set(second)

        return [item for item in first if item not in second]

    # Return a String object of every line of the passed array
    def printArray(self, arr):

        if not isinstance (arr, list):
            raise TypeError('Please provide a List type argument')

        output = ""

        for line in arr:

            output += str(line) + "\n"

        return output

    # Run Search command for passed in Cisco IOS object
    def searchConfig(self, connector, searchtext):

        if not isinstance (searchtext, str):
            raise TypeError('Please provide a String type argument')

        config = connector.send_command_expect(searchtext)
        config = config.split("\n")

        configlines = []

        for line in config:

            configlines.append(line.strip())


        return configlines

    # Main method
    def main(self, hostname, username, password):


        cisco_device = {
            'device_type': 'cisco_ios',
            'ip':   hostname,
            'username': username,
            'password': password,
        }

        try:

            net_connect = ConnectHandler(**cisco_device)

        except:

            print ("Could not connect to host")
            sys.exit

        # get ACLs
        acls = net_connect.send_command('sh access-lists | i list')
        acls = acls.split("\n")

        if len(acls) == 0:

            print ("No ACLs defined")

        else:

            acllist = []

            for line in acls:

                line = line.split("list")[1]

                acllist.append(line.strip())

            print ("Found ACLS -- \n")

            print (self.printArray(acllist))

        print ("\n=====================================\n")

        print ("Applied ACLs --\n")

        appliedacls = []

        accessgroup = self.searchConfig(net_connect, 'sh run | i access-group')

        #print map(str, accessgroup)

        if accessgroup[0] == '':

            print ("No access groups found")

        else:

            for line in accessgroup:

                applied = line.split()[2]

                appliedacls.append(applied)



        matchipaddress = self.searchConfig(net_connect, 'sh run | i match ip address')


        if matchipaddress[0] == '':

            print ("No ACLs for route maps found")

        else:

            for line in matchipaddress:

                applied = line.split()[3]

                appliedacls.append(applied)


        snmpcommunity = self.searchConfig(net_connect, 'sh run | i snmp-server community')

        if snmpcommunity[0] == '':

            print ("No ACLs for SNMP found")

        else:

            for line in snmpcommunity:

                applied = line.split()[4]

                appliedacls.append(applied)

            print (self.printArray(appliedacls))

        print ("\n=====================================\n")

        print ("ACLs Defined But Not Used -- \n")

        aclsfound = []
        aclsnotfound = []

        found = False

        for aline in acllist:

            found = False

            for cline in appliedacls:

                if aline in cline:

                    found = True
                    break

            if found == False:

                aclsnotfound.append(aline)
                found = False

        print (self.printArray(aclsnotfound))

        print ("\n=====================================\n")

        print ("ACLs Used But Not Defined -- \n")

        # Get ACLs applied but not defined
        notdefined = self.diff(appliedacls, acllist)

        print (self.printArray(notdefined))


#boiler plate setup
if __name__ == "__main__":

    hostname = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    audit = Audit()

    audit.main(hostname, username, password)

