class Channel():
    """
    This determines the nodes that are reached by a transmission.
    It therefore keeps track of the
    - nodes
    - their locations
    - their configuration

    Packet transmissions are represented as having a start time 
    and an endtime. These are two distinct events in time.
    When a packet starts, the nodes that are reached are recorded
    locally, so they can be readily available when the packet end
    event is received.

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
        self.pkt_stats = dict()     # pkt to list of nodes mapping

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

    def packet_start(self, pkt, src, dest):
        """
        A packet has been detected on the channel.
        This is the start of the packet
        """
        # Determine based on the pkt config if the transmission
        # reaches dest with RSSI over the sensitivity threshold.
        pkt_rssi = self.calculate_rssi(pkt, src, dest)
        pkt.rssi = pkt_rssi
        if pkt_rssi > self.channel_model.sensitivity[pkt.config['sf']]:
            # This packet reaches the dest, record
            self.pkt_stats[(pkt.src, pkt.sendtime)] = [dest]
            # If so, set the pkt RSSI and 
            # insert into dest network stack.
            self.nodes[dest].phy.recv_start(pkt, src)
        else:
            # RSSI not high enough so packet is lost
            # The packet doesn't reach the destination
            self.pkt_stats[(pkt.src, pkt.sendtime)] = []
            self.logger.lost(src)

    def packet_end(self, pkt, src, dest):
        """
        The pkt transmission is finished.
        """
        # The nodes reached by the TX are recorded already
        reach = self.pkt_stats[(pkt.src, pkt.sendtime)]
        # Need to save them here because a collision will delete the packet
        pkt_rssi = pkt.rssi
        pkt_tuple = (pkt.src, pkt.sendtime)
        if dest in reach:
            self.nodes[dest].phy.recv_done(pkt, src)
        else:
            pass
        # Delete the packet stats
        del self.pkt_stats[pkt_tuple]
        return pkt_rssi
