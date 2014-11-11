from __future__ import absolute_import

import nest
from ..irecorder import IRecorder


class NestSpikeDetector(IRecorder):
    """
    This class knows how to represent NEST Spike Detector for further
    serialization.
    """

    def __init__(self, nest_id):

        assert(nest.GetStatus([nest_id])[0]['model'] == 'spike_detector')

        super(NestSpikeDetector, self).__init__(nest_id)