#!/usr/bin/python3
"""
Test file for LoRa simulator
"""
from simple_areas import DiscArea
from time import time
from channel_model import ChannelModel
from phylayer import PhyLayer
from connected_random_node_deployer import ConnectedRandomNodeDeployment
from simulator import simulate
from random import seed

def sim_test_custom_sf(seed, num_nodes, sf):
    from node_config_custom_sf_setting import get_custom_sf_configurator
    area = DiscArea(300)
    simtime = 3600   # 1 day of simulation
    logfile = 'sim_%d.log'%int(time())
    channel_model = ChannelModel(area)
    net_layers = []
    depl_eng = ConnectedRandomNodeDeployment
    node_config = get_custom_sf_configurator(sf)

    return simulate(num_nodes, area, simtime, logfile, channel_model, net_layers, depl_eng, node_config)

def sim_test(seed, num_nodes):
    from node_config_slowest_setting import NodeConfigSlowestSetting
    area = DiscArea(300)
    simtime = 3600   # 1 day of simulation
    logfile = 'sim_%d.log'%int(time())
    channel_model = ChannelModel(area)
    net_layers = []
    depl_eng = RandomNodeDeployment
    node_config = NodeConfigSlowestSetting

    return simulate(num_nodes, area, simtime, logfile, channel_model, net_layers, depl_eng, node_config)

if __name__ == '__main__':
    usage="Usage: sim_test.py <random_seed> <num_nodes>"
    import sys

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    seed(int(sys.argv[1]))
    num_nodes = int(sys.argv[2])
