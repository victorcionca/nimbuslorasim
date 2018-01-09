"""
We need:
    * Deployment area
    * Layers of the network stack
    * Nodes with
        * address/ID
        * configuration
        * location
        * network stack, instantiated for the node
    * Node deployer
    * Node configurator
    * Post processing.

Input:
    * number of nodes
    * channel model
    * deployment engine: custom, takes in number of nodes, returns list of nodes
    * node configurator: takes in list of nodes, path loss model, configures all
"""
