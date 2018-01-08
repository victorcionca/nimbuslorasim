class LoraNodeTemplate():
    """Template class for nodes."""

    def __init__(self, id, location, config, netstack, sim):
        """
        Parameters:
        id      -- id of node
        location-- location
        config  -- config, such as sf, txpower, bw, cr
        netstack-- network stack to use, class
        sim     -- simulator to access timing and events
        """
        self.id = id
        self.location = location
        self.config = config
        self.netstack = netstack(sim, config, self.app_receive)

    def app_process(self):
        """
        Application process that generates packets
        and feeds them to the network stack
        Makes use of the simulator for timings, events, etc.
        """
        pass

    def app_receive(self):
        """
        Callback to be passed to the network stack constructor.
        The net stack will call this when packets are received.
        """
        pass
