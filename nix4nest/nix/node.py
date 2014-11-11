from __future__ import absolute_import

import nix


class Node(object):

    def __init__(self, nix_source):
        self._nix_source = nix_source

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_source.name)

    @property
    def type(self):
        """ Target ID for this connection """
        return self._nix_source.type

    @property
    def properties(self):
        """ Object NEST properties to be serialized """
        return self._nix_source.metadata

    @staticmethod
    def create_node(where, name, obj_type, params):
        """
        Creates a Node class representing NEST neurons, stimulators, recorders.

        :param where:       block where to create Node (nix::Block)
        :param name:        name of the node (str)
        :param obj_type:    type of the node (str)
        :param params:      node properties (dict)
        :return:            instance of Node
        """
        assert(where.metadata is not None)

        # check if node already exist in sources
        if len(where.find_sources(lambda x: x.name == name)) > 0:
            raise ValueError("Neuron %s already exist" % name)

        # check if node already exist in metadata
        sources = where.metadata.find_sections(lambda x: x.name == 'nodes')[0]
        if sources.find_sections(lambda x: x.name == name):
            raise ValueError("Metadata for node %s already exist" % name)

        source = where.create_source(name, obj_type)
        source.metadata = sources.create_section(name, obj_type)

        for k, v in params.items():
            value = [nix.Value(x) for x in v] if type(v) == list else nix.Value(v)
            source.metadata.create_property(k, value)

        return Node(source)