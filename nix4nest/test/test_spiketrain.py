import unittest

import numpy as np
import nest
import nix
# TODO find nicer injection way
import nix4nest

from nix4nest.nix.spiketrain import SpikeTrain
from nix4nest.nix.node import Node


class TestSpikeTrain(unittest.TestCase):

    def setUp(self):
        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

        self.source = Node(self.block.create_source('foo', 'neuron'))

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_append(self):
        pass

    def test_create(self):
        length = 10
        times = np.random.rand(length)

        st = SpikeTrain.create_spiketrain(self.block, 'foo', times)

        assert(not st.source)

        st.source = self.source

        assert(self.source.name == st.source.name)
        assert(st.data.size == length)

        assert(len(self.block.spiketrains) > 0)
        test_st = self.block.spiketrains[0]
        assert(st.name == test_st.name)

    def test_dump(self):

        # network setup
        nest.ResetKernel()

        n1_id = nest.Create('iaf_neuron')[0]
        n2_id = nest.Create('iaf_neuron')[0]

        dc1_id = nest.Create("dc_generator", 1)[0]
        nest.SetStatus([dc1_id], {'amplitude': 220., 'start': 20., 'stop': 40.})
        dc2_id = nest.Create("dc_generator", 1)[0]
        nest.SetStatus([dc2_id], {'amplitude': 220., 'start': 60., 'stop': 80.})

        syn_spec = {'weight': 5.0, 'model': 'static_synapse'}
        nest.Connect([dc1_id], [n1_id], syn_spec=syn_spec)
        nest.Connect([dc2_id], [n2_id], syn_spec=syn_spec)

        sd_id = nest.Create('spike_detector')[0]
        nest.ConvergentConnect([n1_id, n2_id], [sd_id])

        # testing
        empty = self.block.dump_spike_detector(sd_id)  # empty detector
        assert(len(empty) == 0)

        n1 = self.block.dump_node(n1_id)  # dump nodes such that they are
        n2 = self.block.dump_node(n2_id)  # connected to the spiketrains
        nest.Simulate(100)

        spiketrains = self.block.dump_spike_detector(sd_id, 'new_sd')

        assert(len(spiketrains) == 2)

        # spiketrain from first neuron should have times < 50.0
        st1 = filter(lambda x: x.source.name == n1.name, self.block.spiketrains)[0]
        assert(st1.data.size > 0)
        assert((st1.data[:] < 50.0).all())

        # spiketrain from second neuron should have times > 50.0
        st2 = filter(lambda x: x.source.name == n2.name, self.block.spiketrains)[0]
        assert(st2.data.size > 0)
        assert((st2.data[:] > 50.0).all())
