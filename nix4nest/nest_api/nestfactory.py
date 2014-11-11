import nix

from nix4nest.nix.node import Node
from nix4nest.nix.connection import Connection
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
        assert(where.metadata is not None)
        assert(type(nest_id) == int)

        node = NestNode(nest_id)

        # check if node already exist in sources
        if len(where.find_sources(lambda x: x.name == node.name)) > 0:
            raise ValueError("Neuron with ID %d already exist" % nest_id)

        # check if node already exist in metadata
        sources = where.metadata.find_sections(lambda x: x.name == 'neurons')[0]
        if sources.find_sections(lambda x: x.name == node.name):
            raise ValueError("Metadata for neuron with ID %d already exist"
                             % nest_id)

        source = where.create_source(node.name, node.type)
        source.metadata = sources.create_section(node.name, node.type)

        for k, v in node.properties.items():
            value = [nix.Value(x) for x in v] if type(v) == list else nix.Value(v)
            source.metadata.create_property(k, value)

        return Node(source)

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
        assert(where.metadata is not None)
        assert(type(source_id) == int)
        assert(type(target_id) == int)

        connection = NestConnection(source_id, target_id)

        # check if connection already exist
        if len(where.find_sources(lambda x: x.name == connection.name)) > 0:
            raise ValueError("Connection between %d and %d already exist" %
                             (source_id, target_id))

        # check if connection already exist in metadata
        conns = where.metadata.find_sections(lambda x: x.name == 'connections')[0]
        if conns.find_sections(lambda x: x.name == connection.name):
            raise ValueError("Metadata for connection between %d and %d already"
                             "exist" % (source_id, target_id))

        source = where.create_source(connection.name, connection.type)
        source.metadata = conns.create_section(connection.name, connection.type)

        for k, v in connection.properties.items():
            value = [nix.Value(x) for x in v] if type(v) == list else nix.Value(v)
            source.metadata.create_property(k, value)

        return Connection(source)

    @staticmethod
    def dump_multimeter(where, nest_id, recordable):
        """
        Factory method to dump recorded signals from a Multimeter with a given
        NEST ID.

        :param where:       nix::Block where to create a signal
        :param recordable:  name of the recordable (like 'V_m')
        :return:            an instance of <AnalogSignal> object.
        """
        assert(type(nest_id) == int)

        mm = NestMultimeter(nest_id, recordable)

        name = "signal_from_%d" % nest_id
        iargs = [name, 'analogsignal', nix.DataType.Float, (len(mm.get_data()),)]
        signal = where.create_data_array(*iargs)

        signal.data.append(mm.get_data())
        signal.unit = 'mV'
        signal.append_range_dimension(mm.times)
        signal.dimensions[0].unit = 'ms'

        neurons = where.find_sources(lambda x: int(x.name) in mm.senders)
        map(signal.sources.append, neurons)

        #return Signal(signal)