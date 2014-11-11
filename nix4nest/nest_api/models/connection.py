from __future__ import absolute_import

import nest
from ..ibase import IBase


class NestConnection(IBase):
    """
    This class knows how to represent any NEST Connection in python for further
    serialization.
    """

    def __init__(self, source_id, target_id):
        nest_conn = nest.GetConnections([source_id], [target_id])
        if not nest_conn:
            raise ValueError("No connection between neurons %d and %d" %
                            (source_id, target_id))

        super(NestConnection, self).__init__(source_id, target_id)

        self.source_id = source_id
        self.target_id = target_id

    def _fetch_properties(self):
        nest_conn = nest.GetConnections([self.source_id], [self.target_id])
        return dict(nest.GetStatus(nest_conn)[0])

    @property
    def name(self):
        return "%s_%s" % (str(self.source_id), str(self.target_id))

    @property
    def source(self):
        return self.properties['source']

    @property
    def target(self):
        return self.properties['target']