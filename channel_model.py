class ChannelModel():

    sensitivity = {}        # Dictionary of sensitivity, indexed by SF

    @classmethod
    def path_loss(cls, src, dest, pkt):
        """
        Determines the path loss for the packet
        travelling from src to destination.
        Packet configuration is in pkt
        """
        pass

    @classmethod
    def calculate_rssi(cls, src, dest, pkt):
        """
        Based on the pkt configuration, determine the RSSI of the pkt at dest.
        """
        path_loss = cls.path_loss(src, dest, pkt)
        return pkt.config.txpow - path_loss

    @classmethod
    def max_comms_range(cls):
        """
        Based on the sensitivity determine the maximum comms range
        """
        pass
