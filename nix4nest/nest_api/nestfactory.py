from nix4nest.nix.node import Node
from nix4nest.nix.connection import Connection
from nix4nest.nix.signal import Signal
from nix4nest.nest_api.models.node import NestNode
from nix4nest.nest_api.models.connection import NestConnection
from nix4nest.nest_api.models.multimeter import NestMultimeter


class NestFactory(object):
    """
    A factory class to create proper NIX objects from NEST entities.

    The class uses actual global state (NEST feature) to build objects.
    This is the only nix-dependent class in the NEST API.
    """

    @staticmethod
    def dump_node(where, nest_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param where:   nix::Block where to create a Node
        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        assert(type(nest_id) == int)

        node = NestNode(nest_id)
        return Node.create_node(where, node.name, node.type, node.properties)

    @staticmethod
    def dump_connection(where, source_id, target_id):
        """
        Factory method to build an connection instance from actual NEST global
        state using a nest source and target IDs.

        :param where:       nix::Block where to create a Node
        :param source_id:   ID of the source NEST Node
        :param target_id:   ID of the target NEST Node
        :return:            an instance of <IConnection> object.
        """
        assert(type(source_id) == int)
        assert(type(target_id) == int)

        cn = NestConnection(source_id, target_id)
        return Connection.create_connection(where, cn.name, cn.type, cn.properties)

    @staticmethod
    def dump_multimeter(where, nest_id, recordable):
        """
        Factory method to dump recorded signals from a Multimeter with a given
        NEST ID.

        :param where:       nix::Block where to create a signal
        :param nest_id:     NEST ID of the multimeter
        :param recordable:  name of the recordable (like 'V_m')
        :return:            an instance of <AnalogSignal> object.
        """
        assert(type(nest_id) == int)

        mm = NestMultimeter(nest_id, recordable)
        assert(len(mm.senders) == 1)

        return Signal.create_signal(where, mm.senders[0], mm.times, mm.data, mm.unit)