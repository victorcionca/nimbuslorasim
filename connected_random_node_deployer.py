from random import random
from math import tan, pi
from location_2d import Location2D
from loragw import LoraGW

class ConnectedRandomNodeDeployment():
    """
    Deploys nodes in a 2D disc with GW at the centre.
    Makes sure that all the nodes can talk to the GW
    """

    @classmethod
    def deploy_nodes(cls, num_nodes, Node, channel_model, area, **kwargs):
        """
        Nodes are laid out randomly in an area of given size.
        Makes sure that all the nodes can talk to the GW,
        so the area size will allow nodes with SF7, TXP2 to reach the GW.
        Returns tuple: gws, nodes deployed.

        Parameters:
        num_nodes       -- number of nodes to deploy
        Node            -- constructor for node class
        channel_model   -- channel model for radio propagation
        area            -- object of type DiscArea
        kwargs          -- additional params, not used here.
        """
        nodes = []
        area_size = channel_model.max_comms_range({'txp':2, 'sf':7})
        gw = LoraGW(Location2D(0,0), None, None, None)
        for n_id in range(1,num_nodes+1):  # GW id is 0
            # Select node location; GW is at 0,0
            x = random()*area_size
            alpha = random()*2*pi
            y = x*tan(alpha)
            nodes.append(Node(n_id, Location2D(x, y), None, None, None, None))
        return [gw], nodes
