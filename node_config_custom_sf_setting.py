def get_custom_sf_configurator(sf):
    """
    This is a function that generates configurators
    with custom SF
    """
    class NodeConfigCustomSFSetting():
        spr_f = sf
        @classmethod
        def configure(cls, nodes, gws, area, channel_model):
            """
            Uses the slowest datarate for all the nodes.
            TX power is max (14)
            """
            for g in gws:
                g.config = {'sf':cls.spr_f, 'bw':125, 'cr':(4,8), 'txp':14, 'freq':864000000}
            for n in nodes:
                n.config = {'sf':cls.spr_f, 'bw':125, 'cr':(4,8), 'txp':14, 'freq':864000000}
    return NodeConfigCustomSFSetting
