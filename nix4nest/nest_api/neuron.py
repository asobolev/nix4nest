from __future__ import absolute_import

from nix import Value
from nix4nest.interface.inode import INode
import nest


class Neuron(INode):

    _special_attrs = {
        'model': lambda x: Value(str(x)),
        'node_type': lambda x: Value(str(x)),
        'recordables': lambda x: [Value(str(rec)) for rec in x],
    }

    def __init__(self, nix_source):
        self._nix_source = nix_source

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_source.name)

    @property
    def properties(self):
        """ Object NEST properties to be serialized """
        return self._nix_source.metadata

    @classmethod
    def create_from_nest(cls, where, nest_id):
        """
        Factory method to build an instance from actual NEST global state using
        a given nest ID.

        :param where:   nix::Block where to create a Node
        :param nest_id: ID of the NEST Node
        :return:        an instance of <INode> object.
        """
        assert(where.metadata is not None)

        # check if neuron already exist in sources
        if len(where.find_sources(lambda x: x.name == str(nest_id))) > 0:
            raise ValueError("Neuron with ID %s already exist" % nest_id)

        # check if neuron already exist in metadata
        sources = where.metadata.find_sections(lambda x: x.name == 'sources')[0]
        if sources.find_sections(lambda x: x.name == str(nest_id)):
            raise ValueError("Metadata for neuron with ID %s already exist" % nest_id)

        source = where.create_source(str(nest_id), 'neuron')
        source.metadata = sources.create_section(str(nest_id), 'neuron')

        properties = dict(nest.GetStatus([nest_id])[0])
        for k, v in properties.items():
            value = cls._special_attrs[k](v) if k in cls._special_attrs else Value(v)
            source.metadata.create_property(str(k), value)

        return cls(source)