class LoraNodeTemplate():
    """Template class for nodes."""

    def __init__(self, id, location, config, netstack, sim):
        """
        Parameters:
        id      -- id of node
        location-- location
        config  -- config, such as sf, txpower, bw, cr
        netstack-- network stack to use, unique for the node
        sim     -- simulator to access timing and events
        """
        self.id = id
        self.location = location
        self.config = config
        self.netstack = netstack

    def config_net_stack(self, layers, logger, channel):
        """
        Creates a network stack for the node and binds it to
        the physical layer and the channel.
        """
        pass

    def app_process(self):
        """
        Application process that generates packets
        and feeds them to the network stack
        Makes use of the simulator for timings, events, etc.
        """
        pass
