import unittest

import numpy as np
import nest
import nix
# TODO find nicer injection way
import nix4nest

from nix4nest.nix.signal import Signal
from nix4nest.nix.node import Node


class TestSignal(unittest.TestCase):

    def setUp(self):
        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

        self.source = Node(self.block.create_source('foo', 'neuron'))

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_append(self):
        length = 10
        values = np.empty((0,))
        signal = Signal.create_signal(self.block, 'foo', values, 'mV', 1.0)

        signal.data.append(np.random.rand(length))
        assert(signal.data.size == length)

        signal.data.append(np.random.rand(length))
        assert(signal.data.size == 2 * length)

    def test_create(self):
        length = 10
        values = np.random.rand(length)

        signal = Signal.create_signal(self.block, 'foo', values, 'mV', 1.0)

        assert(not signal.source)

        signal.source = self.source

        assert(self.source.name == signal.source.name)
        assert(signal.data.size == length)
        assert(signal.sampling.sampling_interval == 1.0)

        assert(len(self.block.signals) > 0)
        test_sig = self.block.signals[0]
        assert(signal.name == test_sig.name)

    def test_dump(self):

        # network setup
        nest.ResetKernel()

        neuron_id = nest.Create('iaf_neuron')[0]

        dc_id = nest.Create("dc_generator", 1)[0]
        nest.SetStatus([dc_id], {'amplitude': 220., 'start': 20., 'stop': 40.})
        syn_spec = {'weight': 5.0, 'model': 'static_synapse'}
        nest.Connect([dc_id], [neuron_id], syn_spec=syn_spec)

        rec_params = {'record_from': ['V_m'], 'withtime': True}
        mm_id = nest.Create('multimeter', params=rec_params)[0]

        nest.Connect([mm_id], [neuron_id])

        # testing
        empty = self.block.dump_multimeter(mm_id, 'V_m')  # empty multimeter

        assert(not empty.source)
        assert(empty.data.size == 0)
        assert(empty.sampling.sampling_interval == 1.0)

        neuron = self.block.dump_node(neuron_id)
        nest.Simulate(50)

        signal = self.block.dump_multimeter(mm_id, 'V_m', 'new_mm')

        assert(neuron.name == signal.source.name)
        assert(signal.data.size == 49)
        assert(signal.sampling.sampling_interval == 1.0)