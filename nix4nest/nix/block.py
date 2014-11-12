from nix import Block as NixBlock

from .inject import Inject
from nix4nest.nix.node import Node
from nix4nest.nix.connection import Connection
from nix4nest.nix.signal import Signal
from nix4nest.nest_api.nestfactory import NestFactory


class BlockMixin(NixBlock):
    """
    This mixin adds special methods to the original NIX::Block
    """

    _node_types = ('neuron', 'stimulator')
    _conn_types = ('synapse',)

    class __metaclass__(Inject, NixBlock.__class__):
        # this injects all members and the doc into nix.core.File
        pass

    @property
    def nodes(self):
        sources = self.find_sources(lambda x: x.type in self._node_types)

        return [Node(x) for x in sources]

    @property
    def connections(self):
        sources = self.find_sources(lambda x: x.type in self._conn_types)

        return [Connection(x) for x in sources]

    @property
    def signals(self):
        signals = filter(lambda x: x.type == 'signal', self.data_arrays)

        return [Signal(x) for x in signals]

    def dump_node(self, nest_id, name=None):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        return NestFactory.dump_node(self, nest_id, name)

    def dump_connection(self, source_id, target_id, name=None):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param source_id:   ID of the NEST Node
        :param target_id:   ID of the NEST Node
        :return:            an instance of <IConnection> object.
        """
        return NestFactory.dump_connection(self, source_id, target_id, name)

    def dump_multimeter(self, nest_id, recordable, name=None):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param nest_id:     NEST ID of the multimeter
        :param recordable:  name of the recordable (like 'V_m')
        :return:            an instance of <IConnection> object.
        """
        return NestFactory.dump_multimeter(self, nest_id, recordable, name)