from __future__ import absolute_import

import nest
from ..ibase import IBase


class NestNode(IBase):
    """
    This class knows how to represent any NEST Node in python for further
    serialization.
    """

    def __init__(self, nest_id):
        super(NestNode, self).__init__(nest_id)

        self._nest_id = nest_id

    def _fetch_properties(self):
        return dict(nest.GetStatus([self._nest_id])[0])

    @property
    def name(self):
        return str(self._nest_id)