from lorapkt import LoraPacket

class NetworkStack():
    """
    Net stacks are lists of layers.
    Must implement a config method.
    Must implement a transmit method that
    feeds packets into the topmost layer of the stack
    """

    def __init__(self, logger, layer_stack, sim, config, appcb, myid):
        """
        Parameters:
        layer_stack     -- List of layer classes
        appcb           -- application layer callback
        """
        self.logger = logger
        self.myid = myid
        self.app_callback = appcb
        self.layers = [AppWrapper(self.app_callback)]
        for l in layer_stack:
            new_layer = l(sim, config, logger)
            # Connect layers
            self.layers[-1].lower = new_layer
            new_layer.upper = self.layers[-1]
            self.layers.append(new_layer)
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

    def update_config(self, config):
        self.config = config
        for l in self.layers:
            l.update_config(config)

class AppWrapper():
    """
    Top level of the stack, above the upper layer.
    Translates from the layer stack to the application.
    """

    def __init__(self, app_callback):
        self.app_callback = app_callback
        self.lower = None
        self.upper = None

    def recv(self, pkt, src):
        """
        Packet has been received, notify the application.
        """
        self.app_callback(pkt.data, src)

    def send(self, pkt, dest):
        self.lower.send(pkt, dest)
