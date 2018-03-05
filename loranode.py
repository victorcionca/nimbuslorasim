from loranode_template import LoraNodeTemplate
from random import expovariate
from nwkstack import NetworkStack
from phylayer import PhyLayer

class PeriodicLoraNode(LoraNodeTemplate):

    def __init__(self, id, location, config, netstack, sim, period):
        """
        A node that sends data periodically

        Parameters:
        id      -- id of node
        location-- location
        config  -- config, such as sf, txpower, bw, cr
        netstack-- network stack to use
        sim     -- simulator to access timing and events
        period  -- data send period
        """
        self.id = id
        self.location = location
        self.config = config
        self.netstack = netstack
        self.phy = PhyLayer(sim, config, None)
        self.phy.myid = id
        self.sim = sim
        # TODO: period should be kwargs
        self.period = period

    def config_net_stack(self, layers, logger, channel):
        if self.config is None or self.sim is None:
            # TODO throw exception
            pass
        nwkstack = NetworkStack(logger, layers, self.sim, self.config,
                                self.app_receive, self.id)
        self.netstack = nwkstack
        # Connect the network stack to the phy layer
        nwkstack.layers[-1].lower = self.phy
        self.phy.upper = nwkstack.layers[-1]
        self.phy.channel = channel
        self.phy.logger = logger
        self.phy.sim = self.sim
        self.phy.config = self.config

    def app_process(self):
        """
        Application process that generates packets
        and feeds them to the network stack
        Makes use of the simulator for timings, events, etc.
        """
        while True:
            self.netstack.transmit("Hello", 0)  # Send "Hello" to the GW
            #print('New packet at ', self.sim.now)
            yield self.sim.timeout(expovariate(1.0/float(self.period)))

    def app_receive(self, data, src):
        """
        Callback to be passed to the network stack constructor.
        The net stack will call this when packets are received.
        """
        pass
