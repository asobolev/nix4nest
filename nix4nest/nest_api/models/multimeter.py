from __future__ import absolute_import

import nest
from ..irecorder import IRecorder


class NestMultimeter(IRecorder):
    """
    This class knows how to represent any NEST Device (multimeter, spike
    detector) in python for further serialization.
    """

    def __init__(self, nest_id, recordable):
        assert(str(nest.GetStatus([nest_id])[0]['model']) == 'multimeter')
        assert(recordable in nest.GetStatus([nest_id])[0]['record_from'])

        super(NestMultimeter, self).__init__(nest_id)
        self._recordable = recordable

    @property
    def data(self):
        return self._get_data[self._recordable]