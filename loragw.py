from nwkstack import NetworkStack

# TODO: Improve this

class LoraGW():

    def __init__(self, location, config, netstack, sim):
        """
        A node that sends data periodically

        Parameters:
        id      -- id of node
        location-- location
        config  -- config, such as sf, txpower, bw, cr
        netstack-- network stack to use
        sim     -- simulator to access timing and events
        """
        self.id = 0     # GWs always have id 0 for convenience; other nodes start at 1
        self.location = location
        self.config = config        # Doesn't the GW use special config, as in lowest data rate?
        self.netstack = netstack
        self.sim = sim

    def config_net_stack(self, layers, logger, channel):
        if self.config is None or self.sim is None:
            # TODO throw exception
            pass
        nwkstack = NetworkStack(logger, layers, self.sim, self.config,
                                self.app_receive, channel, self.id)
        self.netstack = nwkstack

    def app_process(self):
        """
        Application process that generates packets
        and feeds them to the network stack
        Makes use of the simulator for timings, events, etc.
        """
        # GW doesn't send packets periodically, it sends commands/ACKs etc
        pass

    def app_receive(self, data, src):
        """
        Callback to be passed to the network stack constructor.
        The net stack will call this when packets are received.
        """
        print('RXd', data, 'from', src)
