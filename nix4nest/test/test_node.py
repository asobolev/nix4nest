import unittest

import nest
import nix
# TODO find nicer injection way
import nix4nest


class TestNode(unittest.TestCase):

    def setUp(self):
        nest.ResetKernel()

        self.nest_id = nest.Create('iaf_neuron')[0]

        self.file = nix.File.open("/tmp/unittest.h5", nix.FileMode.Overwrite)
        self.block = self.file.create_nest_block("test block", "session")

    def tearDown(self):
        del self.file.blocks[self.block.id]
        self.file.close()

    def test_create_from_nest(self):
        neuron = self.block.create_node(self.nest_id)

        assert(neuron.name == str(self.nest_id))

        for k in nest.GetStatus([self.nest_id])[0].keys():
            assert(neuron.properties.has_property_by_name(str(k)))

    def test_block_neurons(self):
        neuron = self.block.create_node(self.nest_id)

        assert(len(self.block.neurons()) > 0)