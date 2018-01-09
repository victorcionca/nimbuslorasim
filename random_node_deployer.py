class RandomNodeDeployment():
    """
    Deploys nodes in an area
    """

    @classmethod
    def deploy_nodes(cls, number, Node, channel_model, area_size=None):
        """
        Nodes are laid out randomly in an area of given size.
        No guarantees of connectivity are given if the area size is provided.
        Returns the created list of nodes.

        Parameters:
        number          -- number of nodes to deploy
        channel_model   -- channel model for radio propagation
        area_size       -- area is disc, this is the range. If None,
                           the maximum range that ensures communication 
                           will be obtained with the channel model.
        """
        nodes = []
        if area_size is None:
            area_size = channel_mode.max_comms_range()
        for n_id in range(number):
            # TODO select node location
            nodes.append(Node(n_id, location, None, None, None)
        return nodes
