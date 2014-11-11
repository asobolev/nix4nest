from __future__ import absolute_import

import nix


class Connection(object):

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
        """ Object NEST properties """
        return self._nix_source.metadata

    @property
    def source(self):
        """ Source ID for this connection """
        return self.properties['source']

    @property
    def target(self):
        """ Target ID for this connection """
        return self.properties['target']

    @staticmethod
    def create_connection(where, name, obj_type, params):
        """
        Creates a Node class representing NEST connection.

        :param where:       block where to create Connection (nix::Block)
        :param name:        name of the source node (str)
        :param obj_type:    type of the node (str)
        :param params:      node properties (dict)
        :return:            Connection object
        """
        assert(where.metadata is not None)

        # check if connection already exist in sources
        if len(where.find_sources(lambda x: x.name == name)) > 0:
            raise ValueError("Connection %s already exist" % name)

        # check if connection already exist in metadata
        sources = where.metadata.find_sections(lambda x: x.name == 'connections')[0]
        if sources.find_sections(lambda x: x.name == name):
            raise ValueError("Metadata for connection %s already exist" % name)

        source = where.create_source(name, obj_type)
        source.metadata = sources.create_section(name, obj_type)

        for k, v in params.items():
            value = [nix.Value(x) for x in v] if type(v) == list else nix.Value(v)
            source.metadata.create_property(k, value)

        return Connection(source)