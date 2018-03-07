from math import log10, exp

class ChannelModel():

    # Dictionary of sensitivity, indexed by SF
    sensitivity = {
                    7:-126.5,
                    8:-127.25,
                    9:-131.25,
                    10:-132.75,
                    11:-134.5,
                    12:-133.25
                    }


    def __init__(self, area):
        """
        The channel model is defined based on the deployment area
        """
        self.area = area
        self.Lpld0 = 127.41
        self.gamma = 2.08
        self.d0 = 40

    def path_loss(self, src_loc, dest_loc, tx_config):
        """
        Determines the path loss for a packet
        travelling from src location to destination location.
        Packet was sent with tx_config configuration.
        """
        dist = src_loc.distance(dest_loc)
        return self.Lpld0 + 10*self.gamma*log10(dist/float(self.d0))

    def calculate_rssi(self, src_loc, dest_loc, tx_config):
        """
        Based on the tx configuration, determine the RSSI of the pkt at dest.
        """
        path_loss = self.path_loss(src_loc, dest_loc, tx_config)
        return tx_config['txp'] - path_loss

    def max_comms_range(self, tx_config):
        """
        Based on the sensitivity and TX configuration 
        determine the maximum comms range.
        This is the range where the RSSI is equal to the sensitivity.
        """
        return self.d0*exp(
                (tx_config['txp'] - self.Lpld0 - self.sensitivity[tx_config['sf']])
                /(10*self.gamma))
