from __future__ import absolute_import

from nix4nest.nest_api.inode import INode
import nest


class IAFNeuron(INode):

    _special_attrs = {
        'model': lambda x: str(x),
        'node_type': lambda x: str(x),
        'recordables': lambda x: [str(rec) for rec in x],
    }

    def __init__(self, nest_id):
        super(IAFNeuron, self).__init__(nest_id)

        self.nest_id = nest_id

    @property
    def name(self):
        return str(self.nest_id)

    @property
    def properties(self):
        nest_properties = dict(nest.GetStatus([self.nest_id])[0])

        properties = {}
        for k, v in nest_properties.items():
            is_special = k in self._special_attrs
            properties[str(k)] = self._special_attrs[k](v) if is_special else v

        return properties