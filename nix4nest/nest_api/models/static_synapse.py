from __future__ import absolute_import

from nix4nest.nest_api.iconnection import IConnection
import nest


class StaticSynapse(IConnection):

    _special_attrs = {
        'synapse_model': lambda x: str(x),
        'node_type': lambda x: str(x)
    }
    _properties = {}

    def __init__(self, source_id, target_id):
        super(StaticSynapse, self).__init__(source_id, target_id)

        self.source_id = source_id
        self.target_id = target_id

    @property
    def _nest_properties(self):
        nest_conn = nest.GetConnections([self.source_id], [self.target_id])
        return dict(nest.GetStatus(nest_conn)[0])

    @property
    def name(self):
        return "%s_%s" % (str(self.source_id), str(self.target_id))

    @property
    def properties(self):

        if not self._properties:
            for k, v in self._nest_properties.items():
                is_special = k in self._special_attrs
                self._properties[str(k)] = self._special_attrs[k](v) if is_special else v

        return self._properties

    @property
    def source(self):
        return self.properties['source']

    @property
    def target(self):
        return self.properties['target']