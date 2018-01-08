class NwkLayerTemplate():
    """
    Template for a network layer.
    Has an upper and lower layer.
    Communicates via send/recv interface.
    """

    def __init__(self, sim, config):
        self.sim = sim
        self.config = config
        self.upper = None
        self.lower = None

    def send(self, pkt):
        """
        Receive pkt for sending to the lower layer.
        """
        pass

    def recv(self, pkt):
        """
        Receive pkt for sending to upper layer.
        """
        pass
