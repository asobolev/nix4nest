import unittest

import numpy as np
import nest
import nix
# TODO find nicer injection way
import nix4nest

from nix4nest.nix.weightstack import WeightStack


class TestWeightStack(unittest.TestCase):

    def setUp(self):
        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_append(self):
        sources = (1, 3, 2)
        targets = (4, 6, 5, 7)

        values = np.empty((0, len(sources), len(targets)))

        params = (self.block, 'foo', values, sources, targets)
        ws = WeightStack.create_weight_stack(*params)

        assert(len(self.block.weightstacks) > 0)
        test_ws = self.block.weightstacks[0]
        assert(ws.name == test_ws.name)

        snapshot = np.random.rand(1, len(sources), len(targets))
        ws.append_snapshot(snapshot, 5.0)
        assert(len(ws.data) == 1)
        assert(len(ws.dimensions[0].ticks) == 1)

        snapshot = np.random.rand(1, len(sources), len(targets))
        ws.append_snapshot(snapshot, 10.0)
        assert(len(ws.data) == 2)
        assert(len(ws.dimensions[0].ticks) == 2)

    def test_nest(self):
        nest.ResetKernel()

        new_neuron = lambda x: nest.Create('iaf_neuron')[0]
        sources = [new_neuron(x) for x in range(2)]
        targets = [new_neuron(x) for x in range(2)]

        syn_spec = {'weight': 5.0, 'model': 'static_synapse'}
        nest.Connect(sources, targets, 'all_to_all', syn_spec=syn_spec)

        params = (self.block, 'foo', np.empty((0, 2, 2)), sources, targets)
        ws = WeightStack.create_weight_stack(*params)

        snapshot = self.block.capture_weights(sources, targets)
        ws.append_snapshot([snapshot], 0)
        assert(len(ws.data) == 1)
        assert(len(ws.dimensions[0].ticks) == 1)
        for i, elem in enumerate(ws.dimensions[1].ticks):
            assert(elem == sources[i])
        for i, elem in enumerate(ws.dimensions[2].ticks):
            assert(elem == targets[i])

        nest.Simulate(50)

        snapshot = self.block.capture_weights(sources, targets)
        ws.append_snapshot([snapshot], 0)
        assert(len(ws.data) == 2)
        assert(len(ws.dimensions[0].ticks) == 2)