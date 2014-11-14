from __future__ import absolute_import
from .nixbase import NixBase
from .node import Node


class SpikeTrain(NixBase):

    def __init__(self, nix_object):
        super(SpikeTrain, self).__init__(nix_object)
        self._source = None

    @property
    def data(self):
        return self._nix_object.data

    @property
    def data_type(self):
        return self._nix_object.data_type

    @property
    def unit(self):
        return self._nix_object.unit

    @property
    def source(self):
        if not self._source and self._nix_object.sources:
            self._source = Node(self._nix_object.sources[0])
        return self._source

    @source.setter
    def source(self, node):
        """
        :param node:      nix4nest::Node
        """
        if self.source:
            self._nix_object.sources.remove(self.source._nix_object)
        self._nix_object.sources.append(node._nix_object)
        self._source = Node(self._nix_object.sources[0])

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