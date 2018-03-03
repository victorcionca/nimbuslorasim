import pickle

class PacketLogger():
    """
    Logs packet events: generation, sending, delivery, status, loss

    The log is stored as a two level dictionary.
    The first level has the node ids as the keys, the value
    being a second dictionary with keys
    'created', 'sent', 'tx_success', 'collision', 'lost'
    each counting the number of packets in that category.
    """

    def __init__(self, logfilepath):
        self.logfilepath = logfilepath
        self.pkt_log = dict()

    def persist(self):
        """
        Persists the logs to the logfile
        Uses pickle to serialise the log data
        """
        print('Pickling logs to', self.logfilepath)
        pickle.dump(self.pkt_log, open(self.logfilepath, 'wb'))

    def add_node(self, node):
        self.pkt_log[node.id] = {
                'pos':str(node.location), 'created':0, 'sent':0, 'tx_success':0, 'collision':0, 'lost':0, 'avg_rssi':0
                }

    def created(self, node_id):
        """Packet was generated and entered the network stack"""
        self.pkt_log[node_id]['created']+=1

    def sent(self, node_id, pkt_rssi):
        """Packet was sent from the phy layer of a network stack"""
        self.pkt_log[node_id]['sent']+=1
        prev_rssi = self.pkt_log[node_id]['avg_rssi']
        sent = self.pkt_log[node_id]['sent']
        self.pkt_log[node_id]['avg_rssi'] = ((sent-1)*prev_rssi + pkt_rssi)/sent

    def tx_success(self, node_id):
        """Packet was successfully received at the destination"""
        self.pkt_log[node_id]['tx_success']+=1

    def collision(self, node_id):
        """Packet sufferred a collision"""
        self.pkt_log[node_id]['collision']+=1

    def lost(self, node_id):
        """Packet couldn't reach the destination"""
        self.pkt_log[node_id]['lost']+=1


