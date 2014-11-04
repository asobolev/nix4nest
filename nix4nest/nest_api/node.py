from __future__ import absolute_import

import nest
from .ibase import IBase


class NestNode(IBase):
    """
    This class knows how to represent any NEST Node in python for further
    serialization.
    """

    _supported_types = (int, float, str)

    def __init__(self, nest_id):
        super(NestNode, self).__init__(nest_id)

        self._nest_id = nest_id
        self._properties = {}

    @property
    def name(self):
        return str(self._nest_id)

    @property
    def type(self):
        return self.properties['node_type']

    @property
    def properties(self):
        if not self._properties:
            nest_properties = dict(nest.GetStatus([self._nest_id])[0])

            for k, v in nest_properties.items():
                self._properties[str(k)] = [IBase._clean(x) for x in v] if \
                    type(v) == list else IBase._clean(v)

        return self._properties