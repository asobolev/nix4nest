from __future__ import absolute_import
from .nixbase import NixBase
import nix


class Node(NixBase):

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