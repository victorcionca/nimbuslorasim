from nwklayer_template import NwkLayerTemplate

class PhyLayer(NwkLayerTemplate):
    """
    Physical layer of the network stack.
    In addition to the nwk layer functionality
    it will model the channel and handle collisions.
    """

    powerThreshold = [\
                    [6,6,7,9,13,16],\
                    [6,6,7,9,13,16],\
                    [7,7,6,9,13,16],\
                    [9,9,9,6,13,16],\
                    [13,13,13,13,6,16],\
                    [16,16,16,16,16,6]] # dB
    collisions = ['simple', 'capture', 'capture_nonorth']

    def __init__(self, sim, config, logger):
        self.myid = None
        self.sim = sim
        self.config = config
        self.logger = logger
        self.upper = None
        self.channel = None
        # PHY specific stuff
        self.incoming = []  # Packets in transit towards node
        # Configure the type of collision handled
        self.collision_type = 'capture_nonorth'

    def frequency_collision(self, p1, p2):
        if abs(p1.config['freq']-p2.config['freq'])<=120\
                and (p1.config['bw']==500 or p2.config['freq']==500):
            return True
        elif abs(p1.config['freq']-p2.config['freq'])<=60\
                and (p1.config['bw']==250 or p2.config['freq']==250):
            return True
        else:
            if abs(p1.config['freq']-p2.config['freq'])<=30:
                return True
        return False

    def sf_collision(self, p1, p2):
        if p1.config['sf'] == p2.config['sf']:
            return True
        return False

    def power_collision_1(self, p1, p2):
        """Collision with capture effect"""
        powerThreshold = 6
        if p1.config['sf'] == p2.config['sf']:
            if abs(p1.rssi - p2.rssi) < powerThreshold:
                 # packets are too close to each other, both collide
                 # return both packets as casualties
                 return (p1, p2)
            elif p1.rssi - p2.rssi < powerThreshold:
                 # p2 overpowered p1, return p1 as casualty
                 return (p1,)
            # p2 was the weaker packet, return it as a casualty
            return (p2,)
        else:
            return ()

    def power_collision_2(self, p1, p2):
        """Collision with capture effect and cross-channel interference"""
        # Conservative powerThreshold
        powerThreshold = 6
        if p1.config['sf'] == p2.config['sf']:
            return self.power_collision_1(p1, p2)
        else:
            # Checking for cross channel interference
            if abs(p1.rssi - p2.rssi) < powerThreshold:
               return ()
            elif p1.rssi - p2.rssi > powerThreshold:
               return (p2,)
            return (p1,)

    def timing_collision(self, p1, p2):
        # assuming p1 is the freshly arrived packet and this is the last check
        # we've already determined that p1 is a weak packet, so the only
        # way we can win is by being late enough (only the first n - 5 preamble symbols overlap)

        # we can lose at most (Npream - 5) * Tsym of our preamble
        Tpreamb = 2**p1.config['sf']/(1.0*p1.config['bw']) * (p1.preamble - 5)

        # check whether p2 ends in p1's critical section
        p2_end = p2.sendtime + p2.airtime()
        p1_cs = p1.sendtime + Tpreamb/1000
        if p1_cs < p2_end:
            # p1 collided with p2 and lost
            return True
        return False


    def check_collisions(self):
        """
        Go through the packets in the incoming list 
        and handle the collisions, marking the packets
        accordingly
        """
        if len(self.incoming) == 1: return  # Single packet in Q

        pkt = self.incoming[-1]
        for p in self.incoming[:-1]:
            # TODO Can we break out fast if we determine a collision?
            # Maybe if we keep track of the strongest packet?
            if self.collision_type == 'capture' or self.collision_type == 'capture_nonorth':
                if self.frequency_collision(pkt, p) and self.timing_collision(pkt, p):
                    if self.collision_type == 'capture':
                        collided = self.power_collision_1(pkt, p)
                    else:
                        collided = self.power_collision_2(pkt, p)
                    for c in collided:
                        c.collided = True
            else:
                if self.frequency_collision(pkt, p) and self.sf_collision(pkt, p):
                    pkt.collided = True
                    p.collided = True



    def send(self, pkt, dest):
        """
        A new packet for sending over the air.
        """
        # Set the packet send time
        pkt.sendtime = self.sim.now
        # TODO Should check if the TX is not busy at this time
        self.sim.process(self.send_process(pkt, dest))
        # TODO do we want to return something?

    def send_process(self, pkt, dest):
        """
        This is a simpy process that transmits the packet to the channel.
        """
        # Start transmitting the packet
        self.channel.packet_start(pkt, self.myid, dest)
        # Wait for the packet airtime
        yield self.sim.timeout(pkt.airtime())
        # Now notify the channel of packet completion
        rssi = self.channel.packet_end(pkt, self.myid, dest)
        # TODO log the results. Get the RSSI somehow
        self.logger.sent(self.myid, rssi)

    def recv_start(self, pkt, src):
        """
        A packet is on the channel and it's within earshot.
        Process the packet and its collisions
        """
        # TODO Can we get more packets? Is there a limit for the channel?
        # There shouldn't. Any number of packets can be sent at the same
        # time. They will interfere, cause collisions, etc.
        # The max number of radios/channels the BS has is only important
        # for different SFs...
        self.incoming.append(pkt)
        self.check_collisions()


    def recv_done(self, pkt, src):
        """
        A packet transmission is completed.
        """
        # Remove from the incoming list
        self.incoming.remove(pkt)

        # Log status of the packet
        if pkt.collided:
            self.logger.collision(src)
            del pkt.data
            del pkt
        else:
            # If there were no collisions, forward to upper layer
            self.logger.tx_success(src)
            self.upper.recv(pkt, src)
