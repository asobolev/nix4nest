from nix import Block as NixBlock

from .inject import Inject
from nix4nest.nix.node import Node
from nix4nest.nest_api.nestfactory import NestFactory


class BlockMixin(NixBlock):
    """
    This mixin adds special methods to the original NIX::Block
    """

    class __metaclass__(Inject, NixBlock.__class__):
        # this injects all members and the doc into nix.core.File
        pass

    def neurons(self):
        sources = self.find_sources(lambda x: x.type == 'neuron')

        return [Node(x) for x in sources]

    def connections(self):
        sources = self.find_sources(lambda x: x.type == 'connection')

        return [Node(x) for x in sources]

    def create_node(self, nest_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        return NestFactory.create_node(self, nest_id)

    def create_connection(self, source_id, target_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param source_id:   ID of the NEST Node
        :param target_id:   ID of the NEST Node
        :return:            an instance of <IConnection> object.
        """
        return NestFactory.create_connection(self, source_id, target_id)