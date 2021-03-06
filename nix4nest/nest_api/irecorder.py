from __future__ import absolute_import

import nest
from .ibase import IBase


class IRecorder(IBase):
    """
    This class implements common methods for any NEST recorder Device
    (multimeter, spike detector).
    """

    def __init__(self, nest_id):
        assert(str(nest.GetStatus([nest_id])[0]['node_type']) == 'recorder')

        super(IRecorder, self).__init__(nest_id)

        self._nest_id = nest_id
        self._events = {}

    def _fetch_properties(self):
        return dict(nest.GetStatus([self._nest_id])[0])

    def _get_data(self):
        if not self._events:
            self.refresh()
        return self._events

    def refresh(self):
        self._events = nest.GetStatus([self._nest_id], 'events')[0]

    @property
    def name(self):
        return str(self._nest_id)

    @property
    def senders(self):
        return self._get_data()['senders']

    @property
    def times(self):
        return self._get_data()['times']