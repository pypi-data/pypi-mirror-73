from sendit.protocols.etherframe import EtherFrame
from sendit.helper_functions.helper import *
from sendit.handlers.raw_nic import Raw_Nic
from threading import Thread


# Create a class called e listerner
# Has attributes about what it should be doing...
# what macs it should be listening to
# and what stacks it should be running ... ipv4, ipv6, or mac
# to add or remove a mac, use method!
# to add or remove a stack, use method!

class Ethernet_Listener():
    

    def __init__(self, macs, ipv4=True, ipv6=False, arp=True ):
        self.macs = macs
        self.ipv4 = ipv4
        self.ipv6 = ipv6
        self.arp = arp
        self.threads = list()
        for mac in macs:
            if self.ipv4:
                pass # launch ipv4 thread here
            if self.ipv6:
                pass # launch ipv6 thread here
            if self.arp:
                pass # launch arp thread here
        # Create list of all threads being kept...
        # Then these threads can be removed or added as values change
        # 
        pass
    
    def listen(self, interface):
        #Raw Nic will be created here
        nic = Raw_Nic(interface)
        while True:
            # Receive maximum amount of bytes
            data = nic.recv(1518)
            frame = E
            


        

    def add_MAC(self, mac):
        if helper.is_valid_mac(mac):
            macs.append(mac)
        else:
            pass
            #Throw error
    def remove_MAC(self, mac):
        try:
            self.macs.remove(mac)
        except ValueError:
            print("That MAC address was not in the current list")

    def set_on(self, protocol):
        lower = protocol.lower()
        if lower == "ipv4":
            self.ipv4 = True
        elif lower == "ipv6":
            self.ipv6 = True
        elif lower == "arp":
            self.arp = True
        else:
            raise ValueError(protocol + " is not a currently supported protocol for Ethernet_Listener")

    def set_off(self, protocol):
        lower = protocol.lower()
        if lower == "ipv4":
            self.ipv4 = False
        elif lower == "ipv6":
            self.ipv6= False
        elif lower == "arp":
            self.arp = False
        else:
            raise ValueError(protocol + " is not a currently supported protocol for Ethernet_Listener")



