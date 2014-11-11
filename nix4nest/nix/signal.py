from __future__ import absolute_import

import nix


class Signal(object):

    def __init__(self, nix_data_array):
        self._nix_data_array = nix_data_array

    @property
    def name(self):
        """ Object name / ID """
        return str(self._nix_data_array.name)

    @property
    def type(self):
        """ Target ID for this connection """
        return self._nix_data_array.type

    @property
    def data(self):
        return self._nix_data_array.data

    @property
    def data_type(self):
        return self._nix_data_array.data_type

    @property
    def dimensions(self):
        return self._nix_data_array.dimensions

    @property
    def unit(self):
        return self._nix_data_array.unit

    @property
    def source(self):
        return self._nix_data_array.sources[0].name

    @staticmethod
    def create_signal(where, source_name, times, values, unit):
        """
        Creates a Signal object representing recorded signal (by Multimeter).

        :param where:       block where to create Node (nix::Block)
        :param source_name: name of the source node (str)
        :param times:       numpy array with times (assuming units 'ms')
        :param values:      numpy array with values
        :param unit:        value units (str)
        :return:            instance of Signal
        """
        assert(where.metadata is not None)
        assert(len(times) == len(values))

        name = "signal_from_%d" % source_name
        iargs = [name, 'signal', nix.DataType.Float, (len(values),)]
        signal = where.create_data_array(*iargs)

        signal.data.append(values)
        signal.unit = unit
        signal.append_range_dimension(times)
        signal.dimensions[0].unit = 'ms'

        neurons = where.find_sources(lambda x: x.name == source_name)

        assert(len(neurons) == 1)
        map(signal.sources.append, neurons)

        return Signal(signal)