class PhyLayer(NwkLayerTemplate):
    """
    Physical layer of the network stack.
    In addition to the nwk layer functionality
    it will model the channel and handle collisions.
    """

    def __init__(self, sim, config):
        self.sim = sim
        self.config = config
        self.upper = None
        self.lower = None   # This won't change, there's nothing below
        # PHY specific stuff
        self.incoming = []  # Packets in transit towards node

    def check_collisions(self):
        """
        Go through the packets in the incoming list 
        and handle the collisions, marking the packets
        accordingly
        """
        pass

    def dispatch(self, pkt):
        """
        A packet is on the channel and it's within earshot.
        Process the packet and its collisions
        """
        # TODO Can we get more packets? Is there a limit for the channel?
        # There shouldn't. Any number of packets can be sent at the same
        # time. They will interfere, cause collisions, etc.
        # The max number of radios/channels the BS has is only important
        # for different SFs...
        self.incoming.append(pkt)
        self.check_collisions()

        # Yield for the pkt airtime

        # Remove from the list
        pass
