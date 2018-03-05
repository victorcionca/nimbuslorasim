class NodeConfigSlowestSetting():

    @classmethod
    def configure(self, nodes, gws, area, channel_model):
        """
        Uses the slowest datarate for all the nodes.
        TX power is max (14)
        """
        for g in gws:
            g.config = {'sf':12, 'bw':125, 'cr':(4,8), 'txp':14, 'freq':864000000}
        for n in nodes:
            n.config = {'sf':12, 'bw':125, 'cr':(4,8), 'txp':14, 'freq':864000000}
