from lorapkt import LoraPacket
class NetworkStack():
    """
    Net stacks are lists of layers.
    Must contain a physical layer.
    Must implement a config method.
    Must implement a transmit method that
    feeds packets into the topmost layer of the stack
    Connects to a channel model that gets packets and
    dispatches them to other nodes.
    """

    def __init__(self, logger, layer_stack, sim, config, appcb, channel, myid):
        """
        Parameters:
        layer_stack     -- List of layer classes
        appcb           -- application layer callback
        channel         -- Model of the comms channel
        """
        self.logger = logger
        self.myid = myid
        self.app_callback = appcb
        self.layers = []
        if len(layer_stack) == 0:
            # TODO throw exception if no layers in the netstack
            pass
        for l in layer_stack:
            new_layer = l(sim, config, logger)
            # Connect layers
            if len(self.layers) > 0:
                self.layers[-1].lower = new_layer
                new_layer.upper = self.layers[-1]
            self.layers.append(new_layer)
        self.channel = channel
        # connect physical layer to channel
        self.channel_wrapper = ChannelWrapper(myid, channel, logger)
        self.layers[-1].lower = self.channel_wrapper
        # Connect the upper layer to the application wrapper
        self.layers[0].upper = AppWrapper(self.app_callback)
        self.config = config
        self.sim = sim

    def transmit(self, data, dest):
        """
        Takes data and passes it to the topmost layer in the stack.
        Converts the data from bytes to a packet object.
        """
        packet = LoraPacket(self.config, data, self.myid, dest)
        self.logger.created(self.myid)
        self.layers[0].send(packet, dest)

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

    def __init__(self, myid, channel, logger):
        self.myid = myid    # For src address
        self.channel = channel
        self.logger = logger

    def send(self, pkt, dest):
        pkt_rssi = self.channel.deliver(pkt, self.myid, dest)
        self.logger.sent(self.myid, pkt_rssi)

class AppWrapper():
    """
    Top level of the stack, above the upper layer.
    Translates from the layer stack to the application.
    """

    def __init__(self, app_callback):
        self.app_callback = app_callback

    def recv(self, pkt, src):
        """
        Packet has been received, notify the application.
        """
        self.app_callback(pkt.data, src)
