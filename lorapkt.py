class LoraPacket():

    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.status = None
        self.airtime = None

    def airtime(self):
        """Computes the airtime based on the configuration"""
        pass

