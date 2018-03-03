class NwkLayerTemplate():
    """
    Template for a network layer.
    Has an upper and lower layer.
    Communicates via send/recv interface.
    """

    def __init__(self, sim, config, logger):
        self.sim = sim
        self.config = config
        self.logger = logger
        self.upper = None
        self.lower = None

    def send(self, pkt, dest):
        """
        Receive pkt for sending to the lower layer.
        """
        pass

    def recv(self, pkt, src):
        """
        Receive pkt for sending to upper layer.
        """
        pass
