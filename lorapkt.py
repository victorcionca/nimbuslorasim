class LoraPacket():

    def __init__(self, config, data):
        self.config = config    # TXpow, SF, BW, CR
        self.data = data
        self.rssi = None
        self.status = None
        self.airtime = None

    def airtime(self):
        """Computes the airtime based on the configuration"""
        pass

