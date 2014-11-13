from __future__ import absolute_import

from .node import Node


class SpikeTrain(object):

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
    def create_spiketrain(where, name, times, unit='ms'):
        """
        Creates a Spiketrain object representing recorded spike times
         (by Spike Detector).

        :param name:        simply name of the spiketrain (str)
        :param where:       block where to create Node (nix::Block)
        :param times:       numpy array with spike times
        :param unit:        value units (str)
        :return:            instance of Spiketrain
        """
        assert(hasattr(times, 'dtype'))

        st = where.create_data_array(name, 'spiketrain', times.dtype, (0,))

        st.data.append(times)
        st.unit = unit
        st.append_set_dimension()

        return SpikeTrain(st)