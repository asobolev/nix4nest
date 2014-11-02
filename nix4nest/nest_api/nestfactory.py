import nest
import nix

from nix4nest.nix.node import Node
from nix4nest.nix.connection import Connection
from .models.iafneuron import IAFNeuron
from .models.static_synapse import StaticSynapse


class NestFactory:
    """
    A factory class to create proper NIX objects from NEST entities.

    The class uses actual global state (NEST feature) to build objects.
    This is the only nest-dependent class in the API.
    """

    classes = {
        'iaf_neuron': IAFNeuron,
        'static_synapse': StaticSynapse
    }

    @staticmethod
    def create_node(where, nest_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param where:   nix::Block where to create a Node
        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        assert(where.metadata is not None)
        assert(type(nest_id) == int)

        properties = dict(nest.GetStatus([nest_id])[0])

        assert('model' in properties, "Cannot determine model")
        assert(str(properties['model']) in NestFactory.classes)

        node = NestFactory.classes[str(properties['model'])](nest_id)

        # check if node already exist in sources
        if len(where.find_sources(lambda x: x.name == node.name)) > 0:
            raise ValueError("Neuron with ID %s already exist" % nest_id)

        # check if node already exist in metadata
        sources = where.metadata.find_sections(lambda x: x.name == 'neurons')[0]
        if sources.find_sections(lambda x: x.name == node.name):
            raise ValueError("Metadata for neuron with ID %s already exist"
                             % nest_id)

        source = where.create_source(node.name, 'neuron')
        source.metadata = sources.create_section(node.name, 'neuron')

        for k, v in node.properties.items():
            value = [nix.Value(x) for x in v] if type(v) == list else nix.Value(v)
            source.metadata.create_property(k, value)

        return Node(source)

    @staticmethod
    def create_connection(where, source_id, target_id):
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

        name = "%s_%s" % (str(source_id), str(target_id))

        # check if connection already exist
        if len(where.find_sources(lambda x: x.name == name)) > 0:
            raise ValueError("Connection between %s and %s already exist" %
                             (source_id, target_id))

        # check if connection already exist in metadata
        conns = where.metadata.find_sections(lambda x: x.name == 'connections')[0]
        if conns.find_sections(lambda x: x.name == name):
            raise ValueError("Metadata for connection between %s and %s already"
                             "exist" % (source_id, target_id))

        source = where.create_source(name, 'connection')
        source.metadata = conns.create_section(name, 'connection')

        nest_conn = nest.GetConnections([source_id], [target_id])
        properties = dict(nest.GetStatus(nest_conn)[0])

        for k, v in properties.items():
            is_special = k in Node._special_attrs
            value = Connection._special_attrs[k](v) if is_special else nix.Value(v)
            source.metadata.create_property(str(k), value)

        return Connection(source)