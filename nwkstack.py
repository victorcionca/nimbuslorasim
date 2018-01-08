class NetworkStackTemplate():
    """
    Template for network stacks.
    Net stacks are lists of layers.
    Must contain a physical layer.
    Must implement a config method.
    Must implement a transmit method that
    feeds packets into the topmost layer of the stack
    """

    def __init__(self, layer_stack, sim, config, appcb):
        """
        Parameters:
        layer_stack     -- List of layer classes
        appcb           -- application layer callback
        """
        self.layers = []
        for l in layer_stack:
            self.layers.append(l(sim, config))
        self.config = config
        self.sim = sim
        self.app_callback = appcb

    def transmit(self, data):
        """
        Takes data and passes it to the topmost layer in the stack
        """
        self.layers[0].send(data)

    def update_config(self, config):
        self.config = config
        for l in self.layers:
            l.update_config(config)
