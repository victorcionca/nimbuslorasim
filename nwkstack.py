class NetworkStackTemplate():
    """
    Template for network stacks.
    Net stacks are lists of layers.
    Must contain a physical layer.
    Must implement a config method.
    Must implement a transmit method that
    feeds packets into the topmost layer of the stack
    Connects to a channel model that gets packets and
    dispatches them to other nodes.
    """

    def __init__(self, layer_stack, sim, config, appcb, channel, myid):
        """
        Parameters:
        layer_stack     -- List of layer classes
        appcb           -- application layer callback
        channel         -- Model of the comms channel
        """
        self.myid = myid
        self.layers = []
        for l in layer_stack:
            new_layer = l(sim, config)
            # Connect layers
            if len(self.layers) > 0:
                self.layers[-1].lower = new_layer
                new_layer.upper = self.layers[-1]
            self.layers.append(new_layer)
        self.channel = channel
        # connect physical layer to channel
        self.channel_wrapper = ChannelWrapper(myid, channel)
        self.layers[-1].lower = self.channel_wrapper
        self.config = config
        self.sim = sim
        self.app_callback = appcb

    def transmit(self, data):
        """
        Takes data and passes it to the topmost layer in the stack.
        Converts the data from bytes to a packet object.
        """
        # TODO convert to packet
        self.layers[0].send(data)

    def incoming(self, pkt, src):
        """
        A new packet is received over the channel.
        Dispatch it to the physical layer.
        """
        self.layers[-1].recv(pkt, src)

    def update_config(self, config):
        self.config = config
        for l in self.layers:
            l.update_config(config)

class ChannelWrapper():
    """
    Wrapper class to make a channel behave like a layer
    so it can be connected to the physical layer
    """

    def __init__(self, myid, channel):
        self.myid = myid    # For src address
        self.channel = channel

    def send(self, pkt, dest):
        self.channel.deliver(pkt, self.myid, dest)
