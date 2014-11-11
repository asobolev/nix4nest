from __future__ import absolute_import

import nest
from .ibase import IBase


# TODO rename to Recorder

class NestMultimeter(IBase):
    """
    This class knows how to represent any NEST Device (multimeter, spike
    detector) in python for further serialization.
    """

    def __init__(self, nest_id, recordable):
        assert(recordable in nest.GetStatus([nest_id])[0]['record_from'])

        super(NestMultimeter, self).__init__(nest_id)

        self._nest_id = nest_id
        self._properties = {}
        self._events = {}
        self._recordable = recordable

    @property
    def name(self):
        return str(self._nest_id)

    @property
    def properties(self):
        if not self._properties:
            nest_properties = dict(nest.GetStatus([self._nest_id])[0])

            for k, v in nest_properties.items():
                self._properties[str(k)] = [IBase._clean(x) for x in v] if \
                    type(v) == list else IBase._clean(v)

        return self._properties

    @property
    def _get_data(self):
        if not self._events:
            self._events = nest.GetStatus([self._nest_id], 'events')[0]
        return self._events

    @property
    def senders(self):
        return self._get_data['senders']

    @property
    def times(self):
        return self._get_data['times']