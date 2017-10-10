import sys
from netmiko import ConnectHandler



class Audit():



    def diff(self, first, second):
            second = set(second)
            return [item for item in first if item not in second]


    def printArray(self, arr):

        if not isinstance (arr, list):
            raise TypeError('Please provide a List argument')

        output = ""

        for line in arr:

            output += str(line) + "\n"

        return output



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

        acllist = []

        for line in acls:

            line = line.split("list")[1]

            acllist.append(line.strip())

        print ("Found ACLS -- \n")

        print (self.printArray(acllist))

        print ("\n=====================================\n")


        ## Get Config
        config = net_connect.send_command_expect('sh run | i access-group')
        config = config.split("\n")

        configlines = []

        for line in config:

            configlines.append(line.strip())

        print ("Applied ACLs --\n")

        appliedacls = []

        for line in configlines:

            applied = line.split()[2]

            appliedacls.append(applied)

            print (applied)

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

