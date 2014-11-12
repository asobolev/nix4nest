from __future__ import absolute_import

from .node import Node


class Signal(object):

    def __init__(self, nix_data_array):
        self._nix_data_array = nix_data_array
        self._source = None

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
        if not self._source and self._nix_data_array.sources:
            self._source = Node(self._nix_data_array.sources[0])
        return self._source

    @source.setter
    def source(self, node):
        """
        :param node:      nix4nest::Node
        """
        if self.source:
            self._nix_data_array.sources.remove(self.source._nix_source)
        self._nix_data_array.sources.append(node._nix_source)
        self._source = Node(self._nix_data_array.sources[0])

    @staticmethod
    def create_signal(where, name, values, unit, interval, s_unit='ms'):
        """
        Creates a Signal object representing recorded signal (by Multimeter).

        :param name:        simply name of the signal (str)
        :param where:       block where to create Node (nix::Block)
        :param values:      numpy array with values
        :param unit:        value units (str)
        :param interval:    sampling interval
        :param s_unit:      units of sampling (str)
        :return:            instance of Signal
        """
        assert(where.metadata is not None)
        assert(hasattr(values, 'dtype'))

        signal = where.create_data_array(name, 'signal', values.dtype, (0,))

        signal.data.append(values)
        signal.unit = unit

        signal.append_sampled_dimension(interval)
        signal.dimensions[0].unit = s_unit

        return Signal(signal)