from __future__ import absolute_import
from .nixbase import NixBase
import numpy as np


class WeightStack(NixBase):

    def __init__(self, nix_object):
        super(WeightStack, self).__init__(nix_object)
        self._sources = []
        self._targets = []

    @property
    def data(self):
        return self._nix_object.data

    @property
    def data_type(self):
        return self._nix_object.data_type

    @property
    def dimensions(self):
        return self._nix_object.dimensions

    def append_snapshot(self, snapshot, time):
        self.data.append(snapshot)

        # extend time dimension
        if len(self._nix_object.dimensions) == 0:
            self.build_dimensions([time], self._sources, self._targets)
        else:
            dim = self._nix_object.dimensions[0]
            dim.ticks = np.array(list(dim.ticks) + [time])

    def build_dimensions(self, times, sources, targets):
        """
        Builds dimensions according to the given values.

        :param times:       ticks for time domain (in 'ms')
        :param sources:     list of NEST IDs of sources
        :param targets:     list of NEST IDs of targets
        :return:
        """
        for dim in (times, sources, targets):
            assert(len(dim) > 0)

        nix_array = self._nix_object

        nix_array.append_range_dimension(times)
        nix_array.append_range_dimension(sorted(sources))
        nix_array.append_range_dimension(sorted(targets))

        nix_array.dimensions[0].unit = 'ms'
        nix_array.dimensions[0].label = 'time'
        nix_array.dimensions[1].label = 'source'
        nix_array.dimensions[2].label = 'target'

    @staticmethod
    def create_weight_stack(where, name, weights, sources, targets, times=()):
        """
        Creates a Stack with connection weights evolution in time.

        :param name:        name of the weight stack (str)
        :param where:       block where to create Node (nix::Block)
        :param weights:     3D array with connection weights. Dimensions:
                                - time (1)
                                - source (2)
                                - target (3)
        :return:            instance of WeightStack
        """
        assert(hasattr(weights, 'dtype'))
        assert(len(weights.shape) == 3)
        for dim in (sources, targets):
            assert(len(dim) > 0)

        params = name, 'weightstack', weights.dtype, weights.shape
        ws = where.create_data_array(*params)
        ws.data.append(weights)

        weightstack = WeightStack(ws)

        if len(times) > 0:
            weightstack.build_dimensions(sources, targets, times)

        else:  # need to temporary store these because 'time' should be first
            weightstack._sources = sources
            weightstack._targets = targets

        return weightstack