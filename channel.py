class Channel():
    """
    This determines the nodes that are reached by a transmission.
    It therefore keeps track of the
    - nodes
    - their locations
    - their configuration.
    Implements the channel model, ie path loss, sensitivity.

    TODO: This initial version assumes all comms is towards the BS.
          Therefore it considers that other nodes are not receiving.
          However - receive windows in LoRa?
    """

    def __init__(self, nodes, channel_model, logger):
        """
        Parameters
        nodes         -- List of nodes to consider in the network
        channel_model -- Channel model class
        """
        self.nodes = {n.id:n for n in nodes}    # Dict of node_id: node obj
        self.channel_model = channel_model
        self.logger = logger

    def calculate_rssi(self, pkt, src, dest):
        """
        Determine RSSI at dest based on packet TX settings at src.
        """
        src_n = self.nodes[src]
        dst_n = self.nodes[dest]
        rssi = self.channel_model.calculate_rssi(src_n.location,
                                                 dst_n.location,
                                                 pkt.config)
        return rssi

    def deliver(self, pkt, src, dest):
        """
        A new packet to be delivered from src to dest
        There is no return value, on error packets are
        blown in the wind forever...
        """
        # Determine based on the pkt config if the transmission
        # reaches dest with RSSI over the sensitivity threshold.
        pkt_rssi = self.calculate_rssi(pkt, src, dest)
        if pkt_rssi > self.channel_model.sensitivity[pkt.config['sf']]:
            # If so, set the pkt RSSI and 
            # insert into dest network stack.
            pkt.rssi = pkt_rssi
            self.nodes[dest].netstack.incoming(pkt, src)
        else:
            # RSSI not high enough so packet is lost
            self.logger.lost(src)
        return pkt_rssi
