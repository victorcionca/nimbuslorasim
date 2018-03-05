"""
We need:
    * Deployment area
    * Layers of the network stack
    * Nodes with
        * address/ID
        * configuration
        * location
        * network stack, instantiated for the node
    * Node class
    * Node deployer
    * Node configurator
    * Post processing - logger

Input:
    * number of nodes
    * channel model
    * deployment engine: custom, takes in number of nodes, returns list of nodes
    * node configurator: takes in list of nodes, path loss model, configures all
"""

from loranode import PeriodicLoraNode
from channel import Channel
from simpy import Environment
from logger import PacketLogger

def simulate(num_nodes, area, simtime, logfile, channel_model, net_layers, depl_eng, node_config):
    """
    Creates a simulation
    Parameters:
    area            -- Area object (e.g DiscArea)
    logfile         -- Path to file where logs should be saved
    channel_model   -- Channel model object
    net_layers      -- list of net layer classes
    depl_eng        -- Node deployment class
    node_config     -- Node configurator
    """
    # 1. Set up simulation engine, logger
    sim_eng = Environment()
    logger = PacketLogger(logfile)

    # 2. Deploy the nodes in the area
    gw, nodes = depl_eng.deploy_nodes(num_nodes,
                                      PeriodicLoraNode,
                                      channel_model, area)

    # 3. Common channel
    channel = Channel(gw+nodes, channel_model, logger)

    # 4. Configure nodes
    node_config.configure(nodes, gw, area, channel_model)

    # 5. Set up network stack for all nodes
    for g in gw:
        g.sim = sim_eng
        g.config_net_stack(net_layers, logger, channel)

    for n in nodes:
        # Register node with simulator
        n.period = 60   # TODO period is static for now
        n.sim = sim_eng
        # Register node application with simulation engine
        sim_eng.process(n.app_process())
        n.config_net_stack(net_layers, logger, channel)
        logger.add_node(n)

    # All set now for starting the simulation
    sim_eng.run(until=simtime)

    # Save logger results
    logger.persist()
