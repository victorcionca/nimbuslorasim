#!/usr/bin/python3
"""
Test file for LoRa simulator
"""
from simple_areas import DiscArea
from time import time
from channel_model import ChannelModel
from phylayer import PhyLayer
from random_node_deployer import RandomNodeDeployment
from node_config_slowest_setting import NodeConfigSlowestSetting
from simulator import simulate

num_nodes = 100
area = DiscArea(300)
simtime = 3600   # 1 day of simulation
logfile = 'sim_%d.log'%int(time())
channel_model = ChannelModel(area)
net_layers = []
depl_eng = RandomNodeDeployment
node_config = NodeConfigSlowestSetting

simulate(num_nodes, area, simtime, logfile, channel_model, net_layers, depl_eng, node_config)
