import unittest

import nest
from nix4nest.nest_api.models.multimeter import NestMultimeter


class TestNode(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.neuron_id = nest.Create('iaf_neuron')[0]

        rec_params = {'record_from': ['V_m'], 'withtime': True}
        self.mm_id = nest.Create('multimeter', params=rec_params)[0]

        nest.Connect([self.mm_id], [self.neuron_id])

        self.mm = NestMultimeter(self.mm_id, 'V_m')

    def tearDown(self):
        nest.ResetKernel()

    def test_properties(self):
        for k in nest.GetStatus([self.mm_id])[0].keys():
            assert(k in self.mm.properties)

    def test_data(self):
        assert(len(self.mm.get_data()) == 0)

        nest.Simulate(50)

        assert(len(self.mm.get_data()) == 0)
        assert(len(self.mm.get_data(update=True)) == 49)

        assert(self.neuron_id in self.mm.senders)
        assert((self.mm.senders == self.neuron_id).all())