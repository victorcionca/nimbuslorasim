from math import ceil

class LoraPacket():

    def __init__(self, config, data, src=None, dest=None,
                 header=False, preamble=8, ldropt=False):
        """
        Config is a dictionary with keys 'sf', 'txp', 'bw', 'cr', 'freq'
        'cr' in dictionary is given as tuple, eg 4/8 -> (4,8)
        header represents the implicit header
        preamble is the number of symbols in the preamble
        ldropt represents low data rate optimization.
        """
        self.config = config
        self.data = data
        self.src = src
        self.dest = dest
        self.rssi = None
        self.collided = False
        self.sendtime = None
        self.header = header
        self.preamble = preamble
        self.ldropt = ldropt

    def airtime(self):
        """Computes the airtime based on the configuration"""
        sf, bw, cr = [self.config[k] for k in ['sf', 'bw', 'cr']]
        cr = cr[1] - 4
        H = 1 if self.header else 0
        DE = 1 if self.ldropt else 0
        if self.config['bw'] == 125 and sf in [11, 12]:
            # low data rate optimization mandated for BW125 with SF11 and SF12
            DE = 1
        if sf == 6:
            # can only have implicit header with SF6
            H = 1

        Tsym = (2.0**sf)/bw
        Tpream = (self.preamble + 4.25)*Tsym
        payloadSymbNB = 8 + max(ceil((8.0*len(self.data)-4.0*sf+28+16-20*H)/(4.0*(sf-2*DE)))*(cr+4),0)
        Tpayload = payloadSymbNB * Tsym
        return (Tpream + Tpayload)/1000
