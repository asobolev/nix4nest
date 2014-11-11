import unittest

import nest
from nix4nest.nest_api.models.spike_detector import NestSpikeDetector


class TestNode(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.n1_id = nest.Create('iaf_neuron')[0]
        self.n2_id = nest.Create('iaf_neuron')[0]

        self.dc_id = nest.Create("dc_generator", 1)[0]
        profile = {'amplitude': 220., 'start': 20., 'stop': 40.}
        nest.SetStatus([self.dc_id], profile)

        syn_spec = {'weight': 5.0, 'model': 'static_synapse'}
        nest.Connect([self.dc_id], [self.n1_id], syn_spec=syn_spec)

        self.sd_id = nest.Create('spike_detector')[0]

        nest.Connect([self.n1_id, self.n2_id], [self.sd_id], 'all_to_all')

        self.sd = NestSpikeDetector(self.sd_id)

    def tearDown(self):
        nest.ResetKernel()

    def test_properties(self):
        for k in nest.GetStatus([self.sd_id])[0].keys():
            assert(k in self.sd.properties)

    def test_data(self):
        assert(len(self.sd.senders) == 0)
        assert(len(self.sd.times) == 0)

        nest.Simulate(50)

        assert(len(self.sd.senders) == 0)
        assert(len(self.sd.times) == 0)

        self.sd.refresh()

        assert(len(self.sd.senders) > 0)
        assert(len(self.sd.times) == len(self.sd.senders))

        assert(not self.n2_id in self.sd.senders)
        assert(self.n1_id in self.sd.senders)
        assert((self.sd.senders == self.n1_id).all())