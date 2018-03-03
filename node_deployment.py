class NodeDeployment():
    """
    Deploys nodes in an area
    Implement the method below to create different deployers.
    """

    @classmethod
    def deploy_nodes(cls, num_nodes, Node, channel_model, area, **kwargs):
        """
        Creates number nodes and sets their location property
        Returns a tuple: gws, nodes

        Parameters:
        num_nodes       -- number of nodes to deploy
        Node            -- class to instantiate Node objects
        channel_model   -- channel model for radio propagation
        area            -- area object that implements get_bounds
        """
        pass
