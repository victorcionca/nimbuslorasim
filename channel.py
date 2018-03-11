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

    The channel keeps track of the reach of transmissions from each 
    node. When a packet is sent, all the nodes within reach will
    hear the packet.

    This is implemented as follows:
    - a map with nodeid: [nodeids], [nodeids] representing the nodes
    within and out of reach of the key node
    - this map is built at initialisation and holds, for each node
    the nodes within reach in ideal conditions (lowest BW, highest
    power, no obstacles)
    - then, for each node, the list of destinations is updated to
    the actual configuration
    - every time the node config changes, the list of destinations
    is updated.
    """

    def __init__(self, nodes, channel_model, logger):
        """
        Parameters
        nodes         -- List of nodes to consider in the network
        channel_model -- Channel model class
        """
        self.node_dests = {}
        self.nodes = {n.id:n for n in nodes}    # Dict of node_id: node obj
        self.channel_model = channel_model
        # Build the destinations map
        max_dist = channel_model.max_comms_range({'sf':12, 'txp':14})
        for n in nodes:
            reach = []
            for n_o in nodes:
                if n_o is not n:
                    if n.location.distance(n_o.location) <= max_dist:
                        reach.append(n_o.id)
            self.node_dests[n.id] = (reach, [])
        self.logger = logger
        self.pkt_stats = dict()     # pkt to list of nodes mapping

    def update_node(self, node, config):
        """
        A node has had its configuration changed.
        Update the node's destination list
        """
        reach = []
        notreach = []
        r,nr = self.node_dets[node.id]
        comms_dist = channel_model.max_comms_range(config)
        for n in r+nr:
            if n is None: continue
            if node.location.distance(self.nodes[n].location) <= comms_dist:
                reach.append(n)
            else:
                notreach.append(n)
        del r
        del nr
        self.node_dests[node.id] = (reach, notreach)

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

        TODO:
        For each reached node
        - calculate the RSSI
        - insert in phylayer of reached node _with_ RSSI
        - insert destination in packet statistics
        """
        # Determine based on the pkt config
        # which nodes are within the transmission reach
        reach = []
        # The packet will go to all the nodes within reach of src
        for n in self.node_dests[src][0]:
            n_rssi = self.calculate_rssi(pkt, src, n)
            # TODO Shouldn't make this check
            if pkt_rssi > self.channel_model.sensitivity[pkt.config['sf']]:
                # This packet reaches the dest, record
                # Insert into dest network stack.
                self.nodes[n].phy.recv_start(pkt, src, rssi)
                reach.append(n)
        # Store the nodes reached by the packet, for ref in packet end
        self.pkt_stats[(pkt.src, pkt.sendtime)] = reach

    def packet_end(self, pkt, src, dest):
        """
        The pkt transmission is finished.
        Return
        TX status: True if pkt delivered. False if pkt lost
        """
        # Inform the nodes reached by the packet
        reach = self.pkt_stats[(pkt.src, pkt.sendtime)]
        for n in reach:
            self.nodes[n].phy.recv_done(pkt, src)
        # Inform the higher layers about TX success status
        tx_done = dest is in reach
        # Delete the packet stats
        del self.pkt_stats[pkt_tuple]
        return tx_done
